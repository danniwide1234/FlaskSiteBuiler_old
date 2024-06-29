from flask import render_template
from app.auth import bp

@bp.route('/login')
def login():
    return render_template('auth/login.html')

@bp.route('/register')
def register():
    return render_template('auth/register.html')

@bp.route('/reset_password')
def reset_password():
    return render_template('auth/reset_password.html')

@bp.route('/reset_request')
def reset_request():
    return render_template('auth/reset_request.html')

