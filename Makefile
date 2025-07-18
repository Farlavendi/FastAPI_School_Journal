.PHONY: up up-build down watch restart restart-build config upgrade taskiq

up:
	docker compose up -d

up-build:
	docker compose up -d --build

down:
	docker compose down -v

watch:
	docker compose up --watch

restart: down up

restart-build: down up-build

config:
	docker compose config

upgrade:
	alembic upgrade head

taskiq:
	taskiq worker src.core.taskiq:broker --no-configure-logging --fs-discover --tasks-pattern "**src/tasks"
