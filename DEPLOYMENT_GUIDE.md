# BrokerFlow AI - Deployment Guide

## 🎯 **Overview**

This guide provides comprehensive instructions for deploying BrokerFlow AI in various environments, from local development to production-scale deployments. The platform supports multiple deployment models including Docker Compose, Kubernetes, and cloud-native architectures.

## 🏗️ **Architecture Overview**

### **Core Components**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Service   │    │  Frontend Dash  │    │   Processor     │
│   (FastAPI)     │    │  (Streamlit)    │    │  (Document AI)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Database      │
                    │   (MySQL 8.0)   │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Cache/Queue   │
                    │  (Redis 7+)     │
                    └─────────────────┘
```

### **Service Dependencies**
- **API Service**: Depends on MySQL, Redis
- **Frontend**: Depends on API Service
- **Processor**: Depends on MySQL, Redis, OpenAI
- **Database**: No external dependencies
- **Cache**: No external dependencies

## 🐳 **Docker Compose Deployment**

### **Prerequisites**
- Docker Engine 20.10+
- Docker Compose 1.29+
- 4GB+ RAM recommended
- 20GB+ disk space

### **Quick Start Deployment**

```bash
# Clone repository
git clone https://github.com/your-org/brokerflow-ai.git
cd brokerflow-ai

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Start services
docker compose up -d

# Initialize database (first time only)
docker compose exec processor python populate_coherent_data.py

# Access services
# Frontend: http://localhost:8501
# API Docs: http://localhost:8000/docs
# phpMyAdmin: http://localhost:8080
```

### Destroy deployment

```bash
# 1. Configurazione iniziale
cp .env.example .env
# Modifica .env con la tua API Key OpenAI (opzionale per demo)

# 2. Avvio ambiente
docker compose up -d
docker compose exec processor python populate_coherent_data.py

# 3. Verifica servizi attivi
docker compose ps

# 4. rimozione ambiente e riallocazione da zero (attenzione può rimuovere anche altri ambienti Docker)
docker compose down
docker rm $(docker ps -aq)
docker rmi $(docker images -q)
docker volume rm $(docker volume ls -q)
docker network rm $(docker network ls -q)
docker system prune -a --volumes
# riallocazione da zero
docker compose up -d
docker compose exec processor python populate_coherent_data.py
```

### **Environment Configuration**

#### **Core Environment Variables**
```env
# Database Configuration
MYSQL_HOST=db
MYSQL_USER=brokerflow
MYSQL_PASSWORD=brokerflow123
MYSQL_DATABASE=brokerflow_ai
MYSQL_ROOT_PASSWORD=root123

# OpenAI API Configuration
OPENAI_API_KEY=sk-proj-your-api-key-here

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379

# Application Configuration
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO
```

#### **Advanced Configuration**
```env
# Email Configuration (for notifications)
SMTP_HOST=smtp.your-provider.com
SMTP_PORT=587
SMTP_USER=notifications@your-domain.com
SMTP_PASSWORD=your-smtp-password

# Security Configuration
JWT_SECRET_KEY=your-jwt-secret-here
JWT_EXPIRATION_DAYS=30

# Performance Tuning
PROCESSOR_WORKERS=4
API_WORKERS=2
MAX_CONNECTIONS=100
```

### **Docker Compose Variants**

#### **Development Environment**
```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  api:
    build: .
    command: uvicorn api_b2b:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/app
      - ./logs:/app/logs
      
  processor:
    build: .
    command: python -m debugpy --listen 0.0.0.0:5678 main.py
    volumes:
      - .:/app
      - ./logs:/app/logs
      
  db:
    ports:
      - "3306:3306"  # Expose for external tools
      
  redis:
    ports:
      - "6379:6379"  # Expose for debugging
```

#### **Production Environment**
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  api:
    build: .
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
    restart: unless-stopped
    
  frontend:
    build: .
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 512M
          cpus: '0.25'
    restart: unless-stopped
    
  processor:
    build: .
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
    restart: unless-stopped
    
  db:
    volumes:
      - /prod/mysql/data:/var/lib/mysql
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
          
  redis:
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.25'
```

## ☸️ **Kubernetes Deployment**

### **Helm Chart Structure**
```
brokerflow-ai/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── ingress.yaml
│   └── hpa.yaml
└── charts/
    └── mysql/
```

