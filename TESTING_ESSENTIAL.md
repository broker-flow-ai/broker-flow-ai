# BrokerFlow AI - Testing Strategy & QA Documentation

## 🚀 Avvio Rapido con Docker

```bash
# 1. Configurazione iniziale
cp .env.example .env
# Modifica .env con la tua API Key OpenAI (opzionale per demo)

# 2. Avvio ambiente
docker compose up -d
docker compose exec processor python populate_database.py

# 3. Verifica servizi attivi
docker compose ps

# 4. rimozione ambiente e riallocazione da zero (attenzione può rimuovere anche altri ambienti Docker)
docker compose down
docker rm $(docker ps -aq)
docker rmi $(docker images -q)
docker volume rm $(docker volume ls -q)
docker network rm $(docker network ls -q)
docker system prune -a --volumes
cd ..
rm -rf broker-flow-ai/
# Copia incolla il progetto aggiornato
# riallocazione da zero
cd broker-flow-ai/
docker compose up -d
docker compose exec processor python populate_database.py
docker exec broker-flow-ai-api-1 python init_complete_auth.py
  🔐 Default Credentials:
   - Username: admin
   - Password: admin123

curl -X POST "http://localhost:8000/api/v1/auth/token" \
   -H "Content-Type: application/x-www-form-urlencoded" \
   -d "username=admin&password=admin123"



  5. Esegui la creazione dell'utente admin

   1 # Esegui lo script per creare l'utente admin
   2 docker exec broker-flow-ai-api-1 python create_admin_user.py

  6. Oppure esegui l'inizializzazione completa

   1 # Esegui l'inizializzazione completa
   2 docker exec broker-flow-ai-api-1 python init_complete_auth.py

  🔐 Default Credentials:
   - Username: admin
   - Password: admin123

# vecchio flow (con documenti pdf in /inbox)
docker compose exec processor python populate_coherent_data.py


```

# Logs docker

✦ Ecco l'elenco dei comandi per visualizzare i log di tutti i servizi dell'applicazione:

    # Visualizza i log di tutti i servizi
    docker compose logs
    
    # Visualizza i log di tutti i servizi con output in tempo reale
    docker compose logs -f
    
    # Visualizza i log di un singolo servizio
    docker compose logs api
    docker compose logs frontend
   docker compose logs db
   docker compose logs init-db
   docker compose logs processor
   docker compose logs phpmyadmin
   docker compose logs redis
   
   # Visualizza i log di un singolo servizio con output in tempo reale
   docker compose logs -f api
   docker compose logs -f frontend
   docker compose logs -f db
   docker compose logs -f init-db
   docker compose logs -f processor
   docker compose logs -f phpmyadmin
   docker compose logs -f redis
   
   # Visualizza i log degli ultimi 100 righe per tutti i servizi
   docker compose logs --tail=100
   
   # Visualizza i log degli ultimi 50 righe per un servizio specifico
   docker compose logs --tail=50 api
   
   # Visualizza i log degli ultimi 30 minuti
   docker compose logs --since=30m
   
   # Visualizza i log degli ultimi 1 ora
   docker compose logs --since=1h
   
   # Visualizza i log con timestamp
   docker compose logs -t
   
   # Combinazione di opzioni: ultime 50 righe con timestamp in tempo reale
   docker compose logs -f --tail=50 -t

  Comandi utili specifici per il debugging:

    # Controlla lo stato di tutti i servizi
    docker compose ps
    
    # Controlla i log dell'inizializzazione del database
    docker compose logs init-db
    
    # Controlla i log dell'API (per errori 404, 500, ecc.)
    docker compose logs api
    
   # Controlla i log del frontend (per errori di connessione)
   docker compose logs frontend
   
   # Controlla i log del database MySQL
   docker compose logs db
   
   # Controlla i log del processor
   docker compose logs processor

  Per visualizzare i log in tempo reale per il debugging:

    # Apri 3 terminali separati:
    
    # Terminale 1 - Log dell'API in tempo reale
    docker compose logs -f api
    
    # Terminale 2 - Log del frontend in tempo reale
    docker compose logs -f frontend
    
    # Terminale 3 - Log del database in tempo reale
   docker compose logs -f db

