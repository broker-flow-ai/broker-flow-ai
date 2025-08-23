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
        required_fields = ["name", "company"]
        for field in required_fields:
            if not client_data.get(field):
                errors.append(f"Il campo '{field}' è obbligatorio")
        
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
        
        # Validate tax ID if provided
        tax_id = client_data.get("tax_id")
        if tax_id:
            is_valid, error_msg = Validators.validate_tax_id(tax_id)
            if not is_valid:
                errors.append(f"Codice Fiscale/Partita IVA: {error_msg}")
        
        # Validate IBAN if provided
        iban = client_data.get("iban")
        if iban:
            is_valid, error_msg = Validators.validate_iban(iban)
            if not is_valid:
                errors.append(f"IBAN: {error_msg}")
        
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
        
        # Validate policy number format (basic check)
        policy_number = policy_data.get("policy_number")
        if policy_number and len(policy_number) < 3:
            errors.append("Il numero di polizza deve essere di almeno 3 caratteri")
        
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