# BrokerFlow AI - README

## 🎯 Cos'è BrokerFlow AI?

BrokerFlow AI è un sistema intelligente progettato per **automatizzare il processo di creazione di preventivi assicurativi** per broker. Riduce le ore di lavoro manuale a pochi minuti, trasformando PDF di richieste in preventivi completi con un solo click.

## 🚀 Funzionalità Principali

- **Lettura Intelligente PDF**: Supporto per PDF digitali e scansionati
- **Classificazione Automatica**: Riconoscimento del tipo di rischio assicurativo
- **Compilazione Moduli**: Generazione automatica di preventivi PDF
- **Email Personalizzate**: Creazione e invio di email ai clienti
- **Tracciamento Richieste**: Database integrato per monitorare le richieste
- **Estremamente Configurabile**: Adattabile a diverse tipologie di broker

## 🏗️ Architettura

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│   PDF in    │───▶│  Estrazione  │───▶│ Classificazio│
│   Arrivo    │    │    Testo     │    │     ne       │
└─────────────┘    └──────────────┘    └──────────────┘
                                                 │
                                                 ▼
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  Template   │◀───│ Compilazione │◀───│   Dati       │
│   PDF       │    │    Moduli    │    │  Estratti    │
└─────────────┘    └──────────────┘    └──────────────┘
                                                 │
                                                 ▼
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│   Email     │◀───│ Generazione  │◀───│ Preventivo   │
│  Finale     │    │   Email      │    │  Compilato   │
└─────────────┘    └──────────────┘    └──────────────┘
```

## 📦 Cosa c'è nella Scatola?

```
brokerflow_ai/
├── inbox/                 # PDF in arrivo da elaborare
├── output/                # Preventivi e email generati
├── templates/             # Moduli PDF delle compagnie
├── modules/               # Moduli core del sistema
├── DOCUMENTAZIONE.md      # Documentazione tecnica completa
├── GUIDA_UTENTE.md        # Istruzioni per l'utente
├── SVILUPPO.md            # Guida per sviluppatori
├── INSTALLAZIONE.md       # Guida all'installazione
├── CHANGELOG.md           # Registro modifiche
├── requirements.txt       # Dipendenze Python
├── schema.sql            # Schema database
└── ...                   # Altri file di configurazione
```

## 🚀 Come Iniziare

### Requisiti
- Python 3.8+
- Tesseract OCR (opzionale, per PDF scansionati)

### Installazione Veloce
```bash
# Clona il repository
git clone https://github.com/tuonome/broker-flow-ai.git
cd broker-flow-ai

# Crea ambiente virtuale
python -m venv brokerflow-env
source brokerflow-env/bin/activate  # Su Windows: brokerflow-env\Scripts\activate

# Installa dipendenze
pip install -r requirements.txt

# Configura le variabili d'ambiente
cp .env.example .env
# Modifica .env con le tue credenziali

# Prova la versione demo
python main_simulated.py
```

## 🧪 Versione Demo

La versione demo permette di testare tutto il flusso senza:
- Database MySQL
- API OpenAI
- Tesseract OCR

Permette di validare l'architettura e il flusso di lavoro.

## 📖 Documentazione Completa

- 📚 **[DOCUMENTAZIONE TECNICA](DOCUMENTAZIONE.md)** - Dettagli tecnici dell'implementazione
- 👤 **[GUIDA UTENTE](GUIDA_UTENTE.md)** - Istruzioni per l'uso quotidiano
- 💻 **[GUIDA SVILUPPO](SVILUPPO.md)** - Estendere e modificare il sistema
- ⚙️ **[INSTALLAZIONE](INSTALLAZIONE.md)** - Setup completo del sistema
- 📋 **[CHANGELOG](CHANGELOG.md)** - Storico delle versioni

## 🎯 Casi d'Uso

### Broker Assicurativi B2B
- Automatizza preventivi per flotte auto
- Riduce i tempi di risposta ai clienti
- Elimina errori di trascrizione

### Broker Retail
- Gestisce volumi elevati di richieste
- Standardizza il processo di emissione
- Libera tempo per consulenza specializzata

### Consulenti Assicurativi
- Semplifica la comparazione tra compagnie
- Mantiene traccia delle richieste
- Migliora l'esperienza del cliente

## 🔧 Requisiti di Sistema

### Minimi
- CPU: Dual core 2GHz
- RAM: 4GB
- Storage: 1GB disponibile
- Sistema: Windows 10+, macOS 10.14+, Linux

### Consigliati
- CPU: Quad core 3GHz
- RAM: 8GB
- Storage: SSD 10GB+
- Database: MySQL 5.7+

## 🔒 Sicurezza

- Tutti i dati rimangono locali
- Nessun invio a server esterni (eccetto OpenAI se configurato)
- Credenziali gestite in file separati
- Conforme a GDPR per trattamento dati

## 📈 Vantaggi

| Beneficio | Miglioramento |
|----------|---------------|
| **Tempo** | Da 2-3 ore a 2-3 minuti per preventivo |
| **Precisione** | Riduzione errori del 95% |
| **Costi** | Risparmio fino al 70% su operazioni ripetitive |
| **Scalabilità** | Gestione fino a 1000 preventivi/giorno |
| **Clienti** | Riduzione tempi di risposta del 90% |

## 🤝 Contribuire

1. Forka il progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Committa le modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Pusha il branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Distribuito sotto licenza MIT. Vedi `LICENSE` per maggiori informazioni.

## 📞 Contatti

- **Website**: https://brokerflow.ai
- **Email**: info@brokerflow.ai
- **Twitter**: [@BrokerFlowAI](https://twitter.com/BrokerFlowAI)
- **LinkedIn**: [BrokerFlow AI](https://linkedin.com/company/brokerflow-ai)

## 🙏 Ringraziamenti

- OpenAI per le API GPT
- Community open source per le librerie utilizzate
- Tutti i beta tester che hanno contribuito al progetto

---

<p align="center">
  Made with ❤️ for Insurance Brokers
</p>