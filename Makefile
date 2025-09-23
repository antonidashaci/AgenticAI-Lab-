# AgenticAI Lab Makefile
# Build and deployment commands

.PHONY: help setup dev build test clean docker-up docker-down lint format security

# Default target
help: ## Show this help message
	@echo "AgenticAI Lab - Available Commands:"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "\033[36m%-20s\033[0m %s\n", "Command", "Description"} /^[a-zA-Z_-]+:.*?##/ { printf "\033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)

##@ Setup Commands
setup: ## Initial project setup
	@echo "🚀 Setting up AgenticAI Lab..."
	@echo "📦 Installing Node.js dependencies..."
	pnpm install
	@echo "🐍 Installing Python dependencies..."
	poetry install
	@echo "🐳 Starting Docker services..."
	docker-compose up -d
	@echo "⏳ Waiting for services to be ready..."
	sleep 30
	@echo "🗄️ Running database migrations..."
	$(MAKE) db-migrate
	@echo "✅ Setup complete! Run 'make dev' to start development."

install: ## Install dependencies only
	pnpm install
	poetry install

##@ Development Commands
dev: ## Start development servers
	@echo "🔥 Starting development environment..."
	pnpm run dev

dev-api: ## Start only API server
	cd api && poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev-web: ## Start only web server
	cd web && pnpm run dev

dev-worker: ## Start only worker
	cd workflows && poetry run python -m temporalio.worker --task-queue agenticai-tasks

##@ Build Commands
build: ## Build all applications
	@echo "🏗️ Building applications..."
	pnpm run build

build-web: ## Build web application
	cd web && pnpm run build

build-api: ## Build API application
	cd api && poetry build

##@ Docker Commands
docker-up: ## Start all Docker services
	@echo "🐳 Starting Docker services..."
	docker-compose up -d

docker-down: ## Stop all Docker services
	@echo "🛑 Stopping Docker services..."
	docker-compose down

docker-logs: ## Show Docker logs
	docker-compose logs -f

docker-build: ## Build Docker images
	docker-compose build

docker-reset: ## Reset Docker environment
	docker-compose down -v
	docker-compose up -d
	sleep 30
	$(MAKE) db-migrate

##@ Database Commands
db-migrate: ## Run database migrations
	@echo "🗄️ Running database migrations..."
	cd api && poetry run alembic upgrade head

db-migration: ## Create new database migration
	@echo "📝 Creating new migration..."
	cd api && poetry run alembic revision --autogenerate

db-reset: ## Reset database
	@echo "🔄 Resetting database..."
	cd api && poetry run alembic downgrade base && poetry run alembic upgrade head

db-seed: ## Seed database with sample data
	@echo "🌱 Seeding database..."
	cd api && poetry run python scripts/seed_data.py

##@ Testing Commands
test: ## Run all tests
	@echo "🧪 Running all tests..."
	pnpm run test

test-api: ## Run API tests
	poetry run pytest -v

test-web: ## Run web tests
	cd web && pnpm run test

test-coverage: ## Run tests with coverage
	poetry run pytest --cov=agenticai --cov-report=html --cov-report=term

test-integration: ## Run integration tests
	poetry run pytest tests/integration/ -v

##@ Code Quality Commands
lint: ## Run linting
	@echo "🔍 Running linters..."
	pnpm run lint

lint-fix: ## Fix linting issues
	@echo "🔧 Fixing linting issues..."
	cd web && pnpm run lint:fix
	poetry run black .
	poetry run isort .

format: ## Format code
	@echo "✨ Formatting code..."
	pnpm run format

typecheck: ## Run type checking
	@echo "🔎 Running type checks..."
	cd web && pnpm run typecheck
	poetry run mypy .

##@ Security Commands
security: ## Run security checks
	@echo "🔒 Running security checks..."
	pnpm run security

security-api: ## Run API security checks
	poetry run safety check
	poetry run bandit -r .

security-web: ## Run web security checks
	cd web && pnpm audit

##@ AI Model Commands
models-download: ## Download AI models
	@echo "🤖 Downloading AI models..."
	./scripts/download-models.sh

models-update: ## Update AI models
	@echo "🔄 Updating AI models..."
	./scripts/update-models.sh

ollama-setup: ## Setup Ollama models
	@echo "🦙 Setting up Ollama models..."
	./scripts/setup-ollama.sh

##@ Deployment Commands
deploy-staging: ## Deploy to staging
	@echo "🚀 Deploying to staging..."
	./scripts/deploy-staging.sh

deploy-production: ## Deploy to production
	@echo "🚀 Deploying to production..."
	./scripts/deploy-production.sh

##@ Monitoring Commands
logs: ## Show application logs
	docker-compose logs -f

logs-api: ## Show API logs
	docker-compose logs -f agenticai_api

logs-web: ## Show web logs
	docker-compose logs -f agenticai_web

logs-worker: ## Show worker logs
	docker-compose logs -f agenticai_worker

monitor: ## Open monitoring dashboard
	@echo "📊 Opening monitoring dashboard..."
	@echo "Grafana: http://localhost:3000 (admin/agenticai_admin_123)"
	@echo "Prometheus: http://localhost:9090"
	@echo "RabbitMQ: http://localhost:15672 (agenticai_user/agenticai_password)"

##@ Utility Commands
clean: ## Clean build artifacts and dependencies
	@echo "🧹 Cleaning up..."
	pnpm run clean
	poetry cache clear --all pypi
	docker system prune -f

clean-all: ## Clean everything including Docker volumes
	@echo "🧹 Deep cleaning..."
	$(MAKE) clean
	docker-compose down -v
	docker system prune -a -f --volumes

backup: ## Backup data
	@echo "💾 Creating backup..."
	./scripts/backup.sh

restore: ## Restore data from backup
	@echo "📥 Restoring from backup..."
	./scripts/restore.sh

health: ## Check system health
	@echo "🏥 Checking system health..."
	./scripts/health-check.sh

##@ Documentation Commands
docs-dev: ## Start documentation development server
	cd docs && pnpm run dev

docs-build: ## Build documentation
	cd docs && pnpm run build

docs-deploy: ## Deploy documentation
	cd docs && pnpm run deploy

##@ Environment Commands
env-check: ## Check environment setup
	@echo "🔍 Checking environment..."
	@echo "Node.js version: $$(node --version)"
	@echo "Python version: $$(python --version)"
	@echo "Poetry version: $$(poetry --version)"
	@echo "Docker version: $$(docker --version)"
	@echo "Docker Compose version: $$(docker-compose --version)"

env-setup: ## Setup environment variables
	@echo "⚙️ Setting up environment variables..."
	cp .env.example .env.local
	@echo "✅ Please edit .env.local with your configuration"

##@ Git Commands
git-setup: ## Setup git hooks
	@echo "🔧 Setting up git hooks..."
	poetry run pre-commit install
	@echo "✅ Git hooks installed"

commit: ## Interactive commit with conventional commits
	@echo "📝 Creating conventional commit..."
	pnpm run commit

##@ Performance Commands
benchmark: ## Run performance benchmarks
	@echo "⚡ Running benchmarks..."
	./scripts/benchmark.sh

load-test: ## Run load tests
	@echo "🔥 Running load tests..."
	./scripts/load-test.sh

profile: ## Profile application performance
	@echo "📊 Profiling application..."
	./scripts/profile.sh

# Colors for output
RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[0;33m
BLUE=\033[0;34m
NC=\033[0m # No Color
