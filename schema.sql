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
    email VARCHAR(255)
);

CREATE TABLE risks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    risk_type VARCHAR(100),
    details JSON,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE policies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    risk_id INT,
    company VARCHAR(100),
    policy_pdf_path VARCHAR(255),
    FOREIGN KEY (risk_id) REFERENCES risks(id)
);