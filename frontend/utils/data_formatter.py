import json
from datetime import datetime, date
from decimal import Decimal
from typing import Any, Dict, List, Union

class DataFormatter:
    """Utility class for formatting data for display and storage"""
    
    @staticmethod
    def format_currency(amount: Union[float, Decimal, int, str], currency: str = "EUR") -> str:
        """Format amount as currency string"""
        try:
            if isinstance(amount, str):
                amount = float(amount)
            elif isinstance(amount, Decimal):
                amount = float(amount)
            
            if currency == "EUR":
                return f"€{amount:,.2f}"
            else:
                return f"{amount:,.2f} {currency}"
        except (ValueError, TypeError):
            return f"€0.00"
    
    @staticmethod
    def format_percentage(value: Union[float, Decimal, int, str]) -> str:
        """Format value as percentage string"""
        try:
            if isinstance(value, str):
                value = float(value)
            elif isinstance(value, Decimal):
                value = float(value)
            
            return f"{value:.2f}%"
        except (ValueError, TypeError):
            return "0.00%"
    
    @staticmethod
    def format_date(date_value: Union[str, datetime, date]) -> str:
        """Format date as DD/MM/YYYY string"""
        if not date_value:
            return "N/A"
        
        try:
            if isinstance(date_value, str):
                # Try to parse different date formats
                for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", 
                           "%d/%m/%Y", "%d-%m-%Y"]:
                    try:
                        parsed_date = datetime.strptime(date_value, fmt)
                        return parsed_date.strftime("%d/%m/%Y")
                    except ValueError:
                        continue
                # If none work, return original string
                return date_value
            elif isinstance(date_value, datetime):
                return date_value.strftime("%d/%m/%Y")
            elif isinstance(date_value, date):
                return date_value.strftime("%d/%m/%Y")
            else:
                return str(date_value)
        except Exception:
            return "N/A"
    
    @staticmethod
    def format_datetime(datetime_value: Union[str, datetime]) -> str:
        """Format datetime as DD/MM/YYYY HH:MM string"""
        if not datetime_value:
            return "N/A"
        
        try:
            if isinstance(datetime_value, str):
                # Try to parse different datetime formats
                for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", 
                           "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S"]:
                    try:
                        parsed_datetime = datetime.strptime(datetime_value, fmt)
                        return parsed_datetime.strftime("%d/%m/%Y %H:%M")
                    except ValueError:
                        continue
                # If none work, return original string
                return datetime_value
            elif isinstance(datetime_value, datetime):
                return datetime_value.strftime("%d/%m/%Y %H:%M")
            else:
                return str(datetime_value)
        except Exception:
            return "N/A"
    
    @staticmethod
    def format_number(number: Union[float, Decimal, int, str], decimals: int = 2) -> str:
        """Format number with thousand separators"""
        try:
            if isinstance(number, str):
                number = float(number)
            elif isinstance(number, Decimal):
                number = float(number)
            
            if decimals == 0:
                return f"{int(number):,}"
            else:
                return f"{number:,.{decimals}f}"
        except (ValueError, TypeError):
            return "0"
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100) -> str:
        """Truncate text to max length with ellipsis"""
        if not text:
            return ""
        
        if len(text) <= max_length:
            return text
        else:
            return text[:max_length] + "..."
    
    @staticmethod
    def format_client_name(client_data: Dict[str, Any]) -> str:
        """Format client name nicely"""
        name = client_data.get("name", "")
        company = client_data.get("company", "")
        
        if name and company:
            return f"{name} ({company})"
        elif name:
            return name
        elif company:
            return company
        else:
            return "Cliente Sconosciuto"
    
    @staticmethod
    def format_risk_type(risk_type: str) -> str:
        """Format risk type with proper capitalization"""
        risk_types = {
            "flotta auto": "Flotta Auto",
            "rc professionale": "RC Professionale",
            "fabbricato": "Fabbricato",
            "rischi tecnici": "Rischi Tecnici",
            "altro": "Altro"
        }
        
        normalized_type = risk_type.lower().strip()
        return risk_types.get(normalized_type, risk_type)
    
    @staticmethod
    def format_policy_status(status: str) -> str:
        """Format policy status with proper capitalization and translation"""
        statuses = {
            "active": "Attiva",
            "expired": "Scaduta",
            "cancelled": "Cancellata",
            "pending": "In Attesa"
        }
        
        normalized_status = status.lower().strip()
        return statuses.get(normalized_status, status)
    
    @staticmethod
    def format_claim_status(status: str) -> str:
        """Format claim status with proper capitalization and translation"""
        statuses = {
            "open": "Aperto",
            "in_review": "In Revisione",
            "approved": "Approvato",
            "rejected": "Rifiutato"
        }
        
        normalized_status = status.lower().strip()
        return statuses.get(normalized_status, status)
    
    @staticmethod
    def format_sector(sector: str) -> str:
        """Format sector with proper capitalization"""
        sectors = {
            "trasporti": "Trasporti",
            "sanità": "Sanità",
            "edilizia": "Edilizia",
            "legalità": "Legalità",
            "ingegneria": "Ingegneria",
            "commercio": "Commercio",
            "logistica": "Logistica",
            "noleggio": "Noleggio",
            "assicurativo": "Assicurativo"
        }
        
        normalized_sector = sector.lower().strip()
        return sectors.get(normalized_sector, sector)
    
    @staticmethod
    def json_serializable(obj: Any) -> Any:
        """Convert object to JSON serializable format"""
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, dict):
            return {key: DataFormatter.json_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [DataFormatter.json_serializable(item) for item in obj]
        else:
            return str(obj)
    
    @staticmethod
    def safe_json_dumps(obj: Any, **kwargs) -> str:
        """Safely convert object to JSON string"""
        try:
            serializable_obj = DataFormatter.json_serializable(obj)
            return json.dumps(serializable_obj, **kwargs)
        except Exception as e:
            print(f"Error serializing object to JSON: {str(e)}")
            return json.dumps({"error": "Serialization failed"})
    
    @staticmethod
    def safe_json_loads(json_string: str) -> Any:
        """Safely load JSON string"""
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {str(e)}")
            return {}
    
    @staticmethod
    def mask_sensitive_data(data: Dict[str, Any], sensitive_fields: List[str] = None) -> Dict[str, Any]:
        """Mask sensitive data fields"""
        if sensitive_fields is None:
            sensitive_fields = ["email", "phone", "tax_id", "bank_account"]
        
        masked_data = data.copy()
        
        for field in sensitive_fields:
            if field in masked_data:
                original_value = str(masked_data[field])
                if len(original_value) > 4:
                    masked_value = "*" * (len(original_value) - 4) + original_value[-4:]
                else:
                    masked_value = "*" * len(original_value)
                masked_data[field] = masked_value
        
        return masked_data
    
    @staticmethod
    def calculate_age_from_date(birth_date: Union[str, datetime, date]) -> int:
        """Calculate age from birth date"""
        if not birth_date:
            return 0
        
        try:
            if isinstance(birth_date, str):
                birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
            elif isinstance(birth_date, date) and not isinstance(birth_date, datetime):
                birth_date = datetime.combine(birth_date, datetime.min.time())
            
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return max(0, age)
        except Exception:
            return 0
    
    @staticmethod
    def format_time_ago(timestamp: Union[str, datetime]) -> str:
        """Format timestamp as 'X time ago'"""
        if not timestamp:
            return "N/A"
        
        try:
            if isinstance(timestamp, str):
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                dt = timestamp
            
            now = datetime.now(dt.tzinfo)
            diff = now - dt
            
            if diff.days > 365:
                years = diff.days // 365
                return f"{years} anno{'i' if years > 1 else ''} fa"
            elif diff.days > 30:
                months = diff.days // 30
                return f"{months} mese{'i' if months > 1 else ''} fa"
            elif diff.days > 0:
                return f"{diff.days} giorno{'i' if diff.days > 1 else ''} fa"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"{hours} ora{'e' if hours > 1 else ''} fa"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"{minutes} minuto{'i' if minutes > 1 else ''} fa"
            else:
                return "Poco fa"
        except Exception:
            return "N/A"