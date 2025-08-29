# BrokerFlow AI - Makefile

# Variables
PYTHON = python3
PIP = pip3
TEST_DIR = tests
SRC_DIR = modules

# Default target
.PHONY: help
help:
	@echo "BrokerFlow AI - Makefile Commands"
	@echo "================================="
	@echo "make install           - Install dependencies"
	@echo "make dev-install       - Install development dependencies"
	@echo "make run-processor     - Run document processor"
	@echo "make run-api           - Run API server"
	@echo "make run-frontend      - Run frontend dashboard"
	@echo "make run-simulated     - Run the simulated version"
	@echo "make test              - Run all tests"
	@echo "make test-unit         - Run unit tests"
	@echo "make test-cov          - Run tests with coverage"
	@echo "make test-api          - Test API endpoints"
	@echo "make lint              - Run code linting"
	@echo "make format            - Format code with black"
	@echo "make clean             - Clean temporary files"
	@echo "make docker-build      - Build Docker image"
	@echo "make docker-run        - Run with Docker Compose"
	@echo "make docker-run-api    - Run only API service"
	@echo "make docker-run-frontend - Run only frontend service"
	@echo "make docker-logs       - View Docker logs"
	@echo "make docker-stop       - Stop Docker services"
	@echo "make docs              - Generate documentation"
	@echo "make setup             - Initial setup"

# Initial setup
.PHONY: setup
setup:
	$(PIP) install --upgrade pip
	$(MAKE) install
	@echo "Setup complete! Don't forget to:"
	@echo "1. Copy .env.example to .env and configure it"
	@echo "2. Create the database and run schema.sql"
	@echo "3. Install Tesseract OCR if processing scanned PDFs"
	@echo "4. Run 'make init-auth' to initialize authentication system"

# Initialize authentication system
.PHONY: init-auth
init-auth:
	$(PYTHON) init_complete_auth.py

# Initialize auth tables only
.PHONY: init-auth-tables
init-auth-tables:
	$(PYTHON) init_auth_tables.py

# Populate permissions and roles
.PHONY: populate-permissions
populate-permissions:
	$(PYTHON) populate_permissions.py

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements.txt

# Install development dependencies
.PHONY: dev-install
dev-install:
	$(PIP) install -r requirements-dev.txt

# Run document processor
.PHONY: run-processor
run-processor:
	$(PYTHON) main.py

# Run API server
.PHONY: run-api
run-api:
	uvicorn api_b2b:app --reload

# Run frontend dashboard
.PHONY: run-frontend
run-frontend:
	streamlit run frontend/dashboard.py

# Run the simulated version
.PHONY: run-simulated
run-simulated:
	$(PYTHON) main_simulated.py

# Run all tests
.PHONY: test
test:
	$(PYTHON) -m pytest $(TEST_DIR) -v

# Run unit tests
.PHONY: test-unit
test-unit:
	$(PYTHON) -m pytest $(TEST_DIR)/test_*.py -v

# Run tests with coverage
.PHONY: test-cov
test-cov:
	$(PYTHON) -m pytest $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=html --cov-report=term

# Test API endpoints
.PHONY: test-api
test-api:
	curl -f http://localhost:8000/api/v1/health || echo "API not running"

# Run code linting
.PHONY: lint
lint:
	flake8 $(SRC_DIR) --max-line-length=88
	black --check $(SRC_DIR)
	isort --check-only $(SRC_DIR)

# Format code
.PHONY: format
format:
	black $(SRC_DIR)
	isort $(SRC_DIR)

# Clean temporary files
.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf logs/*.log

# Build Docker image
.PHONY: docker-build
docker-build:
	docker build -t brokerflow-ai .

# Run with Docker Compose
.PHONY: docker-run
docker-run:
	docker-compose up -d

# Run only API service
.PHONY: docker-run-api
docker-run-api:
	docker-compose up -d api

# Run only frontend service
.PHONY: docker-run-frontend
docker-run-frontend:
	docker-compose up -d frontend

# View Docker logs
.PHONY: docker-logs
docker-logs:
	docker-compose logs

# Stop Docker services
.PHONY: docker-stop
docker-stop:
	docker-compose down

# Generate documentation
.PHONY: docs
docs:
	@echo "Generating documentation..."
	@echo "Documentation is in Markdown format in the root directory"