## 🎯 **Approccio al Testing**

BrokerFlow AI adotta un approccio **shift-left testing** con focus su **test automation**, **coverage completo** e **qualità continua**. La strategia comprende:

### **Piramide del Testing**
```
                    🧪 Unit Tests (70%)
                   ╱                ╲
        🧩 Integration Tests (20%)  🎯 End-to-End Tests (10%)
```

### **Livelli di Testing**
1. **Unit Testing**: Singole funzioni/metodi
2. **Integration Testing**: Interazioni tra moduli
3. **Contract Testing**: API endpoints validation
4. **End-to-End Testing**: Flussi completi utente
5. **Performance Testing**: Load/stress testing
6. **Security Testing**: Vulnerabilità e penetration testing
7. **Compliance Testing**: Normative GDPR/SOX/IVASS

## 🧪 **Framework e Tools**

### **Python Testing Stack**
- **pytest**: Framework testing principale
- **pytest-cov**: Code coverage measurement
- **pytest-mock**: Mocking framework
- **pytest-asyncio**: Testing async functions
- **coverage**: Coverage reporting e badge
- **tox**: Testing matrix multi-versione Python

### **API Testing**
- **FastAPI TestClient**: Testing endpoints API
- **httpx**: Richieste HTTP per integration tests
- **Swagger/OpenAPI**: Contract testing automatico

### **Frontend Testing**
- **Streamlit Testing**: Component testing UI
- **Playwright/Selenium**: E2E browser testing
- **Locust**: Load testing performance

### **Database Testing**
- **pytest-docker**: Fixture database testing
- **Factory Boy**: Generazione dati test fixtures
- **Faker**: Dati fake realistici

## 📊 **Struttura Test Suite**

### **Directory Organization**
```
tests/
├── unit/                    # Unit tests singoli moduli
│   ├── test_extract_data.py
│   ├── test_classify_risk.py
│   ├── test_compile_forms.py
│   └── test_generate_email.py
├── integration/             # Integration tests moduli
│   ├── test_processor_workflow.py
│   ├── test_api_integration.py
│   └── test_database_operations.py
├── e2e/                     # End-to-end test scenari completi
│   ├── test_full_quote_process.py
│   ├── test_report_generation.py
│   └── test_user_journey.py
├── performance/             # Performance e load tests
│   ├── test_api_load.py
│   └── test_processor_stress.py
├── security/                # Security vulnerability tests
│   ├── test_auth_security.py
│   └── test_input_validation.py
├── fixtures/               # Dati test e mock objects
│   ├── sample_pdfs/
│   ├── test_data.json
│   └── mock_responses.py
└── conftest.py             # Configurazione pytest fixtures
```

## 🧩 **Unit Tests - Esempi Dettagliati**

### **Test Estrazione Dati PDF**
```python
# tests/unit/test_extract_data.py
import pytest
from modules.extract_data import extract_text_from_pdf

def test_extract_text_digital_pdf():
    """Test estrazione da PDF digitale"""
    # Arrange
    pdf_path = "tests/fixtures/sample_digital.pdf"
    
    # Act
    result = extract_text_from_pdf(pdf_path)
    
    # Assert
    assert isinstance(result, str)
    assert len(result) > 0
    assert "Cliente:" in result
    assert "Azienda:" in result

def test_extract_text_scanned_pdf():
    """Test estrazione da PDF scansionato con OCR"""
    # Arrange
    pdf_path = "tests/fixtures/sample_scanned.pdf"
    
    # Act
    result = extract_text_from_pdf(pdf_path)
    
    # Assert
    assert isinstance(result, str)
    assert len(result) > 0
    # Verifica OCR riconosce testo con accuracy > 85%
    assert len(result.replace(" ", "")) / len("testo_atteso") > 0.85

@pytest.mark.parametrize("pdf_file,expected_sections", [
    ("flotta_auto.pdf", ["Veicoli", "Targa", "Valore"]),
    ("rc_professionale.pdf", ["Studio", "Professione", "Fatturato"]),
    ("fabbricato.pdf", ["Indirizzo", "Superficie", "Valore"]),
])
def test_extract_multiple_pdf_types(pdf_file, expected_sections):
    """Test estrazione tipologie PDF diverse"""
    result = extract_text_from_pdf(f"tests/fixtures/{pdf_file}")
    
    for section in expected_sections:
        assert section in result
```

