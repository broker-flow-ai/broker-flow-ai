import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "brokerflow_ai")

# Path
INBOX_PATH = "inbox/"
OUTPUT_PATH = "output/"
TEMPLATE_PATH = "templates/"

# Email Configuration
EMAIL_CONFIG = {
    'smtp_server': os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    'smtp_port': int(os.getenv("SMTP_PORT", "587")),
    'sender_email': os.getenv("SENDER_EMAIL", ""),
    'sender_password': os.getenv("SENDER_PASSWORD", "")
}

# 2FA Configuration
ENABLE_2FA = os.getenv("ENABLE_2FA", "true").lower() == "true"
OTP_EXPIRATION_MINUTES = int(os.getenv("OTP_EXPIRATION_MINUTES", "10"))
OTP_LENGTH = int(os.getenv("OTP_LENGTH", "6"))

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30