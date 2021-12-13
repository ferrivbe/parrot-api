#!/usr/bin/env bash

cd /code/backend

# image can run in multiple modes
if [[ "${1}" == "shell" ]]; then
    exec /bin/bash
elif [[ "${1}" == "migrate-noinput" ]]; then
    exec python3.9 manage.py migrate --noinput
elif [[ "${1}" == "collectstatic" ]]; then
    exec python3.9 manage.py collectstatic --noinput
elif [[ "${1}" == "runserver" ]]; then
    exec python3.9 manage.py collectstatic --noinput --clear\
        & python3.9 manage.py makemigrations \
        & python3.9 manage.py migrate \
        & gunicorn --config=gunicorn_config.py backend.wsgi:application
elif [[ "${1}" == "migrate" ]]; then
    exec pipenv run python3.9 manage.py migrate
elif [[ "${1}" == "makemigrations" ]]; then
    exec python3.9 manage.py makemigrations
else
    exec gunicorn --config=gunicorn_config.py server.wsgi
fi