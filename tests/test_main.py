# tests/test_main.py

import unittest
from flask import url_for
from flasksitebuilder import create_app, db
from flasksitebuilder.models import User
from flask_login import current_user


class MainTests(unittest.TestCase):

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
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

    def login_test_user(self):
        """Helper method to log in the test user."""
        self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)

    def test_home_page_loads(self):
        """Test that the home page loads correctly."""
        response = self.client.get(url_for('main.home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to FlaskSiteBuilder', response.data)

    def test_about_page_loads(self):
        """Test that the about page loads correctly."""
        response = self.client.get(url_for('main.about'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About FlaskSiteBuilder', response.data)

    def test_contact_page_loads(self):
        """Test that the contact page loads correctly."""
        response = self.client.get(url_for('main.contact'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Contact Us', response.data)

    def test_dashboard_page_loads_for_logged_in_user(self):
        """Test that the dashboard page loads for logged in users."""
        self.login_test_user()
        response = self.client.get(url_for('main.dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
        self.assertTrue(current_user.is_authenticated)

    def test_dashboard_page_redirects_for_anonymous_user(self):
        """Test that the dashboard page redirects for anonymous users."""
        response = self.client.get(url_for('main.dashboard'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in to access this page', response.data)
        self.assertFalse(current_user.is_authenticated)

    def test_404_error_page_loads(self):
        """Test that the custom 404 error page loads correctly."""
        response = self.client.get('/nonexistentpage')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 - Page Not Found', response.data)

    def test_500_error_page_loads(self):
        """Test that the custom 500 error page loads correctly."""
        # To test 500 error, we need to cause an internal server error
        @self.app.route('/cause500')
        def cause_500():
            raise Exception("Test 500 error")
        
        response = self.client.get('/cause500', follow_redirects=True)
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'500 - Server Error', response.data)


if __name__ == '__main__':
    unittest.main()

