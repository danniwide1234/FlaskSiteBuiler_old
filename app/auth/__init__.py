from flask import Blueprint

# Define the blueprint: 'auth', set its URL prefix to '/auth'
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Import the routes to associate them with the blueprint
from app.auth import routes

# Optionally, import any necessary configurations or utilities specific to the auth module
# from app.auth import config, utils

# Register any custom error handlers for the auth blueprint if needed
# auth_bp.register_error_handler(403, custom_forbidden_handler)
# auth_bp.register_error_handler(401, custom_unauthorized_handler)

# Additional initialization or setup specific to the auth blueprint can be added here
# e.g., setting up OAuth providers, adding before/after request hooks, etc.
# auth_bp.before_request(before_request_function)
# auth_bp.after_request(after_request_function)