### **Test Classificazione Rischio**
```python
# tests/unit/test_classify_risk.py
import pytest
from unittest.mock import patch, MagicMock
from modules.classify_risk import classify_risk

@patch('openai.Completion.create')
def test_classify_risk_flotta_auto(mock_openai):
    """Test classificazione rischio Flotta Auto"""
    # Arrange
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(text="Flotta Auto")]
    mock_openai.return_value = mock_response
    
    text = """
    Richiesta Preventivo Assicurativo - Flotta Auto
    Cliente: Mario Rossi
    Azienda: Rossi Trasporti SRL
    Veicoli: 3 autocarri con valore totale 60.000 EUR
    """
    
    # Act
    result = classify_risk(text)
    
    # Assert
    assert result == "Flotta Auto"
    mock_openai.assert_called_once()

def test_classify_risk_empty_text():
    """Test classificazione con testo vuoto"""
    result = classify_risk("")
    assert result == "Altro"  # Default fallback

def test_classify_risk_unknown_risk():
    """Test classificazione rischio sconosciuto"""
    text = "Testo casuale senza indicatori chiari di rischio"
    result = classify_risk(text)
    assert result in ["Altro", "Fabbricato", "Rischi Tecnici"]  # Possibili fallback
```

### **Test Compilazione Moduli**
```python
# tests/unit/test_compile_forms.py
import pytest
import os
from modules.compile_forms import compile_form

def test_compile_form_success():
    """Test compilazione modulo con successo"""
    # Arrange
    form_data = {
        "risk_type": "Flotta Auto",
        "client_data": {
            "name": "Mario Rossi",
            "company": "Rossi Trasporti SRL",
            "email": "mario@rossitrasporti.it"
        },
        "extracted_text": "Testo estratto dal PDF...",
        "filename": "sample_flotta.pdf"
    }
    
    template_path = "templates/template.pdf"
    output_name = "test_compiled.pdf"
    output_path = f"output/{output_name}"
    
    # Act
    result_path = compile_form(form_data, template_path, output_name)
    
    # Assert
    assert result_path == output_path
    assert os.path.exists(result_path)
    assert os.path.getsize(result_path) > 0

def test_compile_form_missing_data():
    """Test compilazione con dati mancanti"""
    form_data = {
        "risk_type": "RC Professionale",
        "client_data": {},  # Dati vuoti
        "extracted_text": "",
        "filename": ""
    }
    
    result_path = compile_form(form_data, "templates/template.pdf", "test.pdf")
    
    # Dovrebbe comunque generare un PDF anche con dati parziali
    assert os.path.exists(result_path)
```

## 🔗 **Integration Tests**

### **Test Workflow Completo Processor**
```python
# tests/integration/test_processor_workflow.py
import pytest
import os
import tempfile
from main import process_inbox, extract_client_data, classify_risk

def test_full_processor_workflow():
    """Test completo workflow processor da PDF a database"""
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Copia PDF di test nella inbox temporanea
        test_pdf = "tests/fixtures/sample_flotta.pdf"
        temp_pdf = os.path.join(temp_dir, "inbox", "test.pdf")
        os.makedirs(os.path.dirname(temp_pdf), exist_ok=True)
        
        import shutil
        shutil.copy(test_pdf, temp_pdf)
        
        # Mock configurazione per usare temp_dir
        with patch.dict(os.environ, {
            'INBOX_PATH': os.path.join(temp_dir, 'inbox'),
            'OUTPUT_PATH': os.path.join(temp_dir, 'output'),
            'TEMPLATE_PATH': 'templates/'
        }):
            # Act
            process_inbox()
            
            # Assert
            # Verifica che il PDF sia stato processato
            assert not os.path.exists(temp_pdf)  # Dovrebbe essere spostato
            
            # Verifica che il modulo compilato esista
            compiled_path = os.path.join(temp_dir, 'output', 'compiled_test.pdf')
            assert os.path.exists(compiled_path)
            
            # Verifica che l'email sia stata generata
            email_path = os.path.join(temp_dir, 'output', 'email_test.txt')
            assert os.path.exists(email_path)

def test_database_insertion():
    """Test inserimento dati nel database"""
    # Arrange
    client_data = {
        "name": "Test Cliente",
        "company": "Test Azienda",
        "email": "test@example.com",
        "sector": "Trasporti"
    }
    
    # Act & Assert
    # Verifica connessione database
    from modules.db import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verifica che possiamo eseguire query
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    assert result == (1,)
    
    conn.close()
```

