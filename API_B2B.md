# BrokerFlow AI - API B2B2B Enterprise

## Panoramica

L'API B2B2B di BrokerFlow AI fornisce accesso programmatico a tutte le funzionalità della piattaforma, consentendo integrazioni complete con sistemi esterni come SGA, portali broker e applicazioni personalizzate.

## Endpoint Principali

### Analisi Rischio
```
POST /api/v1/insurance/risk-analysis
```
Analisi avanzata del rischio assicurativo con AI

### Dashboard Analytics
```
GET /api/v1/insurance/portfolio-analytics
GET /api/v1/insurance/company-performance
GET /api/v1/insurance/broker-performance
```
Analisi aggregata del portafoglio e performance KPI

### Compliance Reporting
```
POST /api/v1/insurance/compliance-report
GET /api/v1/insurance/compliance-reports
```
Generazione automatica di report di compliance

### AI Pricing & Underwriting
```
POST /api/v1/insurance/pricing-suggestion
POST /api/v1/insurance/claims-prediction
POST /api/v1/insurance/automated-underwriting
```
Suggerimenti di pricing, predizione sinistri e underwriting automatizzato

### Gestione Sconti & Fedeltà
```
POST /api/v1/insurance/discounts
GET /api/v1/insurance/discounts
GET /api/v1/insurance/discounted-premium
GET /api/v1/insurance/broker-metrics
```
Programmi sconto e metriche performance broker

### Emissione Polizza
```
POST /api/v1/insurance/policy-issuance
```
Processo completo di emissione polizza con integrazioni

## Autenticazione

Tutte le richieste API richiedono autenticazione tramite API key:

```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

## Esempi di Utilizzo

### Analisi Rischio
```bash
curl -X POST "https://api.brokerflow.ai/v1/insurance/risk-analysis" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"client_id": 123}'
```

### Generazione Report Compliance
```bash
curl -X POST "https://api.brokerflow.ai/v1/insurance/compliance-report" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "GDPR",
    "period_start": "2025-01-01",
    "period_end": "2025-12-31"
  }'
```

### Suggerimento Pricing
```bash
curl -X POST "https://api.brokerflow.ai/v1/insurance/pricing-suggestion" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "client_profile": {...},
    "risk_analysis": {...},
    "market_data": {...}
  }'
```

## Webhooks

L'API supporta webhooks per notifiche in tempo reale:

- `policy.issued` - Polizza emessa con successo
- `claim.filed` - Sinistro registrato
- `renewal.due` - Rinnovo in scadenza
- `compliance.report_generated` - Report compliance generato

## Rate Limiting

- **Free tier**: 100 requests/hour
- **Professional tier**: 1,000 requests/hour
- **Enterprise tier**: Custom limits

## SDK Disponibili

### Python SDK
```python
from brokerflow import BrokerFlowClient

client = BrokerFlowClient(api_key="YOUR_API_KEY")

# Analizza rischio cliente
analysis = client.risk_analysis(client_id=123)
print(analysis.risk_score)
```

### JavaScript SDK
```javascript
import { BrokerFlowClient } from '@brokerflow/sdk';

const client = new BrokerFlowClient({ apiKey: 'YOUR_API_KEY' });

// Genera report compliance
const report = await client.generateComplianceReport({
  reportType: 'GDPR',
  periodStart: '2025-01-01',
  periodEnd: '2025-12-31'
});
```

## Error Handling

### Codici di Stato HTTP
- `200`: Successo
- `201`: Creato
- `400`: Richiesta malformata
- `401`: Non autorizzato
- `403`: Accesso negato
- `404`: Risorsa non trovata
- `429`: Troppe richieste
- `500`: Errore interno del server

### Formato Errori
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Il parametro client_id è obbligatorio",
    "details": {
      "missing_field": "client_id"
    }
  }
}
```