### **Helm Values Configuration**
```yaml
# values.yaml
replicaCount:
  api: 3
  frontend: 2
  processor: 2

images:
  repository: your-registry/brokerflow-ai
  tag: "2.1.0"
  pullPolicy: IfNotPresent

resources:
  api:
    limits:
      cpu: "500m"
      memory: "1Gi"
    requests:
      cpu: "250m"
      memory: "512Mi"

env:
  APP_ENV: production
  DEBUG: false
  LOG_LEVEL: INFO

ingress:
  enabled: true
  hosts:
    - host: brokerflow.your-domain.com
      paths: ["/"]
  tls:
    - secretName: brokerflow-tls
      hosts:
        - brokerflow.your-domain.com

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

### **Kubernetes Manifests**

#### **API Deployment**
```yaml
# templates/api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "brokerflow.fullname" . }}-api
spec:
  replicas: {{ .Values.replicaCount.api }}
  selector:
    matchLabels:
      {{- include "brokerflow.selectorLabels" . | nindent 6 }}
      component: api
  template:
    metadata:
      labels:
        {{- include "brokerflow.selectorLabels" . | nindent 8 }}
        component: api
    spec:
      containers:
      - name: api
        image: "{{ .Values.images.repository }}:{{ .Values.images.tag }}"
        command: ["uvicorn", "api_b2b:app", "--host", "0.0.0.0", "--port", "8000"]
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: {{ include "brokerflow.fullname" . }}
        - secretRef:
            name: {{ include "brokerflow.fullname" . }}-secrets
        resources:
          {{- toYaml .Values.resources.api | nindent 10 }}
        readinessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

#### **Service Configuration**
```yaml
# templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "brokerflow.fullname" . }}
  labels:
    {{- include "brokerflow.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: 8000
      protocol: TCP
      name: api
  selector:
    {{- include "brokerflow.selectorLabels" . | nindent 4 }}
    component: api
```

### **Kubernetes Deployment Commands**
```bash
# Install Helm chart
helm install brokerflow ./brokerflow-ai \
  --namespace brokerflow \
  --create-namespace \
  --set env.OPENAI_API_KEY="your-api-key"

# Upgrade deployment
helm upgrade brokerflow ./brokerflow-ai \
  --namespace brokerflow \
  --set images.tag="2.1.1" \
  --set replicaCount.api=5

# Scale services
kubectl scale deployment/brokerflow-api \
  --namespace brokerflow \
  --replicas=5

# View logs
kubectl logs -f deployment/brokerflow-api \
  --namespace brokerflow
```

## ☁️ **Cloud Provider Deployments**

### **AWS Deployment**

#### **Using ECS with Fargate**
```yaml
# task-definition.json
{
  "family": "brokerflow-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "your-ecr-repo/brokerflow-ai:2.1.0",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "MYSQL_HOST",
          "value": "your-rds-endpoint.amazonaws.com"
        }
      ],
      "secrets": [
        {
          "name": "OPENAI_API_KEY",
          "valueFrom": "arn:aws:ssm:region:account:parameter/openai-api-key"
        }
      ]
    }
  ]
}
```

#### **Using EKS**
```bash
# Create EKS cluster
eksctl create cluster \
  --name brokerflow-cluster \
  --version 1.27 \
  --region eu-west-1 \
  --nodegroup-name brokerflow-ng \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 1 \
  --nodes-max 10

# Deploy with Helm
helm repo add brokerflow https://your-helm-repo.com
helm install brokerflow brokerflow/brokerflow-ai \
  --namespace brokerflow \
  --set service.type=LoadBalancer \
  --set ingress.enabled=true
```

### **Google Cloud Deployment**

#### **Using GKE**
```bash
# Create GKE cluster
gcloud container clusters create brokerflow-cluster \
  --zone=europe-west1 \
  --num-nodes=3 \
  --machine-type=e2-medium

# Configure kubectl
gcloud container clusters get-credentials brokerflow-cluster \
  --zone=europe-west1

# Deploy application
kubectl apply -f k8s-manifests/
```

#### **Using Cloud Run**
```bash
# Build and push container
gcloud builds submit \
  --tag gcr.io/your-project/brokerflow-api

# Deploy to Cloud Run
gcloud run deploy brokerflow-api \
  --image gcr.io/your-project/brokerflow-api \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars MYSQL_HOST=your-cloudsql-instance
```