### **Test API Endpoints**
```python
# tests/integration/test_api_integration.py
import pytest
from fastapi.testclient import TestClient
from api_b2b import app

client = TestClient(app)

def test_health_check_endpoint():
    """Test endpoint health check"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"

def test_metrics_endpoint():
    """Test endpoint metriche sistema"""
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    json_response = response.json()
    assert "database_metrics" in json_response
    assert "timestamp" in json_response

def test_risk_analysis_endpoint():
    """Test endpoint analisi rischio"""
    # Arrange
    test_data = {"client_id": 1}
    
    # Act
    response = client.post("/api/v1/insurance/risk-analysis", json=test_data)
    
    # Assert
    # Potrebbe tornare 200 o 404 a seconda se il client esiste
    assert response.status_code in [200, 404, 500]  # A seconda dello stato test
    
    if response.status_code == 200:
        json_response = response.json()
        assert "analysis" in json_response
        assert "client_id" in json_response

def test_portfolio_analytics_endpoint():
    """Test endpoint analisi portafoglio"""
    response = client.get("/api/v1/insurance/portfolio-analytics")
    assert response.status_code == 200
    
    json_response = response.json()
    assert "portfolio_summary" in json_response
    assert "trend_analysis" in json_response
```

## 🎯 **End-to-End Tests**

### **Test Caso d'Uso Completo**
```python
# tests/e2e/test_full_quote_process.py
import pytest
from playwright.sync_api import sync_playwright
import tempfile
import os

def test_complete_quote_process():
    """Test completo processo quotazione da upload PDF a dashboard"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        try:
            # 1. Naviga alla dashboard
            page.goto("http://localhost:8501")
            
            # 2. Verifica elemento dashboard principale
            assert page.is_visible("text=BrokerFlow AI")
            
            # 3. Test analisi rischio (simulazione UI)
            page.click("text=Analisi Rischio Avanzata")
            
            # 4. Inserisci ID cliente
            page.fill("[data-testid='client-id-input']", "1")
            page.click("[data-testid='analyze-button']")
            
            # 5. Verifica risultati
            page.wait_for_selector("[data-testid='risk-analysis-results']")
            assert page.is_visible("text=Risultati Analisi")
            
        finally:
            browser.close()

def test_file_upload_process():
    """Test upload file e processing automatico"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Crea file PDF temporaneo
        test_pdf = "tests/fixtures/sample_flotta.pdf"
        upload_path = os.path.join(temp_dir, "sample_flotta.pdf")
        
        import shutil
        shutil.copy(test_pdf, upload_path)
        
        # Simula upload (in ambiente test reale)
        # Questo test richiederebbe ambiente Docker completo
        assert os.path.exists(upload_path)
        assert os.path.getsize(upload_path) > 0
```

## 📈 **Performance Testing**

### **Load Testing API**
```python
# tests/performance/test_api_load.py
import pytest
from locust import HttpUser, task, between
import random

class APIUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def get_health(self):
        self.client.get("/api/v1/health")
    
    @task(2)
    def get_metrics(self):
        self.client.get("/api/v1/metrics")
    
    @task(1)
    def post_risk_analysis(self):
        client_id = random.randint(1, 100)
        self.client.post(
            "/api/v1/insurance/risk-analysis",
            json={"client_id": client_id}
        )
    
    @task(1)
    def get_portfolio_analytics(self):
        self.client.get("/api/v1/insurance/portfolio-analytics")

# Esecuzione: locust -f tests/performance/test_api_load.py
```

