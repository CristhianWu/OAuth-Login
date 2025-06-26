# OAuth-Login

Welcome to the OAuth Backend using SuperTokens (Self-hosted)

This project is a Django-based backend which provides secure authentication using SuperTokens (self-hosted) with the 'emailPassword' recipe and email verification.

Features
- Self-hosted SuperTokens integration
- EmailPassword authentication
- Email verification
- JWT-based session handling
- Development setup using Docker
- API ready for frontend integration

Technology Stack
- Backend: [Django, Django Rest Framework]
- Database: [PostgreSQL]
- OAuth: SuperTokens (self-hosted)
- Containerization: Docker


Getting Started

After cloning the repository, open terminal and be sure that you are on the same directory as the docker-compose.yaml. Make sure docker daemon is running too. Then, use the following command

> docker compose up -d --build

After that enter the backend container and make migaations with the following command:

> docker exec -it django_myapp bash
> python manage.py migrate

For email verification, check on the "custom_email" directory.

In the supertokens_config.py, you can find the needed configuration for integrating the email delivery.

There is also a view that allows you to verify the email manually.
For testing purposes, this is how the api works

# Register Endpoint (POST)
http://localhost:8000/register/
{
  "name": "YOUR_NAME",
  "last_name": "YOUR_LAST_NAME",
  "email": "YOUR_EMAIL",
  "password": "YOUR_PASSWORD",
  "id_document": "YOUR_ID",
  "role": "YOUR ROLE" (user, employee,admin)
}

# Login Endpoint
http://localhost:8000/login/
{
  "email": "YOUR_EMAIL",
  "password": "YOUR_PASSWORD"
}

# Logout Endpoint
Authorization: Bearer ['ACCESS_TOKEN']

# Verify email manually Endpoint
{
    "user_id": "USER_ID"
}