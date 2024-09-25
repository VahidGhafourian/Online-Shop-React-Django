FROM python:3.11-slim

WORKDIR /app

COPY ./drf/requirements.txt .

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    python3-dev \
    netcat-traditional && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt&& \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./entrypoint.sh .
RUN chmod +x /app/entrypoint.sh

COPY ./drf .

ENTRYPOINT ["/app/entrypoint.sh"]
