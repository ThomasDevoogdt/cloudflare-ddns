# cloudflare-ddns
Simple Cloudflare DDNS update script for domain and subdomains.
I just created a quick and dirty sketch to update my personal DDNS records. It should be enough for most users, feel free to use.

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