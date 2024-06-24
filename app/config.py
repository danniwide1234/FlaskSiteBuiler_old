import os
from dotenv import load_dotenv

# Load environment variables from a .env file located in the instance directory
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    # Add more general configurations here

class DevelopmentConfig(Config):
    """Development configuration."""
    FLASK_ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Log SQL queries for debugging

class TestingConfig(Config):
    """Testing configuration."""
    FLASK_ENV = 'testing'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests
    SQLALCHEMY_ECHO = False

class ProductionConfig(Config):
    """Production configuration."""
    FLASK_ENV = 'production'
    SECRET_KEY = os.getenv('SECRET_KEY')  # Ensure SECRET_KEY is set in production

# Dictionary to map environment names to configuration classes
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