### **Azure Deployment**

#### **Using AKS**
```bash
# Create AKS cluster
az aks create \
  --resource-group brokerflow-rg \
  --name brokerflow-cluster \
  --node-count 3 \
  --enable-addons monitoring \
  --generate-ssh-keys

# Get credentials
az aks get-credentials \
  --resource-group brokerflow-rg \
  --name brokerflow-cluster

# Deploy application
helm install brokerflow ./charts/brokerflow-ai \
  --namespace brokerflow
```

## 🛠️ **Infrastructure as Code**

### **Terraform Configuration**
```hcl
# main.tf
provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_network" "brokerflow" {
  name = "brokerflow-network"
}

resource "docker_volume" "db_data" {
  name = "brokerflow-db-data"
}

resource "docker_container" "db" {
  name  = "brokerflow-db"
  image = "mysql:8.0"
  
  networks_advanced {
    name = docker_network.brokerflow.name
  }
  
  volumes {
    volume_name = docker_volume.db_data.name
    container_path = "/var/lib/mysql"
  }
  
  env = [
    "MYSQL_ROOT_PASSWORD=${var.mysql_root_password}",
    "MYSQL_USER=${var.mysql_user}",
    "MYSQL_PASSWORD=${var.mysql_password}",
    "MYSQL_DATABASE=${var.mysql_database}"
  ]
  
  ports {
    internal = 3306
    external = 3306
  }
}
```

### **Ansible Playbook**
```yaml
# deploy-brokerflow.yml
---
- hosts: brokerflow-servers
  become: yes
  vars:
    docker_compose_version: "1.29.2"
    
  tasks:
    - name: Install Docker
      apt:
        name: docker.io
        state: present
        
    - name: Install Docker Compose
      get_url:
        url: "https://github.com/docker/compose/releases/download/{{ docker_compose_version }}/docker-compose-Linux-x86_64"
        dest: /usr/local/bin/docker-compose
        mode: '0755'
        
    - name: Clone BrokerFlow AI repository
      git:
        repo: https://github.com/your-org/brokerflow-ai.git
        dest: /opt/brokerflow-ai
        force: yes
        
    - name: Configure environment
      template:
        src: env.j2
        dest: /opt/brokerflow-ai/.env
        
    - name: Start services
      shell: |
        cd /opt/brokerflow-ai
        docker-compose up -d
```

## 🔧 **Monitoring and Observability**

### **Prometheus Metrics**
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'brokerflow-api'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/api/v1/metrics'
    
  - job_name: 'brokerflow-processor'
    static_configs:
      - targets: ['processor:8001']
    metrics_path: '/metrics'
```

### **Grafana Dashboards**
```json
{
  "dashboard": {
    "title": "BrokerFlow AI - System Overview",
    "panels": [
      {
        "title": "API Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "95th percentile"
          }
        ]
      },
      {
        "title": "Database Connections",
        "type": "gauge",
        "targets": [
          {
            "expr": "mysql_global_status_threads_connected",
            "legendFormat": "Connected"
          }
        ]
      }
    ]
  }
}
```

### **ELK Stack Integration**
```yaml
# docker-compose.logging.yml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"
      
  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
    depends_on:
      - elasticsearch
      
  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
```

## 🚀 **CI/CD Pipeline**

### **GitHub Actions Workflow**
```yaml
# .github/workflows/deploy.yml
name: Deploy BrokerFlow AI

