FROM python:3.11-slim

COPY ./drf/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt

COPY ./drf /app

RUN cd /app
