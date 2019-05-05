# cloudflare-ddns
Simple Cloudflare DDNS update script for domain and subdomains.
I just created a quick and dirty sketch to update my personal DDNS records. It should be enough for most users, feel free to use.


In the config.json file is:

&nbsp;&nbsp;&nbsp;&nbsp;email: email of the cloudflare account

&nbsp;&nbsp;&nbsp;&nbsp;key: the global api key


## usage
* ```--config```: config path
* ```--repeat```: (optional) repeat every x seconds

```bash
$ python3.6 main.py --config config/config.json [--repeat 30]
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

## docker
##### build
```
docker build -t cloudflare-ddns .
```

##### run
* ```-v $(pwd)/config.json:/config.json```: mount config folder to docker container
* ```--config config.json --repeat 30```: the same usage of the main.py app

```
docker run -v $(pwd)/config.json:/config.json -t cloudflare-ddns --config config.json --repeat 30
```
