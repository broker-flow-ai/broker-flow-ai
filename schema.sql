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
    name VARCHAR(255),
    company VARCHAR(255),
    email VARCHAR(255),
    sector VARCHAR(100),
    address TEXT,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE compliance_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_type ENUM('GDPR', 'SOX', 'IVASS'),
    period_start DATE,
    period_end DATE,
    content JSON,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    FOREIGN KEY (company_id) REFERENCES clients(id),
    FOREIGN KEY (broker_id) REFERENCES clients(id)
);

CREATE TABLE audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(100),
    action VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    details JSON
);