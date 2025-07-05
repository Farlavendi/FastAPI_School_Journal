.PHONY: up up-build down restart config upgrade

up:
	docker compose up -d

up-build:
	docker compose up -d --build

down:
	docker compose down -v

restart: down up

restart-build: down up-build

config:
	docker compose config

upgrade:
	alembic upgrade head
