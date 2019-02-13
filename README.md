# cloudflare-ddns
Simple Cloudflare DDNS update script for domain and subdomains.
I just created a quick and dirty sketch to update my personal DDNS records. It should be enough for most users, feel free to use.


In the config.json file is:

&nbsp;&nbsp;&nbsp;&nbsp;email: email of the cloudflare account

&nbsp;&nbsp;&nbsp;&nbsp;key: the global api key


## usage

```bash
$ python3.6 main.py --config config.json
```

## config.json

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
