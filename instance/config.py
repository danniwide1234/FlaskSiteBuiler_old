import os
from dotenv import load_dotenv

# Load environment variables from a .env file located in the instance directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

class InstanceConfig:
    # General Config
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    # Database Config
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() in ('true', '1', 't')

    # Debugging and Testing
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    TESTING = os.getenv('TESTING', 'False').lower() in ('true', '1', 't')

    # Additional configurations can be added here as needed

