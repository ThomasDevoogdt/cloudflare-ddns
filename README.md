# cloudflare-ddns
Simple multi-record Cloudflare DDNS update script for domain and subdomains.
I just created a quick and dirty sketch to update my personal DDNS records. It should be enough for most users, feel free to use. The reason why I didn't use one of the hundreds of existing docker DDNS services is that I couldn't find any that supports multi-record DDNS updates.

## usage
* ```--config```: config path
* ```--repeat```: (optional) repeat every x seconds
* ```--log-level```: (optional) debug/info/error
* ```--force```: (optional) force ip upload

```bash
$ python3.6 main.py --config config.json [--repeat 30] [--force]
```

Arguments can also be applied with environment variables, prefixed with "DDNS_":
* ```export DDNS_CONFIG=config.json```
* ```export DDNS_REPEAT=30```
* ```export DDNS_LOG_LEVEL=debug```

## config.json
* email: cloudflare account
* key: global api key

```json
{
    "auth": {
        "email": "user@example.com",
        "key": "c2547eb745079dac9320b638f5e225cf483cc5cfdda41"
    },
    "zone": {
        "name": "example.com",
        "records": [
            "example.com",
            "www.example.com",
            "foo.example.com",
            "bar.example.com"
        ]
    }
}
```

## config.json v2.0

Records can now also be defined with a dictionary. The record should always contain the ```"name"``` key. See the record object definitions for optional attributes at https://api.cloudflare.com/#dns-records-for-a-zone-create-dns-record.

```json
{
    "auth": {
        "email": "user@example.com",
        "key": "c2547eb745079dac9320b638f5e225cf483cc5cfdda41"
    },
    "zone": {
        "name": "example.com",
        "records": [
            "example.com",
            {"name": "www.example.com", "proxied": true},
            "foo.example.com",
            {"name": "bar.example.com", "proxied": false}
        ]
    }
}
```

## config.json v3.0

More than one zone can now be defined under the ```"zones"``` key. The old ```"zone"``` key is still valid and is seen as one zone.

```json
{
    "auth": {
        "email": "user@example.com",
        "key": "c2547eb745079dac9320b638f5e225cf483cc5cfdda41"
    },
    "zones": [
        {
            "name": "example.com",
            "records": [
                "example.com",
                "foo.example.com",
            ]
        },
        {
            "name": "example2.com",
            "records": [
                "example2.com",
                "bar.example2.com",
            ]
        }
    ]
}
```

## docker
##### getting started
###### docker pull command
https://hub.docker.com/r/thomasdevoogdt/cloudflare-ddns
```
docker pull thomasdevoogdt/cloudflare-ddns
```

###### docker manual build
* ```cloudflare-ddns```: self chosen name
```
docker build -t cloudflare-ddns .
```

##### run
###### with command options
* ```-v $(pwd)/config.json:/config.json```: mount config folder to docker container
* ```--config config.json --repeat 30```: the same usage of the main.py app

Note: The manual build container needs to be run with the chosen name ```cloudflare-ddns```.
```
docker run -v $(pwd)/config.json:/config.json -t thomasdevoogdt/cloudflare-ddns --config config.json --repeat 30
```

###### with environment variables
* ```-v $(pwd)/config.json:/config.json```: mount config folder to docker container
* ```-e DDNS_CONFIG='config.json' -e DDNS_REPEAT='10'```: the same usage of the main.py app

Note: The manual build container needs to be run with the chosen name ```cloudflare-ddns```.
```
docker run -v $(pwd)/config.json:/config.json -t -e DDNS_CONFIG='config.json' -e DDNS_REPEAT='10' thomasdevoogdt/cloudflare-ddns
```
