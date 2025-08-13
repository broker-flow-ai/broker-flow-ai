# BrokerFlow AI - API Documentation

## 🚀 Overview

The BrokerFlow AI API provides programmatic access to all system functionalities, allowing integration with external systems like CRMs, email platforms, and custom applications.

**Base URL**: `https://api.brokerflow.ai/v1` (for cloud version)
**Local URL**: `http://localhost:8000/api/v1` (for self-hosted version)

## 🔐 Authentication

All API requests require authentication via API key.

### Headers
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

### API Key Management
- Generate API keys in the admin dashboard
- Keys can be scoped to specific permissions
- Keys can be revoked at any time

## 📁 Endpoints

### 1. Process PDF Requests

#### POST `/process/pdf`
Submit a PDF for processing

**Request**
```bash
curl -X POST "https://api.brokerflow.ai/v1/process/pdf" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/request.pdf" \
  -F "callback_url=https://yourapp.com/webhook"
```

**Parameters**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| file | file | Yes | PDF file to process |
| callback_url | string | No | URL for completion notification |
| priority | string | No | Processing priority (low/normal/high) |
| metadata | object | No | Custom metadata to attach |

**Response**
```json
{
  "request_id": "req_1234567890",
  "status": "processing",
  "received_at": "2025-08-13T10:30:00Z"
}
```

#### GET `/process/{request_id}`
Check processing status

**Response**
```json
{
  "request_id": "req_1234567890",
  "status": "completed",
  "completed_at": "2025-08-13T10:30:45Z",
  "result": {
    "risk_type": "Flotta Auto",
    "client": "Mario Rossi",
    "company": "Rossi Trasporti SRL",
    "policy_files": [
      "https://api.brokerflow.ai/v1/files/policy_1234567890.pdf"
    ],
    "email_content": "https://api.brokerflow.ai/v1/files/email_1234567890.txt"
  }
}
```

### 2. Risk Classification

#### POST `/classify/risk`
Classify text for risk type

**Request**
```json
{
  "text": "Richiesta polizza RC Professionale per medico chirurgo...",
  "detailed": true
}
```

**Response**
```json
{
  "risk_type": "RC Professionale",
  "confidence": 0.95,
  "details": {
    "profession": "Medico Chirurgo",
    "coverage_suggestion": "500.000 EUR"
  }
}
```

### 3. PDF Compilation

#### POST `/compile/form`
Compile a PDF form with data

**Request**
```json
{
  "template_id": "allianz_flotta",
  "data": {
    "cliente": "Mario Rossi",
    "azienda": "Rossi Trasporti SRL",
    "veicoli": [
      {
        "targa": "AB123CD",
        "tipo": "Autocarro",
        "anno": "2018",
        "valore": "18000"
      }
    ]
  }
}
```

**Response**
```json
{
  "file_id": "compiled_1234567890",
  "download_url": "https://api.brokerflow.ai/v1/files/compiled_1234567890.pdf",
  "expires_at": "2025-08-14T10:30:45Z"
}
```

### 4. Email Generation

#### POST `/generate/email`
Generate email content

**Request**
```json
{
  "template": "quote_followup",
  "client_name": "Mario Rossi",
  "policy_files": ["policy_1234567890.pdf"],
  "custom_fields": {
    "premium": "1.250 EUR",
    "coverage": "RC Auto + Furto/Incendio"
  }
}
```

**Response**
```json
{
  "subject": "Il suo preventivo assicurativo - Rossi Trasporti",
  "body": "Gentile Mario Rossi,

In allegato trova il preventivo...",
  "html_body": "<html>...</html>"
}
```

### 5. Database Queries

#### GET `/requests`
List processing requests

**Parameters**
| Name | Type | Description |
|------|------|-------------|
| status | string | Filter by status |
| date_from | string | ISO date |
| date_to | string | ISO date |
| limit | integer | Results per page |
| offset | integer | Pagination offset |

