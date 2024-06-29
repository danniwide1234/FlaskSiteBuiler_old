from flask import render_template
from app.main import bp

@bp.route('/')
def index():
    return render_template('core/index.html')

@bp.route('/about')
def about():
    return render_template('core/about.html')

@bp.route('/dashboard')
def dashboard():
    return render_template('core/dashboard.html')

@bp.route('/contact')
def contact():
    return render_template('core/contact.html')

