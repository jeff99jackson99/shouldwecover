.PHONY: help setup install test lint fmt clean run docker-build docker-run docker-stop

# Default target
help:
	@echo "Insurance Claim Coverage Analyzer - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  setup      - Install dependencies and setup environment"
	@echo "  install    - Install Python dependencies"
	@echo "  run        - Run the Streamlit application locally"
	@echo "  test       - Run tests with pytest"
	@echo "  lint       - Run linting with ruff"
	@echo "  fmt        - Format code with black"
	@echo "  clean      - Clean up cache and temporary files"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run Docker container"
	@echo "  docker-stop  - Stop Docker container"
	@echo ""
	@echo "Deployment:"
	@echo "  deploy     - Deploy to production (placeholder)"
	@echo "  logs       - View application logs"

# Setup development environment
setup: install
	@echo "Setting up development environment..."
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		cp .env.example .env; \
		echo "Please update .env with your OpenAI API key"; \
	fi
	@echo "Development environment setup complete!"

# Install Python dependencies
install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "Dependencies installed successfully!"

# Run the application locally
run:
	@echo "Starting Insurance Claim Analyzer..."
	streamlit run src/app/main.py

# Run tests
test:
	@echo "Running tests..."
	pytest tests/ -v --cov=src/ --cov-report=html
	@echo "Tests completed!"

# Run linting
lint:
	@echo "Running linting checks..."
	ruff check src/ tests/
	@echo "Linting completed!"

# Format code
fmt:
	@echo "Formatting code..."
	black src/ tests/
	ruff check --fix src/ tests/
	@echo "Code formatting completed!"

# Clean up cache and temporary files
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.pyd" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.log" -delete 2>/dev/null || true
	@echo "Cleanup completed!"

# Docker commands
docker-build:
	@echo "Building Docker image..."
	docker build -t insurance-claim-analyzer .
	@echo "Docker image built successfully!"

docker-run:
	@echo "Starting Docker container..."
	docker run -d --name insurance-analyzer \
		-p 8501:8501 \
		-e OPENAI_API_KEY=$${OPENAI_API_KEY} \
		insurance-claim-analyzer
	@echo "Container started! Access at http://localhost:8501"

docker-stop:
	@echo "Stopping Docker container..."
	docker stop insurance-analyzer || true
	docker rm insurance-analyzer || true
	@echo "Container stopped and removed!"

# Docker compose commands
docker-compose-up:
	@echo "Starting services with Docker Compose..."
	docker-compose up -d
	@echo "Services started! Access at http://localhost:8501"

docker-compose-down:
	@echo "Stopping services with Docker Compose..."
	docker-compose down
	@echo "Services stopped!"

docker-compose-logs:
	@echo "Viewing Docker Compose logs..."
	docker-compose logs -f

# Development utilities
check-deps:
	@echo "Checking for outdated dependencies..."
	pip list --outdated

update-deps:
	@echo "Updating dependencies..."
	pip install --upgrade -r requirements.txt

# Security checks
security-check:
	@echo "Running security checks..."
	safety check
	bandit -r src/

# Performance testing
benchmark:
	@echo "Running performance benchmarks..."
	python -m pytest tests/test_performance.py -v

# Documentation
docs:
	@echo "Generating documentation..."
	pdoc --html src/ --output-dir docs/
	@echo "Documentation generated in docs/ folder"

# Backup
backup:
	@echo "Creating backup..."
	tar -czf backup_$(shell date +%Y%m%d_%H%M%S).tar.gz \
		--exclude='.git' \
		--exclude='__pycache__' \
		--exclude='*.pyc' \
		--exclude='.env' \
		.
	@echo "Backup created!"

# Production deployment (placeholder)
deploy:
	@echo "Production deployment not configured yet."
	@echo "Please configure your deployment pipeline."

# View logs
logs:
	@echo "Viewing application logs..."
	tail -f app.log

# Quick development cycle
dev: fmt lint test run

# Full development setup
full-setup: setup fmt lint test
	@echo "Full development setup completed!"
	@echo "Run 'make run' to start the application"
