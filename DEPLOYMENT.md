# BrokerFlow AI - Deployment Guide

## 🚀 Overview

This guide provides instructions for deploying BrokerFlow AI in various environments, from local development to production systems.

## 🎯 Deployment Options

### 1. Local Development
- **Purpose**: Development and testing
- **Requirements**: Minimal
- **Scalability**: Not suitable for production
- **Security**: Development only

### 2. Standalone Server
- **Purpose**: Small to medium production use
- **Requirements**: Dedicated server
- **Scalability**: Limited
- **Security**: Basic production security

### 3. Docker Deployment
- **Purpose**: Containerized deployment
- **Requirements**: Docker engine
- **Scalability**: Good with orchestration
- **Security**: Container security best practices

### 4. Cloud Deployment
- **Purpose**: Large scale production
- **Requirements**: Cloud provider account
- **Scalability**: High with auto-scaling
- **Security**: Enterprise security features

## 🛠 Local Development Deployment

### Prerequisites
- Python 3.8+
- MySQL 5.7+ (optional)
- Tesseract OCR (for scanned PDFs)
- Git

### Steps

1. **Clone the Repository**
```bash
git clone https://github.com/yourorganization/brokerflow-ai.git
cd brokerflow-ai
```

2. **Create Virtual Environment**
```bash
python -m venv brokerflow-env
source brokerflow-env/bin/activate  # On Windows: brokerflow-env\\Scripts\\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

4. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Set Up Database**
```sql
CREATE DATABASE brokerflow_ai;
USE brokerflow_ai;
SOURCE schema.sql;
```

6. **Run the Application**
```bash
# For development with demo mode
python main_simulated.py

# For full functionality
python main.py
```

## 🐳 Docker Deployment

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 1.29+

### Steps

1. **Clone the Repository**
```bash
git clone https://github.com/yourorganization/brokerflow-ai.git
cd brokerflow-ai
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Build and Run with Docker Compose**
```bash
docker-compose up -d
```

4. **Access Services**
- Application: http://localhost:8000
- Database: mysql://localhost:3306
- phpMyAdmin: http://localhost:8080

### Docker Configuration

#### Environment Variables
Set these in your `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_USER=brokerflow
MYSQL_PASSWORD=your_brokerflow_password
```

#### Volume Mounts
- `./inbox`: PDF input directory
- `./output`: Processed files output directory
- `./templates`: PDF templates directory
- `./logs`: Application logs
- `db_data`: Database persistent storage

### Docker Commands

#### Build Images
```bash
docker-compose build
```

#### Start Services
```bash
docker-compose up -d
```

#### Stop Services
```bash
docker-compose down
```

#### View Logs
```bash
docker-compose logs -f
```

#### Execute Commands in Container
```bash
docker-compose exec brokerflow bash
```

## ☁️ Cloud Deployment

### AWS Deployment

#### Prerequisites
- AWS Account
- AWS CLI configured
- Elastic Beanstalk CLI (eb CLI)

#### Steps

1. **Prepare Application**
```bash
# Create application bundle
zip -r brokerflow-ai.zip . -x \"*.git*\" \"*/__pycache__/*\" \"*.pyc\" \"tmp/*\" \"logs/*\"
```

2. **Deploy to Elastic Beanstalk**
```bash
eb init
eb create brokerflow-ai-production
eb deploy
```

#### AWS Services Used
- **EC2**: Application hosting
- **RDS**: MySQL database
- **S3**: File storage
- **Elastic Beanstalk**: Application deployment
- **CloudWatch**: Monitoring and logging

### Azure Deployment

#### Prerequisites
- Azure Account
- Azure CLI configured

#### Steps

1. **Create Resource Group**
```bash
az group create --name brokerflow-rg --location eastus
```

2. **Deploy with Azure Container Instances**
```bash
az container create \\
  --resource-group brokerflow-rg \\
  --name brokerflow-ai \\
  --image brokerflow/brokerflow-ai:latest \\
  --dns-name-label brokerflow-ai \\
  --ports 8000
```

#### Azure Services Used
- **Azure Container Instances**: Container hosting
- **Azure Database for MySQL**: Database service
- **Azure Storage**: File storage
- **Azure Monitor**: Monitoring and logging

### Google Cloud Deployment

#### Prerequisites
- Google Cloud Account
- Google Cloud SDK configured

#### Steps

1. **Build and Push Docker Image**
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/brokerflow-ai
```

2. **Deploy to Cloud Run**
```bash
gcloud run deploy brokerflow-ai \\
  --image gcr.io/PROJECT-ID/brokerflow-ai \\
  --platform managed
