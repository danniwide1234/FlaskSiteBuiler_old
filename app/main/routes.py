from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

# Define the blueprint: 'main', set its URL prefix: app.url/
main_bp = Blueprint('main', __name__)

# Home route
@main_bp.route('/')
def home():
    return render_template('core/index.html')

# About route
@main_bp.route('/about')
def about():
    return render_template('core/about.html')

# Dashboard route - protected, accessible only when logged in
@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('core/dashboard.html', name=current_user.username)

# Error handlers
@main_bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

