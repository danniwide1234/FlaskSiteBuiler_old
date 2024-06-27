# tests/test_auth.py

import unittest
from flask import url_for
from flasksitebuilder import create_app, db
from flasksitebuilder.models import User
from flask_login import current_user

class AuthTests(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
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

    def test_registration_page_loads(self):
        """Test that the registration page loads correctly."""
        response = self.client.get(url_for('auth.register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create Your FlaskSiteBuilder Account', response.data)

    def test_successful_registration(self):
        """Test that a new user can register successfully."""
        response = self.client.post(url_for('auth.register'), data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created', response.data)
        self.assertIsNotNone(User.query.filter_by(email='newuser@example.com').first())

    def test_duplicate_email_registration(self):
        """Test that registration fails with a duplicate email."""
        response = self.client.post(url_for('auth.register'), data={
            'username': 'newuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email already registered', response.data)

    def test_login_page_loads(self):
        """Test that the login page loads correctly."""
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login to FlaskSiteBuilder', response.data)

    def test_successful_login(self):
        """Test that a user can log in successfully."""
        response = self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back', response.data)
        self.assertTrue(current_user.is_authenticated)

    def test_unsuccessful_login(self):
        """Test that login fails with incorrect credentials."""
        response = self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login Unsuccessful', response.data)
        self.assertFalse(current_user.is_authenticated)

    def test_logout(self):
        """Test that a user can log out successfully."""
        self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'password123'
        })
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out', response.data)
        self.assertFalse(current_user.is_authenticated)

    def test_reset_request_page_loads(self):
        """Test that the reset request page loads correctly."""
        response = self.client.get(url_for('auth.reset_request'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reset Your Password', response.data)

    def test_successful_reset_request(self):
        """Test that a password reset request can be made successfully."""
        response = self.client.post(url_for('auth.reset_request'), data={
            'email': 'test@example.com'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Check your email for the instructions', response.data)

    def test_invalid_reset_request(self):
        """Test that a reset request fails with an invalid email."""
        response = self.client.post(url_for('auth.reset_request'), data={
            'email': 'invalid@example.com'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'That email is not registered', response.data)

    def test_reset_password_page_loads(self):
        """Test that the reset password page loads correctly."""
        token = self.user.get_reset_token()
        response = self.client.get(url_for('auth.reset_password', token=token))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reset Your Password', response.data)

    def test_successful_password_reset(self):
        """Test that a user can reset their password successfully."""
        token = self.user.get_reset_token()
        response = self.client.post(url_for('auth.reset_password', token=token), data={
            'password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your password has been updated', response.data)
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_invalid_token_password_reset(self):
        """Test that password reset fails with an invalid token."""
        response = self.client.post(url_for('auth.reset_password', token='invalidtoken'), data={
            'password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'That is an invalid or expired token', response.data)


if __name__ == '__main__':
    unittest.main()

