from flask import Blueprint

# Create the main blueprint
main_bp = Blueprint('main', __name__)

# Import routes to associate them with the blueprint
from app.main import routes

# Define a function to initialize the blueprint
def init_app(app):
    """
    Initialize the main blueprint and register it with the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    app.register_blueprint(main_bp)

