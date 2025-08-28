import re
from typing import Dict, Any, List, Tuple
from datetime import datetime, date
import json

class Validators:
    """Utility class for validating input data"""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email format"""
        if not email:
            return False, "Email è obbligatoria"
        
        # Regular expression for email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            return True, ""
        else:
            return False, "Formato email non valido"
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """Validate phone number format"""
        if not phone:
            return True, ""  # Phone is optional
        
        # Allow international formats, spaces, dashes, parentheses
        pattern = r'^[\+]?[1-9][\d\s\-\(\)]{7,15}$'
        cleaned = re.sub(r'[^\d\+]', '', phone)
        
        if len(cleaned) >= 8 and len(cleaned) <= 15 and re.match(pattern, phone):
            return True, ""
        else:
            return False, "Formato numero di telefono non valido"
    
    @staticmethod
    def validate_tax_id(tax_id: str) -> Tuple[bool, str]:
        """Validate tax identification number format"""
        if not tax_id:
            return True, ""  # Tax ID is optional
        
        # Italian VAT/Tax ID format (example)
        pattern = r'^[A-Z]{2}[A-Z0-9]{11,15}$|^[0-9]{11,16}$'
        
        if re.match(pattern, tax_id.upper()):
            return True, ""
        else:
            return False, "Formato codice fiscale/partita IVA non valido"
    
    @staticmethod
    def validate_iban(iban: str) -> Tuple[bool, str]:
        """Validate IBAN format"""
        if not iban:
            return True, ""  # IBAN is optional
        
        # Basic IBAN validation
        cleaned = re.sub(r'[^A-Z0-9]', '', iban.upper())
        
        if len(cleaned) >= 15 and len(cleaned) <= 34:
            return True, ""
        else:
            return False, "Formato IBAN non valido"
    
    @staticmethod
    def validate_swift_code(swift: str) -> Tuple[bool, str]:
        """Validate SWIFT/BIC code format"""
        if not swift:
            return True, ""  # SWIFT is optional
        
        pattern = r'^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$'
        
        if re.match(pattern, swift.upper()):
            return True, ""
        else:
            return False, "Formato codice SWIFT/BIC non valido"
    
    @staticmethod
    def validate_amount(amount: float) -> Tuple[bool, str]:
        """Validate monetary amount"""
        try:
            if amount < 0:
                return False, "L'importo non può essere negativo"
            elif amount > 1000000000:  # Max 1 billion
                return False, "L'importo è troppo elevato"
            else:
                return True, ""
        except (ValueError, TypeError):
            return False, "Importo non valido"
    
    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, str]:
        """Validate date format"""
        if not date_str:
            return False, "La data è obbligatoria"
        
        # Accept YYYY-MM-DD or DD/MM/YYYY formats
        patterns = [
            r'^\d{4}-\d{2}-\d{2}$',
            r'^\d{2}/\d{2}/\d{4}$'
        ]
        
        for pattern in patterns:
            if re.match(pattern, date_str):
                try:
                    if "-" in date_str:
                        datetime.strptime(date_str, "%Y-%m-%d")
                    else:
                        datetime.strptime(date_str, "%d/%m/%Y")
                    return True, ""
                except ValueError:
                    continue
        
        return False, "Formato data non valido"
    
    @staticmethod
    def validate_client_data(client_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate complete client data"""
        errors = []
        
        # Validate required fields
        required_fields = ["name"]
        for field in required_fields:
            if not client_data.get(field):
                errors.append(f"Il campo '{field}' è obbligatorio")
        
        # Validate client type
        client_type = client_data.get("client_type")
        valid_client_types = ["individual", "company", "freelance", "public_entity"]
        if client_type and client_type not in valid_client_types:
            errors.append(f"Tipo cliente non valido. Tipi validi: {', '.join(valid_client_types)}")
        
        # Validate email if provided
        email = client_data.get("email")
        if email:
            is_valid, error_msg = Validators.validate_email(email)
            if not is_valid:
                errors.append(f"Email: {error_msg}")
        
        # Validate phone if provided
        phone = client_data.get("phone")
        if phone:
            is_valid, error_msg = Validators.validate_phone(phone)
            if not is_valid:
                errors.append(f"Telefono: {error_msg}")
        
        # Validate mobile if provided
        mobile = client_data.get("mobile")
        if mobile:
            is_valid, error_msg = Validators.validate_phone(mobile)
            if not is_valid:
                errors.append(f"Cellulare: {error_msg}")
        
        # Validate fiscal code if provided
        fiscal_code = client_data.get("fiscal_code")
        if fiscal_code and len(fiscal_code) != 16:
            errors.append("Il codice fiscale deve essere di 16 caratteri")
        
        # Validate VAT number if provided
        vat_number = client_data.get("vat_number")
        if vat_number and len(vat_number) != 11:
            errors.append("La partita IVA deve essere di 11 caratteri numerici")
        
        # Validate SDI code if provided
        sdi_code = client_data.get("sdi_code")
        if sdi_code and len(sdi_code) != 7:
            errors.append("Il codice SDI deve essere di 7 caratteri")
        
        # Validate PEC email if provided
        pec_email = client_data.get("pec_email")
        if pec_email:
            is_valid, error_msg = Validators.validate_email(pec_email)
            if not is_valid:
                errors.append(f"Email PEC: {error_msg}")
        
        # Validate IBAN if provided
        iban = client_data.get("iban")
        if iban:
            is_valid, error_msg = Validators.validate_iban(iban)
            if not is_valid:
                errors.append(f"IBAN: {error_msg}")
        
        # Validate share capital if provided
        share_capital = client_data.get("share_capital")
        if share_capital is not None:
            try:
                share_capital_float = float(share_capital)
                if share_capital_float < 0:
                    errors.append("Il capitale sociale non può essere negativo")
            except (ValueError, TypeError):
                errors.append("Capitale sociale non valido")
        
        # Validate customer status if provided
        customer_status = client_data.get("customer_status")
        valid_statuses = ["active", "inactive", "prospect"]
        if customer_status and customer_status not in valid_statuses:
            errors.append(f"Stato cliente non valido. Stati validi: {', '.join(valid_statuses)}")
        
        # Validate preferred communication if provided
        preferred_communication = client_data.get("preferred_communication")
        valid_communications = ["email", "phone", "mail", "pec"]
        if preferred_communication and preferred_communication not in valid_communications:
            errors.append(f"Canale comunicazione non valido. Canali validi: {', '.join(valid_communications)}")
        
        # Validate language if provided
        language = client_data.get("language")
        valid_languages = ["it", "en", "es", "fr", "de"]
        if language and language not in valid_languages:
            errors.append(f"Lingua non valida. Lingue valide: {', '.join(valid_languages)}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_policy_data(policy_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate complete policy data"""
        errors = []
        
        # Validate required fields
        required_fields = ["risk_id", "company_id", "company", "policy_number"]
        for field in required_fields:
            if not policy_data.get(field):
                errors.append(f"Il campo '{field}' è obbligatorio")
        
        # Validate risk_id
        risk_id = policy_data.get("risk_id")
        try:
            int(risk_id)
        except (ValueError, TypeError):
            errors.append("L'ID rischio deve essere un numero")
        
        # Validate company_id
        company_id = policy_data.get("company_id")
        try:
            int(company_id)
        except (ValueError, TypeError):
            errors.append("L'ID compagnia deve essere un numero")
        
        # Validate dates
        start_date = policy_data.get("start_date")
        end_date = policy_data.get("end_date")
        
        if start_date:
            is_valid, error_msg = Validators.validate_date(start_date)
            if not is_valid:
                errors.append(f"Data inizio: {error_msg}")
        
        if end_date:
            is_valid, error_msg = Validators.validate_date(end_date)
            if not is_valid:
                errors.append(f"Data fine: {error_msg}")
        
        # Validate date range
        if start_date and end_date:
            is_valid, error_msg = Validators.validate_date_range(start_date, end_date)
            if not is_valid:
                errors.append(f"Periodo polizza: {error_msg}")
        
        # Validate subscription date if provided
        subscription_date = policy_data.get("subscription_date")
        if subscription_date:
            is_valid, error_msg = Validators.validate_date(subscription_date)
            if not is_valid:
                errors.append(f"Data sottoscrizione: {error_msg}")
        
        # Validate policy number format (basic check)
        policy_number = policy_data.get("policy_number")
        if policy_number and len(policy_number) < 3:
            errors.append("Il numero di polizza deve essere di almeno 3 caratteri")
        
        # Validate premium amount if provided
        premium_amount = policy_data.get("premium_amount")
        if premium_amount is not None:
            is_valid, error_msg = Validators.validate_amount(float(premium_amount) if not isinstance(premium_amount, float) else premium_amount)
            if not is_valid:
                errors.append(f"Importo premio: {error_msg}")
        
        # Validate subscription method if provided
        subscription_method = policy_data.get("subscription_method")
        valid_methods = ["digital", "paper", "agent"]
        if subscription_method and subscription_method not in valid_methods:
            errors.append(f"Metodo sottoscrizione non valido. Metodi validi: {', '.join(valid_methods)}")
        
        # Validate premium frequency if provided
        premium_frequency = policy_data.get("premium_frequency")
        valid_frequencies = ["annual", "semiannual", "quarterly", "monthly"]
        if premium_frequency and premium_frequency not in valid_frequencies:
            errors.append(f"Frequenza pagamento non valida. Frequenze valide: {', '.join(valid_frequencies)}")
        
        # Validate payment method if provided
        payment_method = policy_data.get("payment_method")
        valid_methods = ["", "direct_debit", "bank_transfer", "credit_card", "cash", "check"]
        if payment_method and payment_method not in valid_methods:
            errors.append(f"Metodo pagamento non valido. Metodi validi: {', '.join([m for m in valid_methods if m])}")
        
        # Validate primary subscriber ID if provided
        primary_subscriber_id = policy_data.get("primary_subscriber_id")
        if primary_subscriber_id:
            try:
                int(primary_subscriber_id)
            except (ValueError, TypeError):
                errors.append("L'ID sottoscrittore principale deve essere un numero")
        
        # Validate premium delegate ID if provided
        premium_delegate_id = policy_data.get("premium_delegate_id")
        if premium_delegate_id:
            try:
                int(premium_delegate_id)
            except (ValueError, TypeError):
                errors.append("L'ID delegato pagamento deve essere un numero")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_claim_data(claim_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate complete claim data"""
        errors = []
        
        # Validate required fields
        required_fields = ["policy_id", "claim_date", "amount"]
        for field in required_fields:
            if not claim_data.get(field):
                errors.append(f"Il campo '{field}' è obbligatorio")
        
        # Validate policy_id
        policy_id = claim_data.get("policy_id")
        try:
            int(policy_id)
        except (ValueError, TypeError):
            errors.append("L'ID polizza deve essere un numero")
        
        # Validate claim date
        claim_date = claim_data.get("claim_date")
        if claim_date:
            is_valid, error_msg = Validators.validate_date(claim_date)
            if not is_valid:
                errors.append(f"Data sinistro: {error_msg}")
        
        # Validate amount
        amount = claim_data.get("amount")
        if amount is not None:
            is_valid, error_msg = Validators.validate_amount(float(amount) if not isinstance(amount, float) else amount)
            if not is_valid:
                errors.append(f"Importo: {error_msg}")
        
        # Validate description length
        description = claim_data.get("description", "")
        if len(description) > 1000:
            errors.append("La descrizione non può superare i 1000 caratteri")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_json_structure(json_data: str) -> Tuple[bool, str]:
        """Validate JSON structure"""
        try:
            parsed_data = json.loads(json_data)
            return True, ""
        except json.JSONDecodeError as e:
            return False, f"Struttura JSON non valida: {str(e)}"
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
        """Validate that start date is before end date"""
        try:
            if "-" in start_date:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            else:
                start_dt = datetime.strptime(start_date, "%d/%m/%Y")
            
            if "-" in end_date:
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            else:
                end_dt = datetime.strptime(end_date, "%d/%m/%Y")
            
            if start_dt > end_dt:
                return False, "La data di inizio deve essere precedente alla data di fine"
            
            return True, ""
        except ValueError:
            return False, "Formato date non valido"
    
    @staticmethod
    def validate_numeric_range(value: float, min_val: float, max_val: float) -> Tuple[bool, str]:
        """Validate that value is within numeric range"""
        try:
            if value < min_val:
                return False, f"Il valore deve essere maggiore o uguale a {min_val}"
            elif value > max_val:
                return False, f"Il valore deve essere minore o uguale a {max_val}"
            else:
                return True, ""
        except (ValueError, TypeError):
            return False, "Valore numerico non valido"
    
    @staticmethod
    def validate_percentage(percentage: float) -> Tuple[bool, str]:
        """Validate percentage value (0-100)"""
        return Validators.validate_numeric_range(percentage, 0.0, 100.0)
    
    @staticmethod
    def validate_client_sector(sector: str) -> Tuple[bool, str]:
        """Validate client sector"""
        valid_sectors = [
            "Trasporti", "Sanità", "Edilizia", "Legalità", "Ingegneria",
            "Commercio", "Logistica", "Noleggio", "Assicurativo"
        ]
        
        if sector in valid_sectors:
            return True, ""
        else:
            return False, f"Settore non valido. Settori validi: {', '.join(valid_sectors)}"
    
    @staticmethod
    def validate_risk_type(risk_type: str) -> Tuple[bool, str]:
        """Validate risk type"""
        valid_risk_types = [
            "Flotta Auto", "RC Professionale", "Fabbricato", 
            "Rischi Tecnici", "Altro"
        ]
        
        if risk_type in valid_risk_types:
            return True, ""
        else:
            return False, f"Tipo rischio non valido. Tipi validi: {', '.join(valid_risk_types)}"
    
    @staticmethod
    def validate_policy_status(status: str) -> Tuple[bool, str]:
        """Validate policy status"""
        valid_statuses = ["active", "expired", "cancelled", "pending"]
        
        if status in valid_statuses:
            return True, ""
        else:
            return False, f"Stato polizza non valido. Stati validi: {', '.join(valid_statuses)}"
    
    @staticmethod
    def validate_claim_status(status: str) -> Tuple[bool, str]:
        """Validate claim status"""
        valid_statuses = ["open", "in_review", "approved", "rejected"]
        
        if status in valid_statuses:
            return True, ""
        else:
            return False, f"Stato sinistro non valido. Stati validi: {', '.join(valid_statuses)}"