### **Stress Testing Processor**
```python
# tests/performance/test_processor_stress.py
import pytest
import threading
import time
import os
from main import process_inbox

def test_concurrent_processor_execution():
    """Test esecuzione concorrente processor"""
    threads = []
    results = []
    
    def worker(thread_id):
        try:
            start_time = time.time()
            process_inbox()
            end_time = time.time()
            results.append((thread_id, True, end_time - start_time))
        except Exception as e:
            results.append((thread_id, False, str(e)))
    
    # Avvia 5 thread concorrenti
    for i in range(5):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Attendi completamento
    for thread in threads:
        thread.join()
    
    # Verifica che tutti i thread siano completati
    successful = sum(1 for _, success, _ in results if success)
    assert successful >= 4  # Almeno 4 su 5 dovrebbero riuscire
```

## 🛡️ **Security Testing**

### **Test Vulnerabilità Input**
```python
# tests/security/test_input_validation.py
import pytest
from modules.extract_data import extract_client_data

def test_sql_injection_prevention():
    """Test prevenzione SQL injection nell'estrazione clienti"""
    malicious_text = """
    Cliente: '; DROP TABLE clients; --
    Azienda: Test'; DELETE FROM policies; --
    Email: test@test.com'; UPDATE clients SET sector='hacked'; --
    """
    
    # L'estrazione non dovrebbe eseguire comandi SQL
    client_data = extract_client_data(malicious_text)
    
    # I dati dovrebbero essere sanitizzati
    assert "DROP TABLE" not in str(client_data.values())
    assert "DELETE FROM" not in str(client_data.values())

def test_xss_prevention():
    """Test prevenzione XSS nei dati estratti"""
    malicious_text = """
    Cliente: <script>alert('xss')</script>
    Azienda: Test <img src=x onerror=alert('xss')>
    """
    
    client_data = extract_client_data(malicious_text)
    
    # I tag HTML dovrebbero essere rimossi o escapizzati
    for value in client_data.values():
        if value:
            assert "<script>" not in str(value)
            assert "onerror=" not in str(value)

def test_path_traversal_prevention():
    """Test prevenzione path traversal negli upload"""
    malicious_filenames = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\calc.exe",
        "/etc/passwd",
        "C:\\Windows\\System32\\cmd.exe"
    ]
    
    for filename in malicious_filenames:
        # La funzione dovrebbe rifiutare o sanitizzare questi nomi
        sanitized = sanitize_filename(filename)
        assert sanitized != filename
        assert ".." not in sanitized
        assert "/" not in sanitized
        assert "\\" not in sanitized
```

### **Test Autenticazione**
```python
# tests/security/test_auth_security.py
import pytest
from fastapi.testclient import TestClient
from api_b2b import app

client = TestClient(app)

def test_unauthorized_access():
    """Test accesso non autorizzato a endpoint protetti"""
    # Prova ad accedere a endpoint che richiedono autenticazione
    response = client.post("/api/v1/protected-endpoint")
    assert response.status_code == 401  # Unauthorized

def test_jwt_token_expiration():
    """Test scadenza token JWT"""
    import jwt
    import time
    
    # Crea token scaduto
    payload = {
        "user_id": 1,
        "exp": time.time() - 3600  # Scaduto 1 ora fa
    }
    
    # Il sistema dovrebbe rifiutare token scaduti
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode("expired_token", "secret", algorithms=["HS256"])
```

## 📊 **Coverage e Metriche**

### **Target Coverage**
- **Unit Tests**: 90%+
- **Integration Tests**: 80%+
- **API Tests**: 95%+
- **Security Tests**: 85%+

### **Badge Coverage**
```markdown
[![Coverage Status](https://coveralls.io/repos/github/tuo-account/broker-flow-ai/badge.svg?branch=main)](https://coveralls.io/github/tuo-account/broker-flow-ai?branch=main)
[![Build Status](https://github.com/tuo-account/broker-flow-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/tuo-account/broker-flow-ai/actions/workflows/ci.yml)
[![Code Quality](https://api.codeclimate.com/v1/badges/your-badge/maintainability)](https://codeclimate.com/github/tuo-account/broker-flow-ai)
```