```

#### Google Cloud Services Used
- **Cloud Run**: Container hosting
- **Cloud SQL**: MySQL database
- **Cloud Storage**: File storage
- **Cloud Logging**: Logging service

## 🏢 Enterprise Deployment

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Load Balancer                            │
└─────────────────────────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────────────────────────┐
│              Web/API Servers (3+ instances)                 │
└─────────────────────────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────────────────────────┐
│              Processing Workers (5+ instances)              │
└─────────────────────────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────────────────────────┐
│              Redis Cache & Message Queue                    │
└─────────────────────────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────────────────────────┐
│              MySQL Cluster (Master/Slave)                   │
└─────────────────────────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────────────────────────┐
│              File Storage (S3/Cloud Storage)                │
└─────────────────────────────────────────────────────────────┘
```

### High Availability

#### Database
- Master-slave replication
- Automatic failover
- Regular backups
- Geographical distribution

#### Application
- Multiple server instances
- Load balancing
- Health checks
- Auto-scaling

#### Storage
- Redundant file storage
- CDN for static assets
- Backup and disaster recovery

### Security

#### Network Security
- Firewall rules
- VPN access for administration
- DDoS protection
- Intrusion detection

#### Data Security
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- Key management
- Access controls

#### Application Security
- Authentication and authorization
- Input validation
- Security headers
- Regular security scanning

### Monitoring and Logging

#### Monitoring
- Application performance monitoring
- Infrastructure monitoring
- Database performance
- Network monitoring

#### Logging
- Centralized log management
- Log retention policies
- Alerting and notifications
- Log analysis

#### Metrics
- Business metrics
- Performance metrics
- System metrics
- User experience metrics

## ⚙️ Configuration Management

### Environment-Specific Configuration

#### Development
```bash
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///brokerflow_dev.db
```

#### Staging
```bash
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=mysql://user:pass@staging-db:3306/brokerflow_ai
```

#### Production
```bash
DEBUG=false
LOG_LEVEL=WARNING
DATABASE_URL=mysql://user:pass@prod-db:3306/brokerflow_ai
ENABLE_SSL=true
```

### Configuration Files

#### config.yaml
Main configuration file with all settings:
```yaml
system:
  name: "BrokerFlow AI"
  version: "1.0.0"
  debug: false

database:
  type: "mysql"
  connection:
    host: "localhost"
    port: 3306
    username: "brokerflow"
    password: "brokerflow123"
    database: "brokerflow_ai"
```

#### .env
Environment variables for sensitive data:
```bash
OPENAI_API_KEY=sk-...
MYSQL_PASSWORD=...
SECRET_KEY=...
```

## 🔧 Maintenance

### Regular Tasks

#### Daily
- Log file rotation
- Database optimization
- Backup verification
- Security scanning

#### Weekly
- System updates
- Performance tuning
- Capacity planning
- Report generation

#### Monthly
- Database maintenance
- Security audit
- Compliance review
- Disaster recovery testing

### Backup and Recovery

#### Backup Strategy
- Daily incremental backups
- Weekly full backups
- Monthly archive backups
- Offsite storage

#### Recovery Procedures
- Database restore
- File recovery
- Configuration recovery
- Service restoration

### Updates and Upgrades

#### Patch Management
- Security patches applied immediately
- Feature updates tested in staging
- Rollback procedures documented
- Change management process

#### Version Upgrades
- Compatibility testing
- Data migration procedures
- Downtime planning
- Communication plan

## 📊 Performance Tuning

### Database Optimization
- Index optimization
- Query optimization
- Connection pooling
- Caching strategies

### Application Optimization
- Memory management
- CPU usage optimization
- I/O optimization
- Concurrency tuning

### Network Optimization
- CDN configuration
- Load balancing
- Compression
- Caching

## 🆘 Troubleshooting

### Common Issues

#### PDF Processing Issues
- **Symptom**: Slow PDF processing
- **Solution**: Check system resources, optimize Tesseract settings

#### Database Connection Issues
- **Symptom**: Database connection errors
- **Solution**: Check connection settings, verify database status

#### AI Classification Issues
- **Symptom**: Incorrect risk classification
- **Solution**: Review training data, adjust confidence thresholds

#### Email Delivery Issues
- **Symptom**: Emails not sent or delivered
- **Solution**: Check SMTP settings, verify spam filters

### Monitoring Alerts

#### Critical Alerts
- System downtime
- Database connectivity issues
- High error rates
- Security incidents

#### Warning Alerts
- High resource usage
- Slow response times
- Low disk space
- Failed backups

## 📞 Support

### Documentation
- User guides
- API documentation
- Troubleshooting guides
- Release notes

### Support Channels
- Email: support@brokerflow.ai
- Phone: +39 02 1234 5678
- Chat: Available in web interface
- Community: GitHub Discussions

### Service Level Agreements
- Response time: 2 hours (critical), 24 hours (standard)
- Uptime: 99.9%
- Resolution time: 4 hours (critical), 72 hours (standard)

---

*Last updated: August 13, 2025*
*Version: 1.0*