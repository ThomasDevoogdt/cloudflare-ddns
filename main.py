#!/usr/bin/python

import argparse
import errno
import http.client
import ipaddress
import json
import logging
import os
import sys
import time

IPV4_FILE = "ipv4.txt"

def parse_args():
    prefix = "DDNS_"
    for env_key, value in os.environ.items():
        if env_key.startswith(prefix):
            argv_key = "--%s" % env_key[len(prefix):].lower().replace("_", "-")
            if argv_key not in sys.argv:
                sys.argv.append(argv_key)
                sys.argv.append(value)

    epilog = str('Arguments can also be applied with environment variables, prefixed with "DDNS_".\n'
                 'e.g.:\n'
                 '    * export DDNS_CONFIG=config.json :  --config config.json\n'
                 '    * export DDNS_REPEAT=5 :            --repeat 5\n')

    parser = argparse.ArgumentParser(description='CloudFlare DDNS', epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--config', type=argparse.FileType('r'), required=True)
    parser.add_argument('-r', '--repeat', type=int, required=False)
    parser.add_argument('-f', '--force', action='store_true', required=False)
    parser.add_argument('--log-level', type=str, required=False, default='info', choices=['debug','error','info'])
    return parser.parse_args()


def get_config(config):
    try:
        return json.loads(config.read())
    except:
        return None
    finally:
        config.close()


IP_PROVIDERS = [
    ("ifconfig.me", "/ip"),
    ("ip.42.pl", "/raw"),
    ("ipinfo.io", "/ip"),
    ("api.ipify.org", "/"),
    ("ip4.seeip.org", "/")
]


def get_ipv4():
    for provider in IP_PROVIDERS:
        try:
            conn = http.client.HTTPConnection(provider[0], timeout=10)
            conn.request("GET", provider[1], "")
            response = conn.getresponse().read().decode("utf-8").strip()
            ip = ipaddress.ip_address(response)
            assert isinstance(ip, ipaddress.IPv4Address)
            return str(ip)
        except:
            continue
        finally:
            conn.close()
    return None


def is_new_ipv4(ipv4):
    if os.path.isfile(IPV4_FILE):
        ipv4_file = open(IPV4_FILE, "r")
        old_ipv4 = ipv4_file.read()
        ipv4_file.close()
        if ipv4 == old_ipv4:
            return False

    ipv4_file = open(IPV4_FILE, "w")
    ipv4_file.write(ipv4)
    ipv4_file.close()
    return True


def clear_cache():
    try:
        os.remove(IPV4_FILE)
    except OSError as e:
        assert e.errno == errno.ENOENT


def get_xauth(config):
    return {
        'x-auth-email': config["auth"]["email"],
        'x-auth-key': config["auth"]["key"]
    }


def cloudflare_url(*args, **kwargs):
    try:
        conn = http.client.HTTPSConnection("api.cloudflare.com")
        conn.request(*args, **kwargs)
        return json.loads(conn.getresponse().read())
    except:
        return None
    finally:
        conn.close()


def get_cloudflare_zone_identifier(xauth_header, zone):
    try:
        url = "/client/v4/zones?name=%s" % zone
        return cloudflare_url("GET", url, "", xauth_header)["result"][0]["id"]
    except (KeyError, TypeError):
        return None


def get_cloudflare_record_identifier(xauth_header, zone_id, record_name):
    try:
        url = "/client/v4/zones/%s/dns_records?name=%s" % (zone_id, record_name)
        return cloudflare_url("GET", url, "", xauth_header)["result"][0]["id"]
    except (KeyError, TypeError):
        return None


def push_cloudflare_record(xauth_header, zone_id, record_id, record_name, ipv4):
    try:
        url = "/client/v4/zones/%s/dns_records/%s" % (zone_id, record_id)
        data = json.dumps({"id": zone_id, "type": "A", "name": record_name, "proxied": True, "content": ipv4})
        return cloudflare_url("PUT", url, data, xauth_header)["success"]
    except (KeyError, TypeError):
        return False


def update_ddns(config):
    ipv4 = get_ipv4()
    assert ipv4, "could not fetch ipv4 address, exiting"
    assert is_new_ipv4(ipv4), "ipv4 (%s) not changed, exiting" % ipv4
    logging.info("new ip address: %s" % ipv4)

    xauth_header = get_xauth(config)
    zone_identifier = get_cloudflare_zone_identifier(xauth_header, config["zone"]["name"])
    assert zone_identifier, "could not fetch zone identifier, exiting"

    logging.info("start updating cloudflare ddns records")
    for record in config["zone"]["records"]:
        record_identifier = get_cloudflare_record_identifier(xauth_header, zone_identifier, record)
        if record_identifier and push_cloudflare_record(xauth_header, zone_identifier, record_identifier, record, ipv4):
            logging.info("ip changed to %s for zone record %s" % (ipv4, record))
        else:
            logging.error("api update failed for zone record %s" % record)
    logging.info("updating cloudflare ddns done")


def main():
    args = parse_args()
    logging.basicConfig(level=args.log_level.upper())
    logging.info("starting cloudflare ddns service")

    if args.force:
        logging.info("forcing ip upload by clearing cache")
        clear_cache()

    config = get_config(args.config)
    assert config, "could not properly load config file, exiting"

    while True:
        try:
            update_ddns(config)
        except AssertionError as e:
            logging.debug(e)
        if not args.repeat:
            break
        time.sleep(args.repeat)


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info("Keyboard exception received. Exiting.")
