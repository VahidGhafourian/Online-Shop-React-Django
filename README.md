# Django Ecommerce API

An E-commerce API built using Django Rest Framework. [Github repository](https://github.com/VahidGhafourian/Online-Shop-React-Django) | [API Documentation](https://github.com/VahidGhafourian/Online-Shop-React-Django/blob/main/API%20Documents.md)

## Basic Features

- Registration using phone number
- Basic E-commerce features.
- Custom permissions set for necessary endpoints.
- Payment integration using Zarinpal.
- Documentation using swagger
- Dockerized for local development and production
- Deploy on VPS using Github actions CI/CD pipline

## Technologies Used

- Django Rest Framework
- PostgreSQL
- Nginx
- Docker
- Zarinpal

## DataBase ER Diagram

Here is the Entity-Relationship diagram generated using https://dbdiagram.io/
![ER-Diagram](https://raw.githubusercontent.com/VahidGhafourian/Online-Shop-React-Django/refs/heads/main/ER-Diagram-Online-Shop.png)

## Getting Started

Clone this repository to your local machine and rename the `.env.example` file found in the root directory of the project to `.env` and update the environment variables accordingly.

Create external volume with docker named `shop`.

```
$ docker-compose up
```

Navigate to http://localhost:8000/admin/
---
More information about API usage can be found [here](https://github.com/VahidGhafourian/Online-Shop-React-Django/blob/main/API%20Documents.md).