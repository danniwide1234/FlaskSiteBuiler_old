from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from app.config import config
from app.extensions import db, migrate, login_manager, mail, bcrypt, bootstrap

def create_app(config_name='default'):
    """
    Factory function to create and configure the Flask app instance.

    Args:
        config_name (str): The configuration name to use for the app (default is 'default').

    Returns:
        Flask: Configured Flask app instance.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    bootstrap.init_app(app)

    # Configure Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.main.routes import main_bp
    from app.auth.routes import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Set up custom error pages
    register_error_handlers(app)

    return app

def register_error_handlers(app):
    """
    Registers custom error handlers for the Flask app.

    Args:
        app (Flask): The Flask app instance.
    """
    from flask import render_template

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

