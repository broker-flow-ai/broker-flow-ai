# BrokerFlow AI - Documentazione API Completa

## 📋 **Panoramica API**

BrokerFlow AI espone un set completo di API RESTful per l'integrazione con sistemi esterni, dashboard, e applicazioni di terze parti. Tutte le API seguono le best practice moderne di progettazione REST e sono documentate automaticamente con OpenAPI/Swagger.

### **Endpoint Base**
```
Produzione: https://api.brokerflow.it/v1
Sviluppo: http://localhost:8000/api/v1
```

### **Formati Supportati**
- **Richieste**: JSON (application/json)
- **Risposte**: JSON (application/json)
- **Encoding**: UTF-8

### **Versioning**
- **URI Versioning**: `/api/v1/endpoint`
- **Backward Compatibility**: Garantita entro minor versions
- **Deprecation Policy**: 3 mesi notice pre-rimozione

## 🔐 **Autenticazione e Autorizzazione**

### **JWT Bearer Token**
Tutti gli endpoint richiedono autenticazione JWT:

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     https://api.brokerflow.it/v1/insurance/risk-analysis
```

### **Ottenere Token di Accesso**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "broker@example.com",
  "password": "secure_password"
}
```

### **Ruoli e Permessi**
- **Broker**: Accesso analisi rischio e clienti propri
- **InsuranceCompany**: Accesso dashboard compagnia e polizze emesse
- **Administrator**: Accesso completo a tutte le funzionalità
- **Auditor**: Accesso solo lettura a report compliance

## 📊 **API Reference Completa**

### **Health Check e Metriche di Sistema**

#### **Verifica Stato Sistema**
```http
GET /api/v1/health
```

**Response Codes:**
- `200 OK`: Sistema operativo
- `503 Service Unavailable`: Problemi con database o servizi

**Response Body:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-18T10:30:45.123456",
  "version": "2.1.0",
  "components": {
    "database": "connected",
    "redis": "connected",
    "openai": "available"
  }
}
```

#### **Metriche di Sistema**
```http
GET /api/v1/metrics
```

**Response Example:**
```json
{
  "database_metrics": {
    "clients": 156,
    "policies": 234,
    "risks": 189,
    "claims": 45,
    "premiums": 1444
  },
  "timestamp": "2025-08-18T10:30:45.123456",
  "uptime": "15 days, 6:32:15"
}
```

### **Analisi del Rischio**

#### **Analisi Rischio Avanzata Cliente**
```http
POST /api/v1/insurance/risk-analysis
Content-Type: application/json

