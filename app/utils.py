import os
from flask import url_for, current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer as Serializer
from app.extensions import mail
from PIL import Image
import secrets

def send_reset_email(user):
    """
    Sends a password reset email to the user.

    Args:
        user (User): The user who requested the password reset.
    """
    token = get_reset_token(user)
    msg = Message('Password Reset Request',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

def get_reset_token(user, expires_sec=1800):
    """
    Generates a password reset token for the user.

    Args:
        user (User): The user who requested the password reset.
        expires_sec (int): The expiration time in seconds for the token (default is 30 minutes).

    Returns:
        str: The generated token.
    """
    s = Serializer(current_app.config['SECRET_KEY'])
    return s.dumps({'user_id': user.id}).decode('utf-8')

def verify_reset_token(token):
    """
    Verifies a password reset token.

    Args:
        token (str): The token to verify.

    Returns:
        User: The user associated with the token if valid, None otherwise.
    """
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token, max_age=1800)['user_id']
    except:
        return None
    from app.models import User
    return User.query.get(user_id)

def save_picture(form_picture, output_size=(125, 125)):
    """
    Saves a user-uploaded picture, resizing it to the specified output size.

    Args:
        form_picture (FileStorage): The uploaded picture.
        output_size (tuple): The desired output size (width, height).

    Returns:
        str: The filename of the saved picture.
    """
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = secrets.token_hex(8) + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

