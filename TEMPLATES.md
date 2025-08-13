# BrokerFlow AI - Project Templates

This directory contains template files used by the BrokerFlow AI system.

## Template Types

### 1. Email Templates
- `email_quote.html`: Template for insurance quote emails
- `email_renewal.html`: Template for policy renewal notifications
- `email_error.html`: Template for error notifications
- `email_welcome.html`: Template for new user welcome emails

### 2. PDF Templates
- `template_flotta_allianz.pdf`: Allianz fleet insurance template
- `template_rc_professionale_unipol.pdf`: Unipol professional liability template
- `template_fabbricato_tua.pdf`: TUA property insurance template
- `template_rischi_tecnici_generali.pdf`: Generali technical risks template

### 3. Report Templates
- `report_daily.html`: Daily processing report
- `report_weekly.html`: Weekly performance report
- `report_monthly.html`: Monthly business report
- `report_annual.html`: Annual summary report

### 4. Document Templates
- `document_quote.pdf`: Standard quote document template
- `document_policy.pdf`: Policy document template
- `document_invoice.pdf`: Invoice document template
- `document_certificate.pdf`: Certificate document template

## Template Structure

### Email Templates
Email templates use Jinja2 syntax for variable substitution:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ subject }}</title>
</head>
<body>
    <h1>Gentile {{ client_name }},</h1>
    <p>In allegato trova il preventivo richiesto per {{ insurance_type }}.</p>
    <p>Importo premio: <strong>{{ premium_amount }}</strong></p>
    <p>Per qualsiasi dubbio, siamo a disposizione.</p>
    <p>Cordiali saluti,<br>{{ broker_name }}</p>
</body>
</html>
```

### PDF Templates
PDF templates should be fillable forms with named fields that match the data structure:

- Client information fields:
  - `cliente_nome`
  - `cliente_cognome`
  - `cliente_azienda`
  - `cliente_indirizzo`
  - `cliente_email`
  - `cliente_telefono`

- Policy information fields:
  - `polizza_tipo`
  - `polizza_numero`
  - `polizza_data_inizio`
  - `polizza_data_fine`
  - `polizza_importo`
  - `polizza_massimali`

- Vehicle information fields (for fleet insurance):
  - `veicolo_targa_1`
  - `veicolo_tipo_1`
  - `veicolo_anno_1`
  - `veicolo_valore_1`

### Report Templates
Report templates use Jinja2 syntax with data tables and charts:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Report {{ report_type }} - {{ period }}</title>
</head>
<body>
    <h1>Report {{ report_name }}</h1>
    <h2>Periodo: {{ period_start }} - {{ period_end }}</h2>
    
    <div class="metrics">
        <div class="metric">
            <h3>Richieste Processate</h3>
            <p>{{ requests_processed }}</p>
        </div>
        <div class="metric">
            <h3>Tempo Medio</h3>
            <p>{{ average_time }} secondi</p>
        </div>
        <div class="metric">
            <h3>Accuratezza</h3>
            <p>{{ accuracy }}%</p>
        </div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Tipo Polizza</th>
                <th>Quantità</th>
                <th>Percentuale</th>
            </tr>
        </thead>
        <tbody>
            {% for item in policy_types %}
            <tr>
                <td>{{ item.type }}</td>
                <td>{{ item.count }}</td>
                <td>{{ item.percentage }}%</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
```

## Template Management

### Adding New Templates
1. Create the template file in the appropriate subdirectory
2. Ensure field names match the data structure
3. Add the template to the database templates table
4. Update the configuration file with the new template path

### Template Validation
- All templates are validated during startup
- Field names are checked against the data schema
- Template integrity is verified
- Missing fields generate warnings

### Template Versioning
- Templates are versioned separately from the main application
- Version information is stored in the database
- Template updates trigger reprocessing of affected documents
- Backward compatibility is maintained when possible

## Customization

### Branding
Templates can be customized with:
- Company logo
- Brand colors
- Contact information
- Legal text

### Localization
Templates support multiple languages:
- Italian (default)
- English
- French
- German
- Spanish

### Conditional Content
Templates can include conditional content based on:
- Policy type
- Client category
- Risk level
- Coverage options

## Best Practices

### Design Guidelines
1. Keep templates clean and professional
2. Use consistent branding
3. Ensure readability on all devices
4. Test templates with sample data
5. Validate output documents

### Performance Considerations
1. Optimize template loading
2. Cache frequently used templates
3. Minimize template complexity
4. Use efficient rendering engines

### Security
1. Sanitize all template inputs
2. Prevent code injection in templates
3. Validate template file integrity
4. Restrict template file access

## Template API

### Template Service
The template service provides methods for:
- Loading templates
- Rendering templates with data
- Validating template fields
- Managing template versions

### Template Functions
Available template functions include:
- Date formatting
- Number formatting
- Text manipulation
- Conditional logic
- Data lookup

### Template Filters
Custom template filters for:
- Currency formatting
- Percentage calculation
- Text truncation
- HTML escaping