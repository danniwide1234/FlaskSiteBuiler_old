from datetime import datetime
from app.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    """
    User model for storing user details and managing authentication.

    Attributes:
        id (int): Primary key.
        username (str): Unique username.
        email (str): Unique email address.
        password_hash (str): Hashed password.
        created_at (datetime): Timestamp of account creation.
        last_login (datetime): Timestamp of last login.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the provided password matches the stored hashed password.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """
        Update the last login timestamp to the current time.
        """
        self.last_login = datetime.utcnow()
        db.session.commit()

    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    """
    Post model for storing blog posts.

    Attributes:
        id (int): Primary key.
        title (str): Title of the post.
        content (str): Content of the post.
        date_posted (datetime): Timestamp of when the post was created.
        user_id (int): Foreign key to the user who created the post.
        author (User): Relationship to the User model.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<Post {self.title}>'

class Comment(db.Model):
    """
    Comment model for storing comments on posts.

    Attributes:
        id (int): Primary key.
        content (str): Content of the comment.
        date_posted (datetime): Timestamp of when the comment was created.
        user_id (int): Foreign key to the user who created the comment.
        post_id (int): Foreign key to the post on which the comment was made.
        author (User): Relationship to the User model.
        post (Post): Relationship to the Post model.
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('comments', lazy=True))
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f'<Comment {self.content[:20]}>'

# Load user by ID function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """
    Load a user by their ID.

    Args:
        user_id (int): The user's ID.

    Returns:
        User: The user object if found, None otherwise.
    """
    return User.query.get(int(user_id))

