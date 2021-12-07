FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # compiler for Python C modules
    g++ make libc6-dev

WORKDIR /code
COPY /src/backend /code/backend
COPY /.docker /code/.docker
COPY /requirements.txt /code

RUN python3.9 -m pip install -r /code/requirements.txt

EXPOSE 8000

COPY /.docker/dev /usr/local/bin/

RUN chmod +x .docker/docker-entrypoint.sh
ENTRYPOINT [".docker/docker-entrypoint.sh"]