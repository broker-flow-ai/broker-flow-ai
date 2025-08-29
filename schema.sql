CREATE DATABASE IF NOT EXISTS brokerflow_ai;
USE brokerflow_ai;

CREATE TABLE request_queue (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255),
    status ENUM('pending', 'processed', 'error') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    -- Informazioni di base
    name VARCHAR(255) COMMENT 'Nome completo del cliente (persona fisica o rappresentante legale)',
    company VARCHAR(255) COMMENT 'Denominazione azienda (se applicabile)',
    client_type ENUM('individual', 'company', 'freelance', 'public_entity') DEFAULT 'individual' COMMENT 'Tipologia di cliente',
    
    -- Contatti
    email VARCHAR(255),
    phone VARCHAR(20),
    mobile VARCHAR(20) COMMENT 'Numero cellulare',
    fax VARCHAR(20) COMMENT 'Numero fax',
    
    -- Indirizzi
    address TEXT COMMENT 'Indirizzo principale',
    city VARCHAR(100) COMMENT 'Città',
    province VARCHAR(100) COMMENT 'Provincia',
    postal_code VARCHAR(10) COMMENT 'Codice postale',
    country VARCHAR(100) DEFAULT 'Italy' COMMENT 'Nazione',
    
    -- Dati fiscali
    fiscal_code VARCHAR(16) COMMENT 'Codice fiscale (persona fisica o società)',
    vat_number VARCHAR(11) COMMENT 'Partita IVA',
    tax_regime VARCHAR(50) COMMENT 'Regime fiscale',
    sdi_code VARCHAR(7) COMMENT 'Codice SDI per fatturazione elettronica',
    pec_email VARCHAR(255) COMMENT 'Email PEC',
    
    -- Dati legali per società
    legal_form VARCHAR(100) COMMENT 'Forma giuridica (SRL, SPA, etc.)',
    company_registration_number VARCHAR(50) COMMENT 'Numero iscrizione registro imprese',
    rea_office VARCHAR(50) COMMENT 'Ufficio REA',
    rea_number VARCHAR(50) COMMENT 'Numero REA',
    share_capital DECIMAL(15,2) COMMENT 'Capitale sociale',
    vat_settlement ENUM('monthly', 'quarterly', 'annual') COMMENT 'Periodicità liquidazione IVA',
    
    -- Dati bancari
    iban VARCHAR(34) COMMENT 'IBAN per addebito diretto premio',
    bank_name VARCHAR(100) COMMENT 'Nome banca',
    bank_iban VARCHAR(34) COMMENT 'IBAN alternativo',
    
    -- Classificazioni
    sector VARCHAR(100) COMMENT 'Settore merceologico/attività principale',
    customer_segment VARCHAR(50) COMMENT 'Segmento cliente (premium, standard, ecc.)',
    customer_status ENUM('active', 'inactive', 'prospect') DEFAULT 'active' COMMENT 'Stato del cliente',
    referred_by VARCHAR(255) COMMENT 'Fonte di acquisizione cliente',
    
    -- Date importanti
    birth_date DATE COMMENT 'Data di nascita (persone fisiche)',
    birth_place VARCHAR(100) COMMENT 'Luogo di nascita (persone fisiche)',
    establishment_date DATE COMMENT 'Data costituzione (società)',
    
    -- Note e preferenze
    notes TEXT COMMENT 'Note interne',
    preferred_communication ENUM('email', 'phone', 'mail', 'pec') COMMENT 'Canale di comunicazione preferito',
    language VARCHAR(10) DEFAULT 'it' COMMENT 'Lingua preferita',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE risks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    broker_id INT,
    risk_type VARCHAR(100),
    details JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (broker_id) REFERENCES clients(id)
);

-- Tabella per i sottoscrittori delle polizze
CREATE TABLE policy_subscribers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    policy_id INT NOT NULL COMMENT 'ID della polizza',
    subscriber_type ENUM('primary', 'co_subscriber', 'beneficiary') DEFAULT 'primary' COMMENT 'Tipo di sottoscrittore',
    entity_type ENUM('individual', 'company') NOT NULL COMMENT 'Tipo di entità',
    
    -- Informazioni personali per persone fisiche
    first_name VARCHAR(100) COMMENT 'Nome',
    last_name VARCHAR(100) COMMENT 'Cognome',
    fiscal_code VARCHAR(16) COMMENT 'Codice fiscale',
    birth_date DATE COMMENT 'Data di nascita',
    birth_place VARCHAR(100) COMMENT 'Luogo di nascita',
    
    -- Informazioni per aziende
    company_name VARCHAR(255) COMMENT 'Denominazione azienda',
    vat_number VARCHAR(11) COMMENT 'Partita IVA',
    legal_form VARCHAR(100) COMMENT 'Forma giuridica',
    
    -- Contatti
    email VARCHAR(255),
    phone VARCHAR(20),
    mobile VARCHAR(20),
    
    -- Indirizzo
    address TEXT,
    city VARCHAR(100),
    province VARCHAR(100),
    postal_code VARCHAR(10),
    country VARCHAR(100) DEFAULT 'Italy',
    
    -- Relazioni
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    -- Rimosso temporaneamente il riferimento a policies(id) per evitare dipendenza circolare
);

