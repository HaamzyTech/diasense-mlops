.PHONY: up down build lint format test

up:
	docker compose up -d --build

down:
	docker compose down -v

build:
	docker compose build

lint:
	@echo "TODO: add lint targets"

format:
	@echo "TODO: add format targets"

test:
	@echo "TODO: add test targets"