{
  "client_id": 123
}
```

**Request Body:**
```json
{
  "client_id": 123,
  "additional_context": {
    "historical_data": true,
    "market_benchmark": true,
    "underwriting_notes": false
  }
}
```

**Response Codes:**
- `200 OK`: Analisi completata con successo
- `404 Not Found`: Cliente non trovato
- `500 Internal Server Error`: Errore elaborazione AI

**Response Body:**
```json
{
  "analysis_id": 456,
  "client_id": 123,
  "analysis": {
    "risk_score": 75.5,
    "confidence_level": 0.92,
    "sector_analysis": {
      "sector": "Trasporti",
      "benchmark_comparison": "Above average risk profile",
      "market_position": "Mid-tier"
    },
    "pricing_recommendation": {
      "recommended_premium": 2850.00,
      "coverage_limit": 500000.00,
      "deductible": 1000.00,
      "risk_multiplier": 1.35
    },
    "recommendation_level": "Medio",
    "underwriting_notes": "Cliente con flotta commerciale di medie dimensioni. Storico sinistri positivo negli ultimi 2 anni.",
    "market_data": {
      "sector_average_premium": 2500.00,
      "sector_loss_ratio": 12.5,
      "competitor_pricing": {
        "General Insurance": 2700.00,
        "Allianz": 2900.00,
        "UnipolSai": 2600.00
      }
    }
  },
  "generated_at": "2025-08-18T10:30:45.123456"
}
```

### **Dashboard Analytics**

#### **Analisi Portafoglio Assicurativo**
```http
GET /api/v1/insurance/portfolio-analytics
Query Parameters: company_id (optional)
```

**Response Example:**
```json
{
  "portfolio_summary": [
    {
      "risk_type": "Flotta Auto",
      "policy_count": 45,
      "active_policies": 38,
      "avg_risk_score": 68.2,
      "total_premium": 127500.00,
      "claim_count": 12,
      "total_claims": 45000.00,
      "claims_ratio": 35.3
    },
    {
      "risk_type": "RC Professionale",
      "policy_count": 67,
      "active_policies": 59,
      "avg_risk_score": 45.8,
      "total_premium": 98500.00,
      "claim_count": 8,
      "total_claims": 23000.00,
      "claims_ratio": 23.3
    }
  ],
  "trend_analysis": [
    {
      "month": "2025-06",
      "policies_issued": 23,
      "premium_collected": 67500.00
    },
    {
      "month": "2025-07",
      "policies_issued": 31,
      "premium_collected": 89200.00
    },
    {
      "month": "2025-08",
      "policies_issued": 18,
      "premium_collected": 52300.00
    }
  ],
  "sector_breakdown": [
    {
      "sector": "Trasporti",
      "client_count": 23,
      "policy_count": 45,
      "avg_risk_score": 72.1
    },
    {
      "sector": "Sanità",
      "client_count": 18,
      "policy_count": 32,
      "avg_risk_score": 51.3
    }
  ],
  "generated_at": "2025-08-18T10:30:45.123456"
}
```

### **Dashboard Compagnia Assicurativa**

#### **Performance Specifica Compagnia**
```http
GET /api/v1/insurance/company-performance
Query Parameters: company_id (required)
```

**Response Example:**
```json
{
  "kpi": {
    "total_policies": 156,
    "active_policies": 134,
    "total_premium": 456789.50,
    "total_claims": 23,
    "total_claim_amount": 123456.78,
    "loss_ratio": 27.0
  },
  "benchmark": {
    "market_avg_loss_ratio": 32.5,
    "market_avg_premium": 3200.00,
    "market_avg_risk_score": 58.2
  },
  "market_position": {
    "loss_ratio_vs_market": -5.5,
    "premium_vs_market": 136789.50
  },
  "trend_data": {
    "monthly_premiums": [
      {"month": "2025-05", "premium": 38500.00},
      {"month": "2025-06", "premium": 42100.00},
      {"month": "2025-07", "premium": 45600.00}
    ],
    "claims_trend": [
      {"month": "2025-05", "claims": 3},
      {"month": "2025-06", "claims": 5},
      {"month": "2025-07", "claims": 4}
    ]
  }
}
```

### **Compliance Reporting**

#### **Generazione Report Compliance**
```http
POST /api/v1/insurance/compliance-report
Content-Type: application/json
```

**Request Body:**
```json
{
  "report_type": "GDPR",
  "period_start": "2025-01-01",
  "period_end": "2025-12-31"
}
```

**Response Example:**
```json
{
  "report_id": 789,
  "report_type": "GDPR",
  "period_start": "2025-01-01",
  "period_end": "2025-12-31",
  "title": "Report Compliance GDPR - Settore Assicurativo 2025",
  "executive_summary": "Analisi completa conformità GDPR per il settore assicurativo...",
  "technical_details": {
    "data_processing_activities": [
      {
        "activity": "Estrazione dati clienti PDF",
        "purpose": "Underwriting automatizzato",
        "legal_basis": "Legittimo interesse + Contratto",
        "retention_period": "365 giorni"
      }
    ],
    "data_protection_measures": "Crittografia AES-256, backup giornalieri cifrati",
    "third_party_processors": ["OpenAI", "MySQL Hosting Provider"]
  },
  "conclusions": {
    "compliance_status": "Fully Compliant",
    "recommendations": [
      "Implementare Data Protection Impact Assessment (DPIA) per nuove funzionalità AI",
      "Aggiornare registro trattamenti trimestralmente"
    ]
  },
  "signature": "BrokerFlow AI Compliance System",
  "generated_at": "2025-08-18T10:30:45.123456"
}
```

#### **Lista Report Esistenti**
```http
GET /api/v1/insurance/compliance-reports
Query Parameters: report_type (optional)
```

**Response Example:**
```json
{
  "reports": [
    {
      "id": 1,
      "report_type": "GDPR",
      "period_start": "2025-01-01",
      "period_end": "2025-12-31",
      "generated_at": "2025-08-18T10:30:45.123456"
    },
    {
      "id": 2,
      "report_type": "SOX",
      "period_start": "2025-01-01",
      "period_end": "2025-06-30",
      "generated_at": "2025-07-15T09:15:22.123456"
    }
  ]
}
```

### **Programmi Sconto e Fedeltà**

#### **Creazione Sconto Personalizzato**
```http
POST /api/v1/insurance/discounts
Content-Type: application/json
```

**Request Body:**
```json
{
  "company_id": 1,
  "broker_id": 45,
  "discount_type": "Volume",
  "percentage": 15.5,
  "start_date": "2025-09-01",
  "end_date": "2026-08-31"
}
```

**Response Example:**
```json
{
  "discount_id": 123,
  "message": "Sconto creato con successo",
  "discount_details": {
    "company": "General Insurance S.p.A.",
    "broker": "Mario Rossi Broker",
    "discount_type": "Volume",
    "percentage": 15.5,
    "start_date": "2025-09-01",
    "end_date": "2026-08-31"
  }
}
```

#### **Calcolo Premio Scontato**
```http
GET /api/v1/insurance/discounted-premium
Query Parameters: 
  base_premium (required)
  company_id (required)
  broker_id (required)
