from wtforms.validators import ValidationError
from app.models import User

class UniqueUsername:
    """
    Custom validator to check if the username is already in use.
    """

    def __init__(self, message=None):
        if not message:
            message = 'This username is already taken. Please choose a different username.'
        self.message = message

    def __call__(self, form, field):
        """
        Check if the username exists in the database.

        Args:
            form (Form): The form instance.
            field (Field): The field instance containing the data to validate.

        Raises:
            ValidationError: If the username already exists.
        """
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(self.message)


class UniqueEmail:
    """
    Custom validator to check if the email is already in use.
    """

    def __init__(self, message=None):
        if not message:
            message = 'This email is already registered. Please use a different email.'
        self.message = message

    def __call__(self, form, field):
        """
        Check if the email exists in the database.

        Args:
            form (Form): The form instance.
            field (Field): The field instance containing the data to validate.

        Raises:
            ValidationError: If the email already exists.
        """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(self.message)

