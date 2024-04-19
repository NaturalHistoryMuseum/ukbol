FROM python:3.12-alpine

RUN apk add --no-cache gcc musl-dev linux-headers postgresql

# setup entrypoint
COPY ./docker/api/entrypoint.sh /deploy/entrypoint.sh

# setup the api app
WORKDIR /app/api
COPY ./api .
RUN pip install -e .

ENTRYPOINT ["/bin/sh", "/deploy/entrypoint.sh"]
CMD ["ukbol", "run", "--host", "0.0.0.0", "--port", "5000"]
