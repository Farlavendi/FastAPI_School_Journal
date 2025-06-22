# This is my project, a prototype of school journal app.

---

## Tech stack:

- Framework: FastAPI
- ORM: SQLAlchemy 2.0
- Database: PostgreSQL
- Migrations: Alembic
- Message broker: RabbitMQ
- Task manager: TaskIQ

---

## Installation and local deploy

Follow these simple steps to deploy locally.

### Clone the repo:

```
git@github.com:Farlavendi/FastAPI_School_Journal.git
```

#### Don't forget to configure environment variables. The required variables can be found in .env.template file.

### Launch Docker containers:

```shell
  docker-compose up -d 
```

### Apply migrations

```shell
  alembic upgrade head
```

### App is available. Follow the link to see docs

```shell
  http://127.0.0.1:8000/
```
