# Makefile for TinyMMO Login Server

.DEFAULT_GOAL := help

.PHONY: help install run test docker-build docker-up docker-down logs clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dependencies via Poetry
	poetry install

run: ## Run the application (demo CLI)
	poetry run python -m login_server

test: ## Run the full test suite with pytest
	poetry run pytest --maxfail=1 --disable-warnings -q

docker-build: ## Build Docker images
	docker-compose build

docker-up: ## Start services with Docker Compose
	docker-compose up -d

docker-down: ## Stop services and remove containers
	docker-compose down

logs: ## Tail Docker Compose logs
	docker-compose logs -f

clean: ## Remove Python cache files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

