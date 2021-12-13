## parrot-api
Backend REST API project for parrot challenge, coded in Django,
documented in Swagger, Redoc and deployed in AWS via CodeDeploy.

For API documentation refer to [usage](https://github.com/ferrivbe/parrot-api/blob/dev/doc/usage.md)

### Running the production environment

* `make up`

### Creating superuser for manual testing
Superusers can create other users with role 2 (user).

* `make dev`
* `dev su`

### Running the testing environment

* `make dev`
* `dev test`
* `dev cov` For test coverage.

### Running the development environment

* `make dev`
* `dev up`

##### Rebuilding the base Docker image

* `make rebuild`

##### Resetting the local database

* `make reset`

### Hostnames for accessing the development service directly

* Local: http://127.0.0.1:8000

### Hostnames for accessing the local production service directly

* Local: http://127.0.0.1

### Recomended environment schema

For testing purposes, we provide an example of enviroment variables.
```
DEBUG=True
APP_LOGGING_LEVEL=WARN
DB_LOGGING_LEVEL=WARN
PYTHONDONTWRITEBYTECODE=1

POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOSTNAME=postgres
```


### About building local environment with Linux systems

If you bring up the local environment in a linux system, maybe you can get some problems about users permissions when working with Docker.
So we give you a little procedure to avoid problems with users permissions structure in Linux.:

1- Delete containers

```
# or docker rm -f $(docker ps -aq) if you don't use docker beyond the test
make down
```

2- Give permissions to your system users to use Docker

```
## Where ${USER} is your current user
sudo usermod -aG docker ${USER}
```

3- Confirm current user is in docker group

```
## If you don't see docker in the list, then you possibly need to log off and log in again in your computer.
id -nG
```


4-  Get the current user id

```
## Commonly your user id number is near to 1000
id -u
```

5- Replace user id in Dockerfiles by your current user id

Edit `.docker/Dockerfile_base` and replace 1337 by your user id.

6- Rebuild the local environment 

```
make rebuild
make up
```
