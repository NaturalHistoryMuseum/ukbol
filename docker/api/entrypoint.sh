#!/bin/sh

echo "Wait for PostgreSQL to start..."
while ! pg_isready -h db -U ckan; do
    sleep 1;
done
echo "PostgreSQL started"

if [ "${RUN_MIGRATE}" == "TRUE" ]
then
  echo "Running migrate"
  ukbol db upgrade
fi

exec "$@"
