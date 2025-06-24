# Fastapi-school-journal

---

## Description

This is my project, a prototype of a student journal and gradebook app, similar to a Student Information System (SIS) or
Online School Diary.

---

## Tech stack:

- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0
- **Database:** PostgreSQL
- **Migrations:** Alembic
- **Message-broker:** RabbitMQ
- **Task manager:** TaskIQ

---

## Installation and deployment.

Follow these steps to set up the application.

### 1. Clone the repository:

```shell
  git clone git@github.com:Farlavendi/FastAPI_School_Journal.git
```

> [!IMPORTANT]
> Configure environment variables. The required variables can be found in .env.template file.

### 2. Generate openssl private and public keys:

```shell
  openssl genpkey -algorithm RSA -out src/certs/private.pem -pkeyopt rsa_keygen_bits:2048
```

```shell
  openssl rsa -pubout -in src/certs/private.pem -out certs/public.pem
```

> [!NOTE]
> These keys are required for JWT auth.

### 3. Launch Docker containers:

```shell
  docker-compose up -d 
```

> [!TIP]
> You can also you Makefile commands. In this case you can just use "make up".

### 4. Apply migrations

```shell
  docker compose exec fastapi alembic upgrade head
```

### 5. 🔗 Available links:

- http://localhost:8000/docs - Swagger UI
- http://localhost:8000/redoc - ReDoc
- http://localhost:8080/ - Maildev
- http://localhost:15672/ - RabbitMQ 