on:
  push:
    branches: [ main, develop ]
  release:
    types: [ created ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: testpass
          MYSQL_DATABASE: test_db
        ports:
          - 3306:3306
          
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
        
    - name: Run tests
      run: pytest tests/ --cov=. --cov-report=xml
      env:
        MYSQL_HOST: localhost
        MYSQL_USER: root
        MYSQL_PASSWORD: testpass
        MYSQL_DATABASE: test_db
        
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      
  deploy-production:
    needs: build-and-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    
    steps:
    - name: Deploy to production
      run: |
        ssh deploy@production-server "cd /opt/brokerflow && git pull && docker-compose down && docker-compose up -d"
```

### **GitLab CI/CD**
```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

test:
  stage: test
  image: python:3.10
  services:
    - mysql:8.0
  variables:
    MYSQL_ROOT_PASSWORD: testpass
    MYSQL_DATABASE: test_db
  script:
    - pip install -r requirements.txt
    - pip install -r requirements-dev.txt
    - pytest tests/ --cov=.

build:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  script:
    - docker build -t registry.gitlab.com/your-org/brokerflow-ai:$CI_COMMIT_SHA .
    - docker push registry.gitlab.com/your-org/brokerflow-ai:$CI_COMMIT_SHA

deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/brokerflow-api brokerflow-api=registry.gitlab.com/your-org/brokerflow-ai:$CI_COMMIT_SHA
  only:
    - main
```

## 🔒 **Security Best Practices**

### **Network Security**
```yaml
# docker-compose.secure.yml
version: '3.8'
services:
  api:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    networks:
      - frontend
      - backend
      
  db:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    networks:
      - backend
    volumes:
      - db_data:/var/lib/mysql:rw
      
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access
```

### **Secrets Management**
```bash
# Using Docker Secrets
echo "your-openai-api-key" | docker secret create openai_api_key -

# Using HashiCorp Vault
vault kv put secret/brokerflow/openai api_key="your-api-key"

# Using AWS Secrets Manager
aws secretsmanager create-secret \
  --name brokerflow/openai-api-key \
  --secret-string "your-api-key"
```

## 📈 **Scaling Strategies**

### **Horizontal Pod Autoscaler (Kubernetes)**
```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: brokerflow-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: brokerflow-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### **Database Scaling**
```sql
-- Read Replicas for MySQL
-- Configure in docker-compose or cloud provider

-- Connection Pooling
-- Increase max_connections and optimize queries

-- Index Optimization
CREATE INDEX idx_client_sector ON clients(sector);
CREATE INDEX idx_policy_status ON policies(status);
CREATE INDEX idx_claim_date ON claims(claim_date);
```

## 🆘 **Troubleshooting Common Issues**

### **Deployment Failures**
```bash
# Check service status
docker compose ps

# View service logs
docker compose logs api
docker compose logs processor

# Check resource usage
docker stats

# Restart problematic services
docker compose restart api
```

### **Database Connection Issues**
```bash
# Test database connectivity
docker compose exec api mysql -h db -u brokerflow -pbrokerflow123 brokerflow_ai

# Check database status
docker compose exec db mysqladmin -u root -p status

# Rebuild database
docker compose down -v
docker compose up -d
```

### **Performance Problems**
```bash
# Monitor system resources
top
htop
iotop

# Check Docker resource usage
docker system df
docker stats

# Optimize queries
docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "SHOW PROCESSLIST;"
```

## 📊 **Backup and Disaster Recovery**

### **Automated Backups**
```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backups/brokerflow"
DATE=$(date +%Y%m%d_%H%M%S)

# Database backup
docker compose exec db mysqldump -u brokerflow -pbrokerflow123 brokerflow_ai > "$BACKUP_DIR/backup_$DATE.sql"

# Compress backup
gzip "$BACKUP_DIR/backup_$DATE.sql"

# Retention policy (keep last 30 days)
find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +30 -delete

# Verify backup integrity
gunzip -t "$BACKUP_DIR/backup_$DATE.sql.gz"
```

### **Restore Procedures**
```bash
# Restore database from backup
gunzip backup_20250818_103045.sql.gz
docker compose exec -T db mysql -u brokerflow -pbrokerflow123 brokerflow_ai < backup_20250818_103045.sql

# Verify restoration
docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "SELECT COUNT(*) FROM clients;"
```

## 📞 **Support and Maintenance**

### **SLA Commitments**
- **Uptime**: 99.9% (99.5% weekends/holidays)
- **Response Time**: < 2 hours (critical), < 24 hours (standard)
- **Resolution Time**: < 24 hours (critical), < 72 hours (standard)

### **Maintenance Windows**
- **Scheduled Maintenance**: Sunday 2:00-4:00 AM UTC
- **Emergency Patches**: As needed with 4-hour advance notice
- **Feature Releases**: Bi-weekly on Tuesdays

### **Contact Information**
- **24/7 Support**: support@brokerflow.it
- **Technical Escalation**: escalation@brokerflow.it
- **Status Page**: status.brokerflow.it
- **SLA Violations**: sla-violations@brokerflow.it

---
*BrokerFlow AI - Enterprise-Grade Deployment Guide*

**Version**: 2.1.0 | **Last Updated**: August 2025