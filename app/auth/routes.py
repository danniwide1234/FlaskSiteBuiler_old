from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.auth import auth_bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for user login.

    Returns:
        Rendered template for login page or redirects to dashboard if login is successful.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful! Welcome back, {}.'.format(user.username), 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route for user registration.

    Returns:
        Rendered template for registration page or redirects to login page if registration is successful.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in, {}.'.format(user.username), 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """
    Route for user logout.

    Returns:
        Redirects to the home page after logging out.
    """
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

# Additional routes for password reset, account management, etc. can be added here

