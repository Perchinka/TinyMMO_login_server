.DEFAULT_GOAL := help

.PHONY: help install run test docker-build docker-up docker-down logs clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dependencies via Poetry
	poetry install

run: ## Run the application (demo CLI)
	docker-compose up -d --build

test: ## Run the full test suite with pytest
	poetry run pytest --maxfail=1 --disable-warnings -q

logs: ## Tail Docker Compose logs
	docker-compose logs -f

clean: ## Remove Python cache files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

