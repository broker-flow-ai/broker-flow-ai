# BrokerFlow AI - Documentazione Tecnica Completa

## 🏗️ **Architettura del Sistema**

### **Componenti Principali**

1. **API Service (FastAPI)**
   - Endpoint RESTful per tutte le funzionalità
   - Autenticazione JWT e rate limiting
   - Documentazione Swagger/OpenAPI automatica

2. **Frontend Dashboard (Streamlit)**
   - Interfaccia utente responsive
   - Dashboard analitiche in tempo reale
   - Visualizzazioni interattive Plotly

3. **Processor Service**
   - Elaborazione documentale AI/ML
   - OCR avanzato con PyMuPDF
   - Classificazione rischi OpenAI GPT-4

4. **Database (MySQL 8.0)**
   - Schema normalizzato per dati assicurativi
   - Relazioni complesse clienti/polizze/sinistri
   - Supporto JSON per dati dinamici

5. **Cache Layer (Redis)**
   - Sessioni utente e caching risultati
   - Rate limiting distribuito
   - Pub/Sub per eventi real-time

### **Flusso di Dati End-to-End**

```
📁 Inbox PDF → 🤖 Processor AI → 🗃️ Database → 📊 API Analytics → 🖥️ Dashboard
     ↓              ↓               ↓              ↓                 ↓
📎 Allegati    🔍 Estrazione    💾 Salvataggio  📈 KPIs         🎯 Visualizzazioni
📧 Email        🧠 Classificazione 📋 Validazione 🔗 Export        📱 Responsive
📄 Templates    💰 Pricing        🔐 Sicurezza   📤 API            📊 Reportistica
```

## 🛠️ **Setup e Deploy**

### **Prerequisiti di Sistema**
- Docker Engine 20.10+
- Docker Compose 1.29+
- 4GB RAM minimo (8GB consigliati)
- 10GB spazio disco disponibile

### **Installazione Locale**

```bash
# Clonare repository
git clone https://github.com/tuo-account/broker-flow-ai.git
cd broker-flow-ai

# Configurare variabili ambiente
cp .env.example .env
# Modificare .env con credenziali reali

# Avviare ambiente
docker compose up -d

# Popolare dati di esempio
docker compose exec processor python populate_coherent_data.py

# Accesso dashboard
http://localhost:8501
```

### **Deploy Produzione**

```bash
# Build immagini ottimizzate
docker compose -f docker-compose.prod.yml build

# Deploy con scaling
docker compose -f docker-compose.prod.yml up -d --scale api=3 --scale processor=2

# Monitoraggio health checks
docker compose -f docker-compose.prod.yml ps
```

## 🔧 **Configurazione Variabili Ambiente**

### **Database**
```env
MYSQL_HOST=db
MYSQL_USER=brokerflow
MYSQL_PASSWORD=brokerflow123
MYSQL_DATABASE=brokerflow_ai
MYSQL_ROOT_PASSWORD=root123
```

### **OpenAI API**
```env
OPENAI_API_KEY=sk-proj-tua-chiave-openai
```

### **Email/SMS Gateway**
```env
SMTP_HOST=smtp.tuoserver.it
SMTP_PORT=587
SMTP_USER=tuo@email.it
SMTP_PASSWORD=tua-password
```

## 📊 **Schema Database**

### **Tabelle Principali**

