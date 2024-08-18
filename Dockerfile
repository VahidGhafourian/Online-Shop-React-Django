FROM python:3.11-slim

WORKDIR /app

COPY ./drf/requirements.txt /app/requirements.txt
COPY ./.env /.env

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./drf /app

RUN python manage.py collectstatic --noinput

RUN cd /app
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "OnlineShop.wsgi:application"]
