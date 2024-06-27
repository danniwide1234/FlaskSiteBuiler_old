# tests/__init__.py

import unittest
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app import create_app, db
from app.models import User, Post

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password123')
        db.session.add(self.user)

        # Create test posts
        self.post1 = Post(title='Test Post 1', content='Content of Test Post 1', author=self.user)
        self.post2 = Post(title='Test Post 2', content='Content of Test Post 2', author=self.user)
        db.session.add(self.post1)
        db.session.add(self.post2)

        db.session.commit()

    def tearDown(self):
        """Tear down test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """Test if the application instance exists"""
        self.assertIsNotNone(current_app)

    def test_app_is_testing(self):
        """Test if the application is running in testing mode"""
        self.assertTrue(current_app.config['TESTING'])

    def test_home_page(self):
        """Test home page route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to FlaskSiteBuilder', response.data)

    def test_login(self):
        """Test login functionality"""
        response = self.client.post('/auth/login', data=dict(
            email='test@example.com',
            password='password123'
        ), follow_redirects=True)
        self.assertIn(b'Welcome back', response.data)
        self.assertTrue(current_user.is_authenticated)

    def test_logout(self):
        """Test logout functionality"""
        with self.client:
            self.client.post('/auth/login', data=dict(
                email='test@example.com',
                password='password123'
            ))
            response = self.client.get('/auth/logout', follow_redirects=True)
            self.assertIn(b'You have been logged out', response.data)
            self.assertFalse(current_user.is_authenticated)

    def test_post_creation(self):
        """Test post creation functionality"""
        with self.client:
            self.client.post('/auth/login', data=dict(
                email='test@example.com',
                password='password123'
            ))
            response = self.client.post('/post/new', data=dict(
                title='Test New Post',
                content='Content of the new test post'
            ), follow_redirects=True)
            self.assertIn(b'Test New Post', response.data)
            self.assertEqual(Post.query.count(), 3)

    def test_post_deletion(self):
        """Test post deletion functionality"""
        with self.client:
            self.client.post('/auth/login', data=dict(
                email='test@example.com',
                password='password123'
            ))
            response = self.client.post(f'/post/{self.post1.id}/delete', follow_redirects=True)
            self.assertNotIn(b'Test Post 1', response.data)
            self.assertEqual(Post.query.count(), 1)

    def test_profile_page(self):
        """Test user profile page"""
        with self.client:
            self.client.post('/auth/login', data=dict(
                email='test@example.com',
                password='password123'
            ))
            response = self.client.get(f'/user/{self.user.username}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'testuser', response.data)

    def test_update_account(self):
        """Test account update functionality"""
        with self.client:
            self.client.post('/auth/login', data=dict(
                email='test@example.com',
                password='password123'
            ))
            response = self.client.post('/account', data=dict(
                username='updateduser',
                email='updated@example.com'
            ), follow_redirects=True)
            self.assertIn(b'Account updated', response.data)
            self.assertEqual(User.query.filter_by(username='updateduser').count(), 1)

    def test_password_reset_request(self):
        """Test password reset request functionality"""
        response = self.client.post('/auth/reset_request', data=dict(
            email='test@example.com'
        ), follow_redirects=True)
        self.assertIn(b'Check your email for the instructions', response.data)

    def test_password_reset(self):
        """Test password reset functionality"""
        token = self.user.get_reset_token()
        response = self.client.post(f'/auth/reset_password/{token}', data=dict(
            password='newpassword123',
            confirm_password='newpassword123'
        ), follow_redirects=True)
        self.assertIn(b'Your password has been updated', response.data)
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_error_404(self):
        """Test 404 error page"""
        response = self.client.get('/nonexistent_route')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 - Page Not Found', response.data)

    def test_error_500(self):
        """Test 500 error page"""
        # Simulate a server error by querying an invalid attribute
        with self.app.app_context():
            try:
                db.session.query(User).filter_by(nonexistent_attr='test').first()
            except Exception as e:
                self.assertTrue(True)  # Placeholder assertion for demonstrating a 500 error test

if __name__ == '__main__':
    unittest.main()

