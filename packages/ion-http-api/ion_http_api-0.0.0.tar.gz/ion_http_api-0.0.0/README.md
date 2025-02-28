![splash_http_api](https://user-images.githubusercontent.com/1449561/154847286-989a6c51-1615-45e1-b40f-aec7c13014fa.png)

# HTTP API for [Ice Open Network](https://ion.org)

Since ION nodes uses its own ADNL binary transport protocol, a intermediate service is needed for an HTTP connection.

ION HTTP API is such a intermediate service, receiving requests via HTTP, it accesses the lite servers of the ION network using `tonlibjson`.

You can use the ready-made [ice-blockchain.com](https://ice-blockchain.com) service or start your own instance.

## Building and running

Recommended hardware: 
- CPU architecture: x86_64 or arm64.
- HTTP API only: 1 vCPU, 2 GB RAM.
- HTTP API with cache enabled: 2 vCPUs, 4 GB RAM.

There are two main ways to run ION HTTP API:
- __Local__ *(experimental)*: works on following platforms: Ubuntu Linux (x86_64, arm64), MacOSX (Intel x86_64, Apple M1 arm64) and Windows (x86_64). 
- __Docker Compose__: flexible configuration, recommended for production environments, works on any x86_64 and arm64 OS with Docker available.

### Local run *(experimental)*
**Note:** It is simple but not stable way to run the service. We do not recommend to use it in production.    
  - (Windows only, first time) Install OpenSSL v1.1.1 for win64 from [here](https://slproweb.com/products/Win32OpenSSL.html).
  - Install package: `pip install ion-http-api`.
  - Run service with `ion-http-api`. This command will run service with [mainnet](https://cdn.ice.io/mainnet/global.config.json) configuration.
    - Run `ion-http-api --help` to show parameters list.

### Docker Compose
  - (First time) Install required tools: `docker`, `docker-compose`, `curl`. 
    - For Ubuntu: run `scripts/setup.sh` from the root of the repo.
    - For MacOS and Windows: install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
    - **Note:** we recommend to use Docker Compose V2.
  - Download ION configuration files to private folder:
    ```bash
    mkdir private
    curl -sL https://cdn.ice.io/mainnet/global.config.json > private/mainnet.json
    curl -sL https://cdn.ice.io/testnet/testnet-global.config.json > private/testnet.json
    ```
  - Run `./configure.py` to create `.env` file with necessary environment variables (see [Configuration](#Configuration) for details).
  - Build services: `docker-compose build`.
    - Or pull latest images: `docker-compose pull`.
  - Run services: `docker-compose up -d`.
  - Stop services: `docker-compose down`.

### Configuration

You should specify environment parameters and run `./configure.py` to create `.env` file.
    ```bash
    export ION_API_LITESERVER_CONFIG=private/testnet.json
    ./configure.py
    ```

The service supports the following environment variables:
#### Webserver settings
- `ION_API_HTTP_PORT` *(default: 80)*

  Port for HTTP connections of API service.

- `ION_API_ROOT_PATH` *(default: /)*

  If you use a proxy server such as Nginx or Traefik you might change the default API path prefix (e.g. `/api/v2`). If so you have to pass the path prefix to the API service in this variable.

- `ION_API_WEBSERVERS_WORKERS` *(default: 1)*

  Number of webserver processes. If your server is under high load try increase this value to increase RPS. We recommend setting it to number of CPU cores / 2.

- `ION_API_GET_METHODS_ENABLED` *(default: 1)*

  Enables `runGetMethod` endpoint.

- `ION_API_JSON_RPC_ENABLED` *(default: 1)*

  Enables `jsonRPC` endpoint.

- `ION_API_LOGS_JSONIFY` *(default: 0)*

  Enables printing all logs in json format.

- `ION_API_LOGS_LEVEL` *(default: ERROR)*

  Defines log verbosity level. Values allowed: `DEBUG`,`INFO`,`WARNING`,`ERROR`,`CRITICAL`.

- `ION_API_GUNICORN_FLAGS` *(default: empty)*

  Additional Gunicorn [command line arguments](https://docs.gunicorn.org/en/stable/settings.html).

#### Tonlib settings
- `ION_API_TONLIB_LITESERVER_CONFIG` *(default docker: private/mainnet.json local: https://cdn.ice.io/mainnet/global.config.json)*

  Path to config file with lite servers information. In case of native run you can pass URL to download config. Docker support only path to file.

- `ION_API_TONLIB_KEYSTORE` *(default docker: /tmp/ion_keystore local: ./ion_keystore/)*
  
  Path to tonlib keystore.

- `ION_API_TONLIB_PARALLEL_REQUESTS_PER_LITESERVER` *(default: 50)*

  Number of maximum parallel requests count per worker.

- `ION_API_TONLIB_CDLL_PATH` *(default: empty)*

  Path to tonlibjson binary. It could be useful if you want to run service on unsupported platform and have built the `libtonlibjson` library manually.

- `ION_API_TONLIB_REQUEST_TIMEOUT` *(default: 10)*

  Timeout for liteserver requests.

#### Cache configuration
- `ION_API_CACHE_ENABLED` *(default: 0)*

  Enables caching lite server responses with Redis.

- `ION_API_CACHE_REDIS_ENDPOINT` *(default: localhost, docker: cache_redis)*

  Redis cache service host.

- `ION_API_CACHE_REDIS_PORT` *(default: 6379)*

  Redis cache service port.

- `ION_API_CACHE_REDIS_TIMEOUT` *(default: 1)*

  Redis cache service port.


## FAQ
#### How to point the service to my own lite server?

To point the HTTP API to your own lite server you should set `ION_API_TONLIB_LITESERVER_CONFIG` to config file with your only lite server.

- If you use MyIonCtrl on your node you can generate config file with these commands: 
    ```
    $ myionctrl
    MyIonCtrl> installer
    MyIonInstaller> clcf
    ```
    Config file will be saved at `/usr/bin/ion/local.config.json`.
- If you don't use MyIonCtrl: copy `private/mainnet.json` and overwrite section `liteservers` with your liteservers ip, port and public key. To get public key from `liteserver.pub` file use the following script:
    ```
    python -c 'import codecs; f=open("liteserver.pub", "rb+"); pub=f.read()[4:]; print(str(codecs.encode(pub,"base64")).replace("\n",""))'
    ```
- Once config file is created assign variable `ION_API_TONLIB_LITESERVER_CONFIG` to its path, run `./configure.py` and rebuild the project.

#### How to run multiple API instances on single machine?

- Clone the repo as many times as many instances you need to the folders with different names (otherwise docker compose containers will conflict). 
- Configure each instance to use unique port (env variable `ION_API_HTTP_PORT`)
- Build and run every instance.

#### How to update tonlibjson library?

Binary file `libtonlibjson` now moved to [pytonlib](https://github.com/ice-blockchain/pytonlib). 
- Docker Compose: `docker-compose build --no-cache`.
- Local run: `pip install -U ion-http-api`.
