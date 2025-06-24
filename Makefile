.PHONY: up up-build down

up:
	docker compose up -d

up-build:
	docker compose up -d --build

down:
	docker compose down -v

config:
	docker compose config