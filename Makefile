.PHONY: help up down build logs ps clean test

help:
	@echo "PhD Progress Tracker - Docker Commands"
	@echo "======================================"
	@echo "make up          - Start all services"
	@echo "make up-dev      - Start all services in development mode"
	@echo "make down        - Stop all services"
	@echo "make build       - Build all Docker images"
	@echo "make logs        - View logs from all services"
	@echo "make ps          - Show running containers"
	@echo "make clean       - Remove all containers and volumes"
	@echo "make test        - Run all tests"

up:
	docker-compose up -d

up-dev:
	docker-compose -f docker-compose.dev.yml up

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

ps:
	docker-compose ps

clean:
	docker-compose down -v
	docker system prune -f

test:
	docker-compose exec backend pytest
	docker-compose exec frontend-dev npm test