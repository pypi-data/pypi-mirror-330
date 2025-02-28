import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for managing database credentials"""

    def __init__(self, db_name=None, user=None, password=None, host=None, port=5432):
        """Initialize configuration with user-provided or environment-based credentials."""
        self.db_name = db_name or os.getenv("DB_NAME")
        self.user = user or os.getenv("DB_USER")
        self.password = password or os.getenv("DB_PASSWORD")
        self.host = host or os.getenv("DB_HOST", "localhost")
        self.port = int(port or os.getenv("DB_PORT", 5432))

    def get_config(self):
        """Return the database configuration as a dictionary"""
        return {
            "dbname": self.db_name,
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "port": self.port,
        }

# Define global DB_CONFIG
DB_CONFIG = Config().get_config()
