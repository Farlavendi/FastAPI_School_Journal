# This is my project, a prototype of school journal app.

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

### 2. Launch Docker containers:

```shell
docker-compose up -d 
```

### 3. Apply migrations

```shell
alembic upgrade head
```

### 4. Access the application.

```shell
http://127.0.0.1:8000/
```

> [!NOTE]
> You will be automaticly redirected to docs page.
