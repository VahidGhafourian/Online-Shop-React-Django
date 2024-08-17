FROM python:3.11-slim

WORKDIR /app

COPY ./drf/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./drf /app

RUN python manage.py collectstatic --noinput

# Set environment variables for Django superuser creation
ENV DJANGO_SUPERUSER_PHONENUMBER=vahid
ENV DJANGO_SUPERUSER_EMAIL=vahid@example.com
ENV DJANGO_SUPERUSER_PASSWORD=vahid

# Script to create a superuser if it doesn't already exist
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$DJANGO_SUPERUSER_PHONENUMBER', '$DJANGO_SUPERUSER_PASSWORD', '$DJANGO_SUPERUSER_EMAIL',) if not User.objects.filter(phone_number='$DJANGO_SUPERUSER_PHONENUMBER').exists() else print('Superuser already exists.')" | python manage.py shell


RUN cd /app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "OnlineShop.wsgi:application"]
