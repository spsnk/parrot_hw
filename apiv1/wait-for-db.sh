#!/bin/sh

while ! nc -z db 5432 ; do
    >&2 echo "Waiting for PostgreSQL Server..."
    sleep 1
done

>&2 echo "Postgres is up - starting server"
>&2 echo "> $@"
exec "$@"
