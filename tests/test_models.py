# tests/test_models.py

import unittest
from flasksitebuilder import create_app, db
from flasksitebuilder.models import User


class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.create_test_user()

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_test_user(self):
        """Create a test user."""
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()

    def test_user_creation(self):
        """Test user model creation."""
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')

    def test_password_hashing(self):
        """Test password hashing and verification."""
        user = User.query.filter_by(username='testuser').first()
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.check_password('wrongpassword'))

    def test_user_repr(self):
        """Test the string representation of the user."""
        user = User.query.filter_by(username='testuser').first()
        self.assertEqual(repr(user), f'<User {user.username}>')

    def test_email_uniqueness(self):
        """Test that email addresses are unique."""
        duplicate_user = User(username='testuser2', email='test@example.com')
        db.session.add(duplicate_user)
        with self.assertRaises(Exception):
            db.session.commit()

    def test_username_uniqueness(self):
        """Test that usernames are unique."""
        duplicate_user = User(username='testuser', email='test2@example.com')
        db.session.add(duplicate_user)
        with self.assertRaises(Exception):
            db.session.commit()


if __name__ == '__main__':
    unittest.main()

