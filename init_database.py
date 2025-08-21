#!/bin/bash
# Script di inizializzazione del database

# Attendi che il database sia pronto
echo "Attendo che il database sia pronto..."
sleep 10

# Esegui lo script per popolare i dati realistici
echo "Popolazione dei dati realistici..."
python /app/populate_realistic_data.py

# Esegui lo script per popolare l'audit log
echo "Popolazione dell'audit log..."
python /app/populate_audit_log.py

echo "Inizializzazione completata!"