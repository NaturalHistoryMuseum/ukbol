#!/bin/bash

# make sure the db is up
docker compose up -d db

# set the env vars
set -o allexport
source ./test.env
set +o allexport

# run the tests
pytest --cov=ukbol tests
