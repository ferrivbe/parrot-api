.DEFAULT_GOAL := help

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: dev
dev: ## run the project with development tools and configurations
	@docker-compose --file docker-compose.dev.yml run --service-ports --rm backend || true

.PHONY: up
up: ## run the project
	@docker-compose up --build

.PHONY: stop
stop: ## stop Docker containers without removing them
	@docker-compose stop

.PHONY: down
down: ## stop and remove Docker containers
	@docker-compose down --remove-orphans

.PHONY: rebuild
rebuild: ## rebuild base Docker images
	@docker-compose down --remove-orphans
	@docker-compose build --no-cache

.PHONY: reset
reset: ## update Docker images and reset local databases
	@docker-compose down --volumes --remove-orphans
	@docker-compose pull

.PHONY: pull
pull: ## update Docker images without losing local databases
	@docker-compose down --remove-orphans
	@docker-compose pull

.PHONY: fromscratch
fromscratch: reset pull up