-- Tabella per i delegati al pagamento dei premi
CREATE TABLE premium_delegates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL COMMENT 'ID del cliente',
    delegate_type ENUM('individual', 'company') NOT NULL COMMENT 'Tipo di delegato',
    
    -- Informazioni personali per persone fisiche
    first_name VARCHAR(100) COMMENT 'Nome',
    last_name VARCHAR(100) COMMENT 'Cognome',
    fiscal_code VARCHAR(16) COMMENT 'Codice fiscale',
    
    -- Informazioni per aziende
    company_name VARCHAR(255) COMMENT 'Denominazione azienda',
    vat_number VARCHAR(11) COMMENT 'Partita IVA',
    
    -- Contatti
    email VARCHAR(255),
    phone VARCHAR(20),
    mobile VARCHAR(20),
    
    -- Indirizzo
    address TEXT,
    city VARCHAR(100),
    province VARCHAR(100),
    postal_code VARCHAR(10),
    country VARCHAR(100) DEFAULT 'Italy',
    
    -- Autorizzazioni
    authorization_level ENUM('full', 'limited', 'specific_policy') DEFAULT 'full' COMMENT 'Livello di autorizzazione',
    authorization_start DATE COMMENT 'Data inizio autorizzazione',
    authorization_end DATE COMMENT 'Data fine autorizzazione',
    is_active BOOLEAN DEFAULT TRUE COMMENT 'Autorizzazione attiva',
    
    -- Relazioni
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    -- Rimosso temporaneamente il riferimento a clients(id) per evitare dipendenza circolare
);

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
    
    -- Informazioni di sottoscrizione
    subscription_date DATE COMMENT 'Data sottoscrizione',
    subscription_method ENUM('digital', 'paper', 'agent') DEFAULT 'digital' COMMENT 'Metodo di sottoscrizione',
    
    -- Premio e pagamento
    premium_amount DECIMAL(15,2) COMMENT 'Importo premio totale',
    premium_frequency ENUM('annual', 'semiannual', 'quarterly', 'monthly') DEFAULT 'annual' COMMENT 'Frequenza pagamento',
    payment_method ENUM('direct_debit', 'bank_transfer', 'credit_card', 'cash', 'check') COMMENT 'Metodo di pagamento',
    
    -- Sottoscrittori (riferimento alla tabella policy_subscribers)
    primary_subscriber_id INT COMMENT 'ID del sottoscrittore principale',
    
    -- Delegati pagamento (riferimento alla tabella premium_delegates)
    premium_delegate_id INT COMMENT 'ID del delegato al pagamento',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (risk_id) REFERENCES risks(id),
    FOREIGN KEY (company_id) REFERENCES clients(id)
    -- Rimossi temporaneamente i riferimenti a policy_subscribers e premium_delegates
    -- che saranno aggiunti dopo la creazione di tutte le tabelle
);

CREATE TABLE claims (
    id INT AUTO_INCREMENT PRIMARY KEY,
    policy_id INT,
    claim_date DATE,
    amount DECIMAL(10,2),
    status ENUM('open', 'in_review', 'approved', 'rejected') DEFAULT 'open',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (policy_id) REFERENCES policies(id)
);

CREATE TABLE premiums (
    id INT AUTO_INCREMENT PRIMARY KEY,
    policy_id INT,
    amount DECIMAL(10,2),
    due_date DATE,
    payment_status ENUM('pending', 'paid', 'overdue') DEFAULT 'pending',
    payment_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (policy_id) REFERENCES policies(id)
);

CREATE TABLE risk_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    risk_score DECIMAL(5,2),
    sector_analysis TEXT,
    pricing_recommendation TEXT,
    recommendation_level ENUM('Alto', 'Medio', 'Basso'),
    underwriting_notes TEXT,
    full_analysis JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE compliance_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_type ENUM('GDPR', 'SOX', 'IVASS'),
    period_start DATE,
    period_end DATE,
    content JSON,
    file_path VARCHAR(500),
    excel_path VARCHAR(500),
    word_path VARCHAR(500),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE discounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT,
    broker_id INT,
    discount_type VARCHAR(50),
    discount_percentage DECIMAL(5,2),
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES clients(id),
    FOREIGN KEY (broker_id) REFERENCES clients(id)
);

CREATE TABLE audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(100),
    action VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    details JSON,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE email_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_id INT,
    recipient_email VARCHAR(255),
    format_type VARCHAR(50),
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES compliance_reports(id) ON DELETE CASCADE
);

CREATE TABLE claim_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    claim_id INT,
    document_name VARCHAR(255),
    document_type VARCHAR(50),
    file_path VARCHAR(500),
    file_size INT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (claim_id) REFERENCES claims(id) ON DELETE CASCADE
);

CREATE TABLE claim_communications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    claim_id INT,
    sender VARCHAR(255),
    recipient VARCHAR(255),
    subject VARCHAR(255),
    message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('sent', 'delivered', 'read') DEFAULT 'sent',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (claim_id) REFERENCES claims(id) ON DELETE CASCADE
);

-- Aggiungiamo ora i riferimenti alle chiavi esterne per policy_subscribers e premium_delegates
-- Rimuoviamo le chiavi esterne che causano dipendenze circolari
-- ALTER TABLE policy_subscribers ADD CONSTRAINT fk_policy_subscribers_policy_id FOREIGN KEY (policy_id) REFERENCES policies(id) ON DELETE CASCADE;
-- ALTER TABLE premium_delegates ADD CONSTRAINT fk_premium_delegates_client_id FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE;
ALTER TABLE policies ADD CONSTRAINT fk_policies_primary_subscriber_id FOREIGN KEY (primary_subscriber_id) REFERENCES policy_subscribers(id);
ALTER TABLE policies ADD CONSTRAINT fk_policies_premium_delegate_id FOREIGN KEY (premium_delegate_id) REFERENCES premium_delegates(id);