#### **clients**
```sql
CREATE TABLE clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    company VARCHAR(255),
    email VARCHAR(255),
    sector VARCHAR(100),
    address TEXT,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **risks**
```sql
CREATE TABLE risks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    broker_id INT,
    risk_type VARCHAR(100),
    details JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (broker_id) REFERENCES clients(id)
);
```

#### **policies**
```sql
CREATE TABLE policies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    risk_id INT,
    company_id INT,
    company VARCHAR(100),
    policy_number VARCHAR(100),
    start_date DATE,
    end_date DATE,
    status ENUM('active', 'expired', 'cancelled') DEFAULT 'active',
    policy_pdf_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (risk_id) REFERENCES risks(id),
    FOREIGN KEY (company_id) REFERENCES clients(id)
);
```

#### **claims**
```sql
CREATE TABLE claims (
    id INT AUTO_INCREMENT PRIMARY KEY,
    policy_id INT,
    claim_date DATE,
    amount DECIMAL(10,2),
    status ENUM('open', 'in_review', 'approved', 'rejected') DEFAULT 'open',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (policy_id) REFERENCES policies(id)
);
```

#### **premiums**
```sql
CREATE TABLE premiums (
    id INT AUTO_INCREMENT PRIMARY KEY,
    policy_id INT,
    amount DECIMAL(10,2),
    due_date DATE,
    payment_status ENUM('pending', 'paid', 'overdue') DEFAULT 'pending',
    payment_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (policy_id) REFERENCES policies(id)
);
```

## 🤖 **Moduli AI Core**

### **Modulo Classificazione Rischio**
```python
# modules/classify_risk.py
def classify_risk(text):
    """
    Classifica il tipo di rischio assicurativo
    Input: testo estratto da PDF richiesta
    Output: categoria rischio (Flotta Auto, RC Professionale, ecc.)
    """
    prompt = f"""
    Classifica il seguente testo come uno di questi tipi di rischio:
    - Flotta Auto
    - RC Professionale  
    - Fabbricato
    - Rischi Tecnici
    - Altro
    
    Testo: {text}
    
    Rispondi solo con la categoria esatta.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    return response.choices[0].message.content.strip()
```

### **Modulo Analisi Rischio**
```python
# modules/risk_analyzer.py
def analyze_risk_sustainability(client_profile, historical_data):
    """
    Analizza sostenibilità del rischio con AI avanzata
    Input: profilo cliente e dati storici
    Output: score rischio, raccomandazioni pricing, note underwriting
    """
    # Analisi predittiva con machine learning
    # Benchmark settoriale
    # Raccomandazioni personalizzate
    # Score 0-100 con confidenza statistica
```

### **Modulo Underwriting Automatizzato**
```python
# modules/ai_underwriting.py
def automated_underwriting(risk_data):
    """
    Processo di underwriting automatizzato
    Input: dati rischio estratti
    Output: decisione underwriting, condizioni, limiti copertura
    """
    # Valutazione compliance normativa
    # Controllo blacklist/whitelist
    # Cross-check fonti esterne
    # Decisione basata su regole + AI
```

## 📈 **API Endpoints Principali**

### **Analisi Rischio**
```
POST /api/v1/insurance/risk-analysis
{
  "client_id": 123
}

Response:
{
  "analysis_id": 456,
  "client_id": 123,
  "analysis": {
    "risk_score": 75.5,
    "sector_analysis": "...",
    "pricing_recommendation": "...",
    "recommendation_level": "Alto"
  }
}
```

### **Dashboard Analytics**
```
GET /api/v1/insurance/portfolio-analytics
Query: ?company_id=1

Response:
{
  "portfolio_summary": [...],
  "trend_analysis": [...],
  "sector_breakdown": [...]
}
```

### **Performance Compagnia**
```
GET /api/v1/insurance/company-performance
Query: ?company_id=1

Response:
{
  "kpi": {
    "total_policies": 150,
    "active_policies": 120,
    "total_premium": 450000.00,
    "loss_ratio": 12.5
  },
  "benchmark": {...},
  "market_position": {...}
}
```

## 📊 **Dashboard Analytics Features**

### **Metriche Portfolio**
- Distribuzione tipi rischio
- Trend emissioni polizze
- Analisi settoriale
- Confronto benchmark mercato

### **Performance Brokers**
- Score totale 0-100
- Livello (Bronze/Gold/Platinum)
- Volume polizze emesse
- Premi totali generati
- Sinistri registrati

### **Compliance Reporting**
- Report GDPR/SOX/IVASS
- Audit trail completo
- Retention policy tracking
- Security measures monitoring

## 🔒 **Sicurezza e Compliance**

### **Data Protection**
- Crittografia AES-256 at rest
- TLS 1.3 in transito
- Key rotation automatico
- Backup criptati e firmati

### **Access Control**
- Autenticazione JWT
- Autorizzazioni RBAC
- Audit logging completo
- Session expiry configurabile

### **Regulatory Compliance**
- GDPR compliant by design
- SOX controls implementati
- IVASS guidelines seguite
- Audit trail 7 anni

## 🚀 **Performance e Scalabilità**

### **Capacity Planning**
- Singola istanza: 1000 PDF/giorno
- Cluster 3 nodi: 10.000 PDF/giorno
- Auto-scaling Kubernetes: 100.000+ PDF/giorno

### **Tempi di Risposta**
- Elaborazione PDF: 5-15 secondi
- API response time: < 200ms
- Dashboard loading: < 2 secondi

### **Monitoraggio**
- Health checks ogni 30s
- Alerting Slack/Email
- Metriche Prometheus
- Logging centralizzato

## 🛠️ **Manutenzione e Troubleshooting**

### **Comandi Diagnostica**
```bash
# Verifica servizi attivi
docker compose ps

# Logs realtime
docker compose logs -f

# Stats risorse
docker stats

# Shell container
docker compose exec api bash
```

### **Problemi Comuni**

#### **Processor non elabora PDF**
```bash
# Verifica file nella inbox
docker compose exec processor ls -la /app/inbox/

# Test OCR manuale
docker compose exec processor pdftotext /app/inbox/sample.pdf -

# Riavvio processor
docker compose restart processor
```

#### **Database connection issues**
```bash
# Verifica connessione
docker compose exec api mysql -h db -u brokerflow -pbrokerflow123 brokerflow_ai

# Restart database
docker compose restart db
```

#### **API non risponde**
```bash
# Verifica health check
curl http://localhost:8000/api/v1/health

# Logs dettagliati
docker compose logs api --tail 100
```

## 📦 **Backup e Recovery**

### **Backup Automatico**
```bash
# Script cron giornaliero
0 2 * * * docker compose exec db mysqldump -u brokerflow -pbrokerflow123 brokerflow_ai > backup_$(date +%Y%m%d).sql

# Compressione e rotazione
tar -czf backup_$(date +%Y%m%d).tar.gz backup_$(date +%Y%m%d).sql
find . -name "backup_*.tar.gz" -mtime +30 -delete
```

### **Recovery Procedure**
```bash
# Restore database
docker compose exec -T db mysql -u brokerflow -pbrokerflow123 brokerflow_ai < backup.sql

# Verifica integrità
docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "SELECT COUNT(*) FROM clients;"
```

## 🔄 **Aggiornamenti e CI/CD**

### **Pipeline Deploy**
```yaml
# .github/workflows/deploy.yml
steps:
  - checkout code
  - run tests
  - build docker images
  - scan vulnerabilities
  - deploy staging
  - smoke tests
  - deploy production
  - health checks
```

### **Versioning Semantico**
- **Major**: Breaking changes API/UI
- **Minor**: Nuove funzionalità backward-compatible  
- **Patch**: Bug fixes e security updates

## 📞 **Supporto e Contatti**

### **Canali Supporto**
- Email: support@brokerflow.it
- Slack: team-brokerflow.slack.com
- Docs: docs.brokerflow.it
- Status: status.brokerflow.it

### **SLA Garantiti**
- Uptime: 99.9% (99.5% weekend/festivi)
- Response time: < 2 ore (business critical)
- Resolution time: < 24 ore (critical), < 72 ore (standard)

---
*BrokerFlow AI - Documentazione Tecnica Aggiornata al 2025*