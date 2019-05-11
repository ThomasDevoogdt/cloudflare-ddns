# cloudflare-ddns
Simple Cloudflare DDNS update script for domain and subdomains.
I just created a quick and dirty sketch to update my personal DDNS records. It should be enough for most users, feel free to use.

## usage
* ```--config```: config path
* ```--repeat```: (optional) repeat every x seconds
* ```--log-level```: (optional) debug/info/error

```bash
$ python3.6 main.py --config config.json [--repeat 30]
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

## docker
##### getting started
###### docker pull command
https://hub.docker.com/r/thomasdevoogdt/cloudflare-ddns
```
docker pull thomasdevoogdt/cloudflare-ddns
```

###### docker manual build
```
docker build -t cloudflare-ddns .
```

##### run
###### with command options
* ```-v $(pwd)/config.json:/config.json```: mount config folder to docker container
* ```--config config.json --repeat 30```: the same usage of the main.py app

```
docker run -v $(pwd)/config.json:/config.json -t cloudflare-ddns --config config.json --repeat 30
```

###### with environment variables
* ```-v $(pwd)/config.json:/config.json```: mount config folder to docker container
* ```-e DDNS_CONFIG='config.json' -e DDNS_REPEAT='10'```: the same usage of the main.py app

```
docker run -v $(pwd)/config.json:/config.json -t -e DDNS_CONFIG='config.json' -e DDNS_REPEAT='10' cloudflare-ddns
```