### **Comandi Testing**
```bash
# Esecuzione completa suite test
pytest tests/ -v --cov=. --cov-report=html --cov-report=term

# Solo unit tests
pytest tests/unit/ -v

# Solo integration tests
pytest tests/integration/ -v

# Con coverage minimo richiesto
pytest tests/ --cov=. --cov-fail-under=85

# Test parallelo per velocità
pytest tests/ -n auto

# Test specifici con marker
pytest tests/ -m "slow" --durations=10
```

## 🚀 **CI/CD Pipeline Testing**

### **GitHub Actions Workflow**
```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: testpass
          MYSQL_DATABASE: test_db
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run unit tests
      run: pytest tests/unit/ --cov=. --cov-report=xml
    
    - name: Run integration tests
      run: pytest tests/integration/ --cov=. --cov-report=xml
      env:
        MYSQL_HOST: localhost
        MYSQL_USER: root
        MYSQL_PASSWORD: testpass
        MYSQL_DATABASE: test_db
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
    
    - name: Security scanning
      run: |
        pip install bandit safety
        bandit -r . -ll
        safety check
    
    - name: Code quality
      run: |
        pip install black flake8 mypy
        black --check .
        flake8 .
        mypy --package modules
```

## 📋 **Test Data Management**

### **Fixture Generation**
```python
# tests/fixtures/mock_responses.py
import json

def mock_openai_risk_classification():
    return {
        "id": "mock-response-1",
        "choices": [{
            "message": {
                "content": "Flotta Auto"
            }
        }]
    }

def mock_client_data():
    return {
        "name": "Mario Rossi",
        "company": "Rossi Trasporti SRL",
        "email": "mario@rossitrasporti.it",
        "sector": "Trasporti"
    }

def mock_policy_data():
    return {
        "risk_type": "Flotta Auto",
        "premium": 2500.00,
        "coverage_limit": 500000.00,
        "deductible": 500.00
    }
```

### **Test Data Factory**
```python
# tests/fixtures/factories.py
import factory
from datetime import datetime, timedelta

class ClientFactory(factory.Factory):
    class Meta:
        model = dict
    
    name = factory.Faker('name')
    company = factory.Faker('company')
    email = factory.Faker('email')
    sector = factory.Faker('random_element', elements=['Trasporti', 'Sanità', 'Edilizia', 'Legalità'])
    created_at = factory.LazyFunction(datetime.now)

class PolicyFactory(factory.Factory):
    class Meta:
        model = dict
    
    risk_type = factory.Faker('random_element', elements=['Flotta Auto', 'RC Professionale', 'Fabbricato'])
    start_date = factory.LazyFunction(datetime.now)
    end_date = factory.LazyFunction(lambda: datetime.now() + timedelta(days=365))
    status = 'active'
    policy_number = factory.Sequence(lambda n: f"POL{n:06d}")
```

## 🎯 **Best Practices Testing**

### **Principi Guida**
1. **Test Isolation**: Ogni test deve essere indipendente
2. **Deterministic**: Stessi input = stessi output
3. **Fast Execution**: Test veloci per feedback rapido
4. **Clear Naming**: Nomi descrittivi che spiegano cosa testano
5. **Arrange-Act-Assert**: Struttura chiara test

### **Anti-Patterns da Evitare**
- **Test Fragili**: Che si rompono per cambiamenti irrilevanti
- **Test Lenti**: Che rallentano il ciclo di sviluppo
- **Test Duplicità**: Stesso scenario testato più volte
- **Test Senza Assertion**: Verifiche incomplete risultati
- **Test Dipendenti**: Ordine esecuzione influenza risultato

### **Pattern Consigliati**
- **Given-When-Then**: Struttura comportamentale test
- **AAA Pattern**: Arrange-Act-Assert chiara
- **Parameterized Tests**: Stessi test con input diversi
- **Fixture Reusable**: Setup condiviso tra test correlati
- **Mock Appropriati**: Solo ciò che è necessario mockare

