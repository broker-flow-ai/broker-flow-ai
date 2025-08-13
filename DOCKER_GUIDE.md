# BrokerFlow AI - Docker Guide

## 🐳 Overview

This guide provides comprehensive instructions for using Docker with BrokerFlow AI, covering everything from basic setup to production deployment.

## 📋 Prerequisites

### System Requirements
- Docker Engine 20.10+
- Docker Compose 1.29+
- 4GB+ RAM recommended
- 10GB+ free disk space

### Installation
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose

# macOS
brew install docker docker-compose

# Windows
# Install Docker Desktop from https://www.docker.com/products/docker-desktop
```

### Verification
```bash
docker --version
docker-compose --version
docker info
```

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/yourorganization/brokerflow-ai.git
cd brokerflow-ai
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Build and Run
```bash
docker-compose up -d
```

### 4. Access Services
- Application: http://localhost:8000
- phpMyAdmin: http://localhost:8080
- MySQL: localhost:3306

## 📁 Dockerfile Analysis

### Base Image
```dockerfile
FROM python:3.10-slim
```
- Uses official Python 3.10 slim image for smaller footprint
- Based on Debian for compatibility

### Working Directory
```dockerfile
WORKDIR /app
```
- Sets `/app` as working directory
- All subsequent commands run from this directory

### Environment Variables
```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
```
- Prevents Python from writing bytecode files
- Ensures Python output is not buffered

### System Dependencies
```dockerfile
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
        tesseract-ocr \
        libtesseract-dev \
        poppler-utils \
    && rm -rf /var/lib/apt/lists/*
```
- Installs essential build tools
- MySQL client development headers
- Tesseract OCR engine and libraries
- Poppler utilities for PDF processing
- Cleans up package cache to reduce image size

### Python Dependencies
```dockerfile
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt
```
- Copies both runtime and development requirements
- Installs dependencies without caching to reduce image size

### Application Code
```dockerfile
COPY . .
```
- Copies entire application codebase
- Excludes files specified in `.gitignore`

### Directory Setup
```dockerfile
RUN mkdir -p inbox output templates
```
- Creates necessary directories for file processing

### Port Exposure
```dockerfile
EXPOSE 8000
```
- Exposes port 8000 for API access
- Does not publish port (use docker-compose for that)

### Security
```dockerfile
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser
```
- Creates non-root user for security
- Changes ownership of application files
- Runs container as non-root user

### Startup Command
```dockerfile
CMD ["python", "main.py"]
```
- Default command to run the application

## 🐳 Docker Compose Configuration

### Services Overview
```yaml
version: '3.8'

services:
  brokerflow:    # Main application
  db:           # MySQL database
  phpmyadmin:   # Database management interface
  redis:        # Cache service
```

### 1. Main Application Service
```yaml
brokerflow:
  build: .
  ports:
    - "8000:8000"
  environment:
    - MYSQL_HOST=db
    - MYSQL_USER=brokerflow
    - MYSQL_PASSWORD=brokerflow123
    - MYSQL_DATABASE=brokerflow_ai
    - OPENAI_API_KEY=${OPENAI_API_KEY}
  volumes:
    - ./inbox:/app/inbox
    - ./output:/app/output
    - ./templates:/app/templates
    - ./logs:/app/logs
  depends_on:
    - db
  restart: unless-stopped
```

**Key Configuration:**
- **Build**: Builds from current directory Dockerfile
- **Ports**: Maps host port 8000 to container port 8000
- **Environment**: Sets environment variables for database and API keys
- **Volumes**: Mounts host directories for persistent data
- **Depends On**: Ensures database starts before application
- **Restart**: Automatically restarts unless manually stopped

### 2. Database Service
```yaml
db:
  image: mysql:8.0
  environment:
    - MYSQL_ROOT_PASSWORD=root123
    - MYSQL_USER=brokerflow
    - MYSQL_PASSWORD=brokerflow123
    - MYSQL_DATABASE=brokerflow_ai
  volumes:
    - db_data:/var/lib/mysql
    - ./schema.sql:/docker-entrypoint-initdb.d/schema.sql
  ports:
    - "3306:3306"
  restart: unless-stopped
```

**Key Configuration:**
- **Image**: Official MySQL 8.0 image
- **Environment**: Database credentials and initial setup
- **Volumes**: 
  - `db_data`: Named volume for persistent storage
  - `schema.sql`: Initializes database schema
- **Ports**: Exposes MySQL port for external access

### 3. phpMyAdmin Service
```yaml
phpmyadmin:
  image: phpmyadmin/phpmyadmin
  environment:
    - PMA_HOST=db
    - PMA_USER=root
    - PMA_PASSWORD=root123
  ports:
    - "8080:80"
  depends_on:
    - db
  restart: unless-stopped
```

**Key Configuration:**
- **Image**: Official phpMyAdmin image
- **Environment**: Connects to MySQL database
- **Ports**: Maps host port 8080 to container port 80
- **Depends On**: Ensures database starts first

### 4. Redis Service
```yaml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
  restart: unless-stopped
```

**Key Configuration:**
- **Image**: Lightweight Redis Alpine image
- **Ports**: Exposes Redis port for caching
- **Restart**: Automatic restart policy

### Volumes
```yaml
volumes:
  db_data:
```
- **db_data**: Named volume for persistent database storage

## ⚙️ Environment Configuration

### .env File Structure
```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=brokerflow_ai

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_email_password

# System Configuration
INBOX_PATH=inbox/
OUTPUT_PATH=output/
TEMPLATE_PATH=templates/

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=brokerflow.log

# Security Configuration
SECRET_KEY=your_secret_key_here
JWT_EXPIRATION_DAYS=30
```

### Docker Environment Variables
Variables can be set in multiple ways:

1. **.env file** (recommended for development)
2. **Command line** (for overrides)
3. **Docker Compose** (for service-specific settings)

### Sensitive Data
```bash
# Never commit API keys to version control
# Use .env file and add to .gitignore
echo ".env" >> .gitignore
```

## ▶️ Running Docker Services

### Basic Commands

#### Start All Services
```bash
docker-compose up -d
```
- `-d`: Run in detached mode (background)

#### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f brokerflow

# Last 100 lines
docker-compose logs --tail=100 brokerflow
```

#### Stop Services
```bash
# Stop all services
docker-compose down

# Stop specific service
docker-compose stop brokerflow

# Stop and remove volumes
docker-compose down -v
```

#### Restart Services
```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart db
```

### Service Management

#### View Running Services
```bash
docker-compose ps
```

#### Execute Commands in Container
```bash
# Access container shell
docker-compose exec brokerflow bash

# Run specific command
docker-compose exec brokerflow python main.py

# Access database
docker-compose exec db mysql -u brokerflow -p brokerflow_ai
```

#### Build Images
```bash
# Rebuild all services
docker-compose build

# Rebuild specific service
docker-compose build brokerflow

# Force rebuild without cache
docker-compose build --no-cache brokerflow
```

## 📁 Volume Management

### Volume Types

#### Named Volumes
```yaml
volumes:
  db_data:
```
- Managed by Docker
- Persistent across container restarts
- Located in Docker's storage area

#### Bind Mounts
```yaml
volumes:
  - ./inbox:/app/inbox
  - ./output:/app/output
```
- Maps host directories to container
- Direct access to files from host
- Useful for development

### Volume Commands

#### List Volumes
```bash
docker volume ls
```

#### Inspect Volume
```bash
docker volume inspect brokerflow_ai_db_data
```

#### Remove Volumes
```bash
# Remove specific volume
docker volume rm brokerflow_ai_db_data

# Remove unused volumes
docker volume prune
```

### Data Persistence

#### Backup Database Volume
```bash
# Create backup
docker run --rm \
  -v brokerflow_ai_db_data:/source \
  -v $(pwd):/backup \
  alpine tar czf /backup/db_backup.tar.gz -C /source .
```

#### Restore Database Volume
```bash
# Restore from backup
docker run --rm \
  -v brokerflow_ai_db_data:/target \
  -v $(pwd):/backup \
  alpine tar xzf /backup/db_backup.tar.gz -C /target
```

## 🔧 Configuration and Customization

### Custom Dockerfile
Create `Dockerfile.custom` for specific needs:

```dockerfile
FROM brokerflow/brokerflow-ai:latest

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    additional-package \
    && rm -rf /var/lib/apt/lists/*

# Copy custom configuration
COPY custom-config.yaml /app/config/custom.yaml

# Expose additional ports
EXPOSE 8000 9000

# Custom startup command
CMD ["python", "main.py", "--config", "custom.yaml"]
```

### Environment-Specific Compose Files
Create `docker-compose.prod.yml` for production:

```yaml
version: '3.8'

services:
  brokerflow:
    build: .
    environment:
      - DEBUG=false
      - LOG_LEVEL=WARNING
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
    restart: always

  db:
    environment:
      - MYSQL_ROOT_PASSWORD_FILE=/run/secrets/db_root_password
    secrets:
      - db_root_password

secrets:
  db_root_password:
    file: ./secrets/db_root_password.txt
```

### Override Configuration
```bash
# Use multiple compose files
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 🛠 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check which process is using the port
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml
```

#### 2. Database Connection Issues
```bash
# Check if database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Test database connection
docker-compose exec brokerflow \
  mysql -h db -u brokerflow -p brokerflow_ai -e "SELECT 1;"
```

#### 3. Permission Issues
```bash
# Fix file permissions
sudo chown -R $(id -u):$(id -g) inbox output templates logs

# Or run as root (not recommended for production)
# Remove USER appuser from Dockerfile
```

#### 4. Volume Mount Issues
```bash
# Check volume mounts
docker-compose exec brokerflow ls -la /app

# Verify host directories exist
ls -la inbox output templates
```

### Debugging Commands

#### Container Information
```bash
# Inspect container
docker inspect brokerflow_ai_brokerflow_1

# Check container resources
docker stats brokerflow_ai_brokerflow_1

# View container processes
docker top brokerflow_ai_brokerflow_1
```

#### Network Debugging
```bash
# Check network configuration
docker network ls
docker network inspect brokerflow_ai_default

# Test connectivity between containers
docker-compose exec brokerflow ping db
```

#### Image Debugging
```bash
# View image layers
docker history brokerflow/brokerflow-ai

# Inspect image
docker inspect brokerflow/brokerflow-ai:latest
```

## 📊 Monitoring and Logging

### Docker Logging

#### Configure Logging Driver
```yaml
services:
  brokerflow:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

#### View Logs
```bash
# Real-time logs
docker-compose logs -f

# Filter logs by time
docker-compose logs --since="2025-08-13"

# Filter logs by pattern
docker-compose logs | grep ERROR
```

### Resource Monitoring

#### Container Resources
```bash
# Monitor all containers
docker stats

# Monitor specific container
docker stats brokerflow_ai_brokerflow_1
```

#### System Resources
```bash
# Check Docker daemon stats
docker system df

# View system-wide information
docker info
```

## 🚀 Production Deployment

### Best Practices

#### Security
```yaml
# Production docker-compose.yml
services:
  brokerflow:
    environment:
      - DEBUG=false
      - SECRET_KEY_FILE=/run/secrets/secret_key
    secrets:
      - secret_key
    restart: always
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
```

#### Resource Limits
```yaml
services:
  brokerflow:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M
          cpus: '0.25'
```

#### Health Checks
```yaml
services:
  brokerflow:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Scaling

#### Horizontal Scaling
```bash
# Scale specific service
docker-compose up -d --scale brokerflow=3
```

#### Load Balancing
Use external load balancer like NGINX or HAProxy for production.

### Backup Strategy

#### Automated Backups
```bash
# Create backup script
#!/bin/bash
docker-compose exec db mysqldump -u root -p$MYSQL_ROOT_PASSWORD brokerflow_ai > backup_$(date +%Y%m%d_%H%M%S).sql
```

#### Scheduled Backups
```bash
# Add to crontab
0 2 * * * /path/to/backup_script.sh
```

## 🔒 Security Considerations

### Image Security
```bash
# Scan images for vulnerabilities
docker scan brokerflow/brokerflow-ai

# Use official base images
# Keep images updated
# Remove unnecessary packages
```

### Runtime Security
```yaml
services:
  brokerflow:
    user: "1000:1000"  # Non-root user
    read_only: true    # Read-only filesystem
    tmpfs:
      - /tmp          # Writable temporary filesystem
    security_opt:
      - no-new-privileges:true
```

### Secrets Management
```yaml
# Use Docker secrets
services:
  brokerflow:
    secrets:
      - db_password
      - openai_api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  openai_api_key:
    file: ./secrets/openai_api_key.txt
```

## 🎯 Advanced Usage

### Multi-stage Builds
```dockerfile
# Build stage
FROM python:3.10-slim as builder
# Install build dependencies and compile

# Runtime stage
FROM python:3.10-slim as runtime
# Copy only necessary files from builder
# Install runtime dependencies only
```

### Custom Networks
```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge

services:
  brokerflow:
    networks:
      - frontend
      - backend
```

### Named Volumes for Specific Paths
```yaml
volumes:
  db_data:
  logs_data:

services:
  brokerflow:
    volumes:
      - logs_data:/app/logs
  db:
    volumes:
      - db_data:/var/lib/mysql
```

## 📞 Support

### Documentation
- User guides in `docs/` directory
- API documentation
- Troubleshooting guides

### Community Support
- GitHub Issues: https://github.com/yourorganization/brokerflow-ai/issues
- GitHub Discussions: https://github.com/yourorganization/brokerflow-ai/discussions

### Professional Support
- Email: support@brokerflow.ai
- SLA: 24/7 support for enterprise customers

---

*Last updated: August 13, 2025*
*Version: 1.0*