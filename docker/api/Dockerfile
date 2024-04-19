FROM python:3.12-alpine

RUN apk add --no-cache gcc musl-dev linux-headers postgresql

# setup the api app
WORKDIR /app/api
COPY api/pyproject.toml pyproject.toml
RUN pip install -e .
COPY api/ .

# todo: setup the web app

# setup entrypoint
COPY ./docker/api/entrypoint.sh /deploy/entrypoint.sh
ENTRYPOINT ["/bin/sh", "/deploy/entrypoint.sh"]

CMD ["python", "-m", "ukbol.app"]