```

**Response Example:**
```json
{
  "base_premium": 2500.00,
  "discounted_premium": 2125.00,
  "discount_percentage": 15.0,
  "savings": 375.00,
  "broker_tier": "Gold"
}
```

### **Metriche Performance Broker**

#### **Calcolo Metriche Broker**
```http
GET /api/v1/insurance/broker-metrics
Query Parameters: broker_id (required)
```

**Response Example:**
```json
{
  "performance_score": 78.5,
  "tier": "Gold",
  "volume_metrics": {
    "policies_count": 45,
    "total_premium": 125678.50
  },
  "claims_metrics": {
    "claims_count": 3,
    "total_claims": 18500.00
  },
  "efficiency_metrics": {
    "conversion_rate": 32.5,
    "avg_turnaround_time": "2.3 giorni"
  },
  "loyalty_metrics": {
    "relationship_duration": "18 mesi",
    "repeat_business": 89.2
  }
}
```

## 📈 **WebSocket API (Real-time)**

### **Connessione WebSocket**
```
wss://api.brokerflow.it/ws/v1/events
```

### **Eventi in Tempo Reale**
```javascript
const ws = new WebSocket('wss://api.brokerflow.it/ws/v1/events');

ws.onopen = function(event) {
    // Subscribe to events
    ws.send(JSON.stringify({
        "action": "subscribe",
        "events": ["policy_processed", "claim_registered", "premium_paid"]
    }));
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Nuovo evento:', data);
    
    switch(data.event_type) {
        case 'policy_processed':
            console.log('Polizza elaborata:', data.policy_id);
            break;
        case 'claim_registered':
            console.log('Sinistro registrato:', data.claim_id);
            break;
        case 'premium_paid':
            console.log('Premio pagato:', data.premium_id);
            break;
    }
};
```

## 📤 **Rate Limiting e Throttling**

### **Limiti API**
- **Anonymous**: 100 richieste/ora
- **Authenticated**: 1000 richieste/ora
- **Premium Tier**: 10000 richieste/ora

### **Headers di Rate Limiting**
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1692345600
```

### **Codici Errore Rate Limiting**
- `429 Too Many Requests`: Limite superato
- `Retry-After`: Secondi prima di riprovare

