import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # General Config
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    # Database Config
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() in ('true', '1', 't')

    # Debugging and Testing
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    TESTING = os.getenv('TESTING', 'False').lower() in ('true', '1', 't')

    # Additional configurations can be added here as needed

