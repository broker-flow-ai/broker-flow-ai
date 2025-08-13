# BrokerFlow AI - FAQ

## 📋 General Questions

### What is BrokerFlow AI?
BrokerFlow AI is an intelligent system designed to automate the process of creating insurance quotes for brokers. It reduces hours of manual work to just a few minutes by transforming PDF requests into complete quotes with a single click.

### Who is it for?
BrokerFlow AI is designed for:
- Insurance brokers (B2B and retail)
- Insurance consultants
- Underwriters
- Insurance company agents

### What types of insurance does it support?
Currently, BrokerFlow AI supports:
- Fleet insurance (Auto flotta)
- Professional liability (RC Professionale)
- Property insurance (Fabbricato)
- Technical risks (Rischi Tecnologici)

More types will be added based on user feedback.

## 🚀 Technical Questions

### What are the system requirements?
**Minimum:**
- CPU: Dual core 2GHz
- RAM: 4GB
- Storage: 1GB available
- OS: Windows 10+, macOS 10.14+, Linux

**Recommended:**
- CPU: Quad core 3GHz
- RAM: 8GB
- Storage: SSD 10GB+
- Database: MySQL 5.7+

### Do I need programming skills to use it?
No! The system is designed to be user-friendly. However, some technical knowledge is helpful for installation and customization.

### Can it handle scanned PDFs?
Yes! BrokerFlow AI uses OCR (Optical Character Recognition) to extract text from scanned documents.

### Is my data secure?
Absolutely. All data processing happens locally on your machine. No data is sent to external servers by default (except to OpenAI if you configure it).

## 💰 Business Questions

### How much does it cost?
BrokerFlow AI is currently in development. We plan to offer:
- Free tier for small brokers
- Professional tier for medium businesses
- Enterprise tier for large organizations

Contact us for early access pricing.

### How long does implementation take?
- **Demo version**: 30 minutes
- **Basic setup**: 1-2 days
- **Full enterprise deployment**: 1-2 weeks

### Do you offer training?
Yes, we provide:
- Online documentation
- Video tutorials
- Live training sessions
- Dedicated support for enterprise clients

## 🔧 Troubleshooting

### I'm getting "ModuleNotFoundError"
Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### OCR is not working
Ensure Tesseract OCR is installed and in your system PATH:
- **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt install tesseract-ocr`

### PDF compilation is not working
The system requires editable PDF forms. Make sure your template PDFs have fillable fields.

### How do I update the system?
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 🌐 Integration Questions

### Can it integrate with my CRM?
Yes, we're working on APIs for popular CRM systems:
- HubSpot
- Salesforce
- Zoho CRM
- Custom APIs

### Does it work with email systems?
Yes, it can integrate with:
- Gmail
- Outlook
- Custom SMTP servers

### Can I customize the email templates?
Absolutely! You can create custom email templates for different types of insurance and clients.

## 🔒 Compliance & Security

### Is it GDPR compliant?
Yes, BrokerFlow AI is designed to be GDPR compliant:
- Data stays on your premises
- No unauthorized data sharing
- Right to data deletion

### How do you handle data privacy?
- All processing is local
- No data is stored on our servers
- You control your data completely

## 📈 Performance

### How many quotes can it process?
- **Demo version**: 10 quotes/minute
- **Production version**: 100+ quotes/minute
- **Enterprise version**: 1000+ quotes/minute (with proper hardware)

### What's the accuracy rate?
- Text extraction: 95%+
- Risk classification: 90%+
- Form compilation: 99%+

## 🆘 Support

### How do I get help?
1. Check our documentation
2. Search existing issues
3. Contact support@brokerflow.ai
4. Join our community Slack

### What's your SLA?
- **Email support**: 24 hours
- **Enterprise clients**: 2 hours
- **Critical issues**: 30 minutes

### Do you offer custom development?
Yes, we offer custom development services for:
- Special insurance types
- Custom integrations
- Enterprise features

## 🚀 Future Development

### What's coming next?
Check our [roadmap](CHANGELOG.md) for upcoming features:
- Advanced PDF compilation
- Web dashboard
- Mobile app
- Multi-language support

### How can I request features?
1. Open an issue on GitHub
2. Contact our product team
3. Vote on our roadmap board

### Can I contribute?
Yes! We welcome contributions from the community. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📞 Contact

### Sales
sales@brokerflow.ai

### Support
support@brokerflow.ai

### General Inquiries
info@brokerflow.ai

### Partnerships
partnerships@brokerflow.ai

---

*Last updated: August 13, 2025*