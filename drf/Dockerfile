FROM python:3.11-slim

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt

COPY ./ /app

RUN cd /app