## 📋 **Error Handling**

### **Codici di Errore Standard**
```json
{
  "detail": "Messaggio di errore descrittivo",
  "error_code": "SPECIFIC_ERROR_CODE",
  "timestamp": "2025-08-18T10:30:45.123456"
}
```

### **Errori Comuni**
| Codice | Descrizione | Soluzione |
|--------|-------------|-----------|
| 400 | Bad Request | Verifica formato JSON |
| 401 | Unauthorized | Fornisci token JWT valido |
| 403 | Forbidden | Controlla permessi utente |
| 404 | Not Found | Verifica ID risorsa |
| 422 | Unprocessable Entity | Correggi dati input |
| 429 | Rate Limited | Attendi Retry-After |
| 500 | Internal Server Error | Contatta supporto |

## 🛠️ **SDK e Client Libraries**

### **Python SDK**
```python
from brokerflow_sdk import BrokerFlowClient

client = BrokerFlowClient(api_key="your-api-key")

# Analisi rischio
analysis = client.risk_analysis.analyze(client_id=123)
print(f"Risk Score: {analysis['risk_score']}")

# Dashboard compagnia
performance = client.company.get_performance(company_id=1)
print(f"Total Policies: {performance['kpi']['total_policies']}")
```

### **JavaScript SDK**
```javascript
import { BrokerFlow } from '@brokerflow/sdk';

const client = new BrokerFlow({ apiKey: 'your-api-key' });

// Analisi portafoglio
const analytics = await client.portfolio.getAnalytics();
console.log('Active Policies:', analytics.summary.active_policies);
```

### **Java SDK**
```java
import it.brokerflow.sdk.BrokerFlowClient;

BrokerFlowClient client = new BrokerFlowClient("your-api-key");

// Report compliance
ComplianceReport report = client.compliance().generateReport(
    ReportType.GDPR, 
    LocalDate.of(2025, 1, 1), 
    LocalDate.of(2025, 12, 31)
);
System.out.println("Report Generated: " + report.getTitle());
```

## 📊 **Webhooks e Callbacks**

### **Configurazione Webhook**
```http
POST /api/v1/webhooks
Content-Type: application/json

{
  "url": "https://your-system.com/webhooks/brokerflow",
  "events": ["policy_processed", "claim_registered"],
  "secret": "your-webhook-secret"
}
```

### **Payload Webhook**
```json
{
  "event_type": "policy_processed",
  "timestamp": "2025-08-18T10:30:45.123456",
  "data": {
    "policy_id": 12345,
    "client_id": 678,
    "risk_type": "Flotta Auto",
    "premium": 2500.00
  },
  "signature": "sha256-signature-here"
}
```

## 📈 **API Monitoring e SLA**

### **SLA Garantiti**
- **Uptime**: 99.9% (99.5% weekend/festivi)
- **Response Time**: < 200ms (95th percentile)
- **Throughput**: 1000 req/sec per istanza

### **Monitoring Endpoints**
```http
GET /api/v1/status/metrics
GET /api/v1/status/health
GET /api/v1/status/version
```

### **Alerting Thresholds**
- **Latency**: > 500ms → Warning, > 1000ms → Critical
- **Error Rate**: > 1% → Warning, > 5% → Critical
- **Availability**: < 99.9% → Critical

## 📞 **Supporto API Developer**

### **Risorse per Sviluppatori**
- **Documentazione Swagger**: https://api.brokerflow.it/docs
- **Sandbox Environment**: https://sandbox.api.brokerflow.it
- **Developer Portal**: https://developers.brokerflow.it
- **Community Forum**: https://community.brokerflow.it

### **Contatti Supporto Tecnico**
- **Email**: api-support@brokerflow.it
- **Slack**: developer-community.slack.com
- **Stack Overflow**: Tag `brokerflow-api`

---
*BrokerFlow AI API - Powering the Future of Insurance Technology*

**Version**: v2.1.0 | **Last Updated**: August 2025