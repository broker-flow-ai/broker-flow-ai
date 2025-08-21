#!/bin/bash
# Script completo per configurare l'ambiente BrokerFlow AI con dati realistici

echo "=== Configurazione completa dell'ambiente BrokerFlow AI ==="
echo

# 1. Pulizia dell'ambiente precedente
echo "1. Pulizia dell'ambiente precedente..."
docker compose down -v
rm -f inbox/*.pdf
echo "✓ Pulizia completata"
echo

# 2. Rigenerazione dei PDF con informazioni settoriali
echo "2. Rigenerazione dei PDF con informazioni settoriali..."
python create_sample_pdf.py
python create_sample_pdf_rc.py
python create_additional_samples.py
echo "✓ PDF rigenerati"
echo

# 3. Verifica del contenuto dei PDF
echo "3. Verifica del contenuto dei PDF..."
echo "Contenuto di sample_flotta.pdf:"
head -5 inbox/sample_flotta.pdf
echo
echo "Contenuto di sample_rc_professionale.pdf:"
head -5 inbox/sample_rc_professionale.pdf
echo "✓ Verifica PDF completata"
echo

# 4. Avvio dell'ambiente Docker
echo "4. Avvio dell'ambiente Docker..."
docker compose up -d
echo "✓ Ambiente Docker avviato"
echo

# 5. Attesa per l'inizializzazione del database e elaborazione dei PDF
echo "5. Attesa per l'inizializzazione del database e elaborazione dei PDF..."
sleep 30
echo "✓ Attesa completata"
echo

# 6. Verifica dell'elaborazione dei PDF
echo "6. Verifica dell'elaborazione dei PDF..."
docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "SELECT filename, status FROM request_queue;"
echo

# 7. Verifica dei clienti estratti
echo "7. Verifica dei clienti estratti..."
docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "SELECT id, name, company, sector, email FROM clients WHERE name != 'Unknown' LIMIT 10;"
echo

# 8. Popolamento dei dati realistici
echo "8. Popolamento dei dati realistici..."
docker compose exec init-db python populate_realistic_data.py
echo "✓ Dati realistici popolati"
echo

# 9. Popolamento dell'audit log
echo "9. Popolamento dell'audit log..."
docker compose exec init-db python populate_audit_log.py
echo "✓ Audit log popolato"
echo

# 10. Verifica finale dei dati
echo "10. Verifica finale dei dati..."
echo
echo "Clienti con settore:"
docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "SELECT id, name, sector FROM clients WHERE sector IS NOT NULL AND sector != 'Unknown' LIMIT 10;"
echo
echo "Polizze per cliente:"
docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "SELECT c.name, c.sector, COUNT(p.id) as policies_count FROM clients c JOIN risks r ON c.id = r.client_id JOIN policies p ON r.id = p.risk_id GROUP BY c.id, c.name, c.sector ORDER BY policies_count DESC;"
echo
echo "Sinistri registrati:"
docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "SELECT COUNT(*) as total_claims FROM claims;"
echo
echo "Audit log entries:"
docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "SELECT COUNT(*) as audit_entries FROM audit_log;"
echo

# 11. Informazioni per l'utilizzo
echo "=== Configurazione completata! ==="
echo
echo "Puoi accedere a:"
echo "- Dashboard: http://localhost:8501"
echo "- API: http://localhost:8000"
echo "- phpMyAdmin: http://localhost:8080"
echo
echo "Clienti disponibili per l'analisi di rischio (usa gli ID mostrati sopra):"
docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "SELECT id, name, sector FROM clients WHERE sector IS NOT NULL AND sector != 'Unknown';"
echo
echo "Per testare l'analisi di rischio, usa un ID cliente dalla lista sopra."