**Response**
```json
{
  "requests": [
    {
      "request_id": "req_1234567890",
      "filename": "flotta_rossi.pdf",
      "status": "completed",
      "risk_type": "Flotta Auto",
      "processed_at": "2025-08-13T10:30:45Z"
    }
  ],
  "total": 1,
  "limit": 10,
  "offset": 0
}
```

#### GET `/clients`
List clients

**Response**
```json
{
  "clients": [
    {
      "client_id": "client_1234567890",
      "name": "Mario Rossi",
      "company": "Rossi Trasporti SRL",
      "email": "mario@rossitrasporti.it",
      "policies_count": 3
    }
  ]
}
```

#### GET `/policies`
List policies

**Response**
```json
{
  "policies": [
    {
      "policy_id": "pol_1234567890",
      "client_id": "client_1234567890",
      "risk_type": "Flotta Auto",
      "company": "Allianz",
      "premium": "1250.00",
      "start_date": "2025-09-01",
      "end_date": "2026-09-01",
      "status": "active"
    }
  ]
}
```

### 6. Templates Management

#### GET `/templates`
List available templates

**Response**
```json
{
  "templates": [
    {
      "template_id": "allianz_flotta",
      "name": "Allianz - Flotta Auto",
      "risk_type": "Flotta Auto",
      "fields": ["cliente", "azienda", "veicoli"]
    }
  ]
}
```

#### POST `/templates`
Create new template

**Request**
```json
{
  "name": "Unipol RC Professionale",
  "risk_type": "RC Professionale",
  "file": "base64_encoded_pdf_template"
}
```

### 7. Webhooks

#### POST `/webhooks`
Receive processing completion notifications

**Payload**
```json
{
  "event": "processing.completed",
  "request_id": "req_1234567890",
  "timestamp": "2025-08-13T10:30:45Z",
  "result": {
    "risk_type": "Flotta Auto",
    "policy_files": ["policy_1234567890.pdf"]
  }
}
```

## 📊 Rate Limiting

- **Free tier**: 100 requests/hour
- **Professional tier**: 1,000 requests/hour
- **Enterprise tier**: Custom limits

Exceeding limits returns `429 Too Many Requests`.

## 📈 Webhook Events

| Event | Description |
|-------|-------------|
| `processing.started` | PDF processing has begun |
| `processing.completed` | PDF processing finished successfully |
| `processing.failed` | PDF processing failed |
| `email.sent` | Email was sent to client |
| `policy.created` | New policy was created |
| `renewal.upcoming` | Policy renewal is approaching |

## 🛠 Error Handling

### HTTP Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `429`: Too Many Requests
- `500`: Internal Server Error

### Error Response Format
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "The request is missing required fields",
    "details": {
      "missing_fields": ["file"]
    }
  }
}
```

## 🧪 SDKs

### Python SDK
```python
from brokerflow import BrokerFlowClient

client = BrokerFlowClient(api_key="YOUR_API_KEY")

# Process a PDF
with open("request.pdf", "rb") as f:
    result = client.process_pdf(f)
    print(result.request_id)
```

### JavaScript SDK
```javascript
import { BrokerFlowClient } from '@brokerflow/sdk';

const client = new BrokerFlowClient({ apiKey: 'YOUR_API_KEY' });

// Process a PDF
const fileInput = document.getElementById('file');
const result = await client.processPDF(fileInput.files[0]);
console.log(result.requestId);
```

## 🔌 Integration Examples

### CRM Integration
```python
# Sync processed requests to CRM
def sync_to_crm(request_id):
    result = client.get_request(request_id)
    crm_client.create_opportunity({
        'client_name': result.client,
        'policy_type': result.risk_type,
        'status': 'quote_sent'
    })
```

### Email Integration
```python
# Send email through SMTP
def send_email(request_id):
    result = client.get_request(request_id)
    email_content = client.download_file(result.email_content)
    
    smtp_client.send({
        'to': result.client_email,
        'subject': email_content.subject,
        'body': email_content.body,
        'attachments': result.policy_files
    })
```

## 📞 Support

For API questions and support:
- Email: api@brokerflow.ai
- Documentation: https://docs.brokerflow.ai
- Status: https://status.brokerflow.ai

---

*Last updated: August 13, 2025*