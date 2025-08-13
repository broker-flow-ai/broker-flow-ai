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
	@echo "make install        - Install dependencies"
	@echo "make dev-install    - Install development dependencies"
	@echo "make run            - Run the application"
	@echo "make run-simulated  - Run the simulated version"
	@echo "make test           - Run all tests"
	@echo "make test-unit      - Run unit tests"
	@echo "make test-cov       - Run tests with coverage"
	@echo "make lint           - Run code linting"
	@echo "make format         - Format code with black"
	@echo "make clean          - Clean temporary files"
	@echo "make docker-build   - Build Docker image"
	@echo "make docker-run     - Run with Docker Compose"
	@echo "make docs           - Generate documentation"
	@echo "make setup          - Initial setup"

# Initial setup
.PHONY: setup
setup:
	$(PIP) install --upgrade pip
	$(MAKE) install
	@echo "Setup complete! Don't forget to:"
	@echo "1. Copy .env.example to .env and configure it"
	@echo "2. Create the database and run schema.sql"
	@echo "3. Install Tesseract OCR if processing scanned PDFs"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements.txt

# Install development dependencies
.PHONY: dev-install
dev-install:
	$(PIP) install -r requirements-dev.txt

# Run the application
.PHONY: run
run:
	$(PYTHON) main.py

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

# Generate documentation
.PHONY: docs
docs:
	@echo "Generating documentation..."
	@echo "Documentation is in Markdown format in the root directory"