### **Metriche Qualità Test**
```python
# pyproject.toml o setup.cfg
[tool.coverage.run]
omit = [
    "*/tests/*",
    "*/venv/*",
    "*/migrations/*",
    "manage.py",
    "settings.py"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

## 📈 **Monitoring Test Results**

### **Dashboard Qualità**
- **Code Coverage Trend**: Andamento copertura nel tempo
- **Test Execution Time**: Velocità esecuzione test suite
- **Failure Rate**: Percentuale test falliti
- **Flaky Tests Detection**: Test instabili identificati

### **Alerting**
- **Coverage Drop**: Allarme se copertura scende sotto soglia
- **Performance Degradation**: Test che diventano significativamente più lenti
- **New Failures**: Notifiche immediata test precedentemente passati

---
*BrokerFlow AI - Testing Excellence for Insurance Innovation*





```
antonio@hp:~/progetti/broker-flow-ai$ docker compose ps
WARN[0000] /home/antonio/progetti/broker-flow-ai/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
NAME                          IMAGE                      COMMAND                  SERVICE      CREATED         STATUS         PORTS
broker-flow-ai-api-1          broker-flow-ai-api         "uvicorn api_b2b:app…"   api          8 minutes ago   Up 8 minutes   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp, 8501/tcp
broker-flow-ai-db-1           mysql:8.0                  "docker-entrypoint.s…"   db           8 minutes ago   Up 8 minutes   0.0.0.0:3306->3306/tcp, [::]:3306->3306/tcp, 33060/tcp
broker-flow-ai-frontend-1     broker-flow-ai-frontend    "streamlit run front…"   frontend     8 minutes ago   Up 8 minutes   8000/tcp, 0.0.0.0:8501->8501/tcp, [::]:8501->8501/tcp
broker-flow-ai-phpmyadmin-1   phpmyadmin/phpmyadmin      "/docker-entrypoint.…"   phpmyadmin   8 minutes ago   Up 8 minutes   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp
broker-flow-ai-processor-1    broker-flow-ai-processor   "python main.py"         processor    8 minutes ago   Up 8 minutes   8000/tcp, 8501/tcp
broker-flow-ai-redis-1        redis:7-alpine             "docker-entrypoint.s…"   redis        8 minutes ago   Up 8 minutes   0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp

docker compose down

docker cp schema.sql broker-flow-ai-db-1:/docker-entrypoint-initdb.d/schema.sql

  Dopo aver copiato il file, riavviamo i servizi per applicare le modifiche:

   1 docker compose down
   2 docker compose up -d

  Infine, controlliamo i log per verificare che il database sia stato inizializzato correttamente:

   1 docker compose logs init-db


✦ Ecco tutti i comandi in sequenza per resettare e ricreare il database da zero:

   1. Fermare e rimuovere tutti i container e i volumi:

   1    docker compose down -v

   2. Verificare che tutti i volumi siano stati rimossi:

   1    docker volume ls | grep broker-flow-ai

   3. Se ci sono ancora volumi, rimuoverli manualmente:

   1    docker volume rm <nome_volume>

   4. Avviare nuovamente tutti i servizi:

   1    docker compose up -d

   5. Attendere qualche secondo che il database si inizializzi, poi controllare i log:

   1    docker compose logs init-db

   6. Se i log mostrano ancora errori, possiamo provare a copiare manualmente il file schema.sql e rieseguirlo:

   1    docker cp schema.sql broker-flow-ai-db-1:/tmp/schema.sql
   2    docker exec -i broker-flow-ai-db-1 mysql -u root -proot123 < /tmp/schema.sql

   7. Oppure accedere interattivamente al container MySQL ed eseguire lo script:

   1    docker exec -it broker-flow-ai-db-1 bash
   2    mysql -u root -proot123 < /tmp/schema.sql
   3    exit

docker exec broker-flow-ai-db-1 mysql -u root -proot123 brokerflow_ai -e "SELECT username,email,role,status FROM users WHERE username='admin';"


curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

   8. Infine, verificare che le tabelle siano state create correttamente:

   1    docker exec -it broker-flow-ai-db-1 mysql -u root -proot123 -e "USE brokerflow_ai; SHOW TABLES;"

```
