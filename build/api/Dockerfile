FROM python:3.12.9-slim

RUN apt update && \
    apt install -y libpq-dev && \
    apt -q clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /api

COPY api/pyproject.toml .
COPY api/tests tests
COPY api/migrations migrations
COPY api/ukbol ukbol
RUN pip install .

CMD ["ukbol", "run", "--host", "0.0.0.0", "--port", "5000"]
