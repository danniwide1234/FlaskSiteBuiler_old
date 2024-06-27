# tests/test_config.py

import unittest
from flasksitebuilder import create_app
from flasksitebuilder.config import DevelopmentConfig, TestingConfig, ProductionConfig


class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.app = None

    def tearDown(self):
        """Tear down the test environment."""
        if self.app:
            self.app_context.pop()

    def assertConfig(self, config):
        """Helper method to assert common configuration values."""
        self.assertEqual(self.app.config['SECRET_KEY'], config.SECRET_KEY)
        self.assertEqual(self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'], config.SQLALCHEMY_TRACK_MODIFICATIONS)
        self.assertEqual(self.app.config['MAIL_SERVER'], config.MAIL_SERVER)
        self.assertEqual(self.app.config['MAIL_PORT'], config.MAIL_PORT)
        self.assertEqual(self.app.config['MAIL_USE_TLS'], config.MAIL_USE_TLS)
        self.assertEqual(self.app.config['MAIL_USERNAME'], config.MAIL_USERNAME)
        self.assertEqual(self.app.config['MAIL_PASSWORD'], config.MAIL_PASSWORD)

    def test_development_config(self):
        """Test the DevelopmentConfig."""
        self.app = create_app('development')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.assertTrue(self.app.config['DEBUG'])
        self.assertFalse(self.app.config['TESTING'])
        self.assertEqual(self.app.config['SQLALCHEMY_DATABASE_URI'], DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
        self.assertConfig(DevelopmentConfig)

    def test_testing_config(self):
        """Test the TestingConfig."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.assertTrue(self.app.config['DEBUG'])
        self.assertTrue(self.app.config['TESTING'])
        self.assertEqual(self.app.config['SQLALCHEMY_DATABASE_URI'], TestingConfig.SQLALCHEMY_DATABASE_URI)
        self.assertConfig(TestingConfig)
        self.assertFalse(self.app.config['WTF_CSRF_ENABLED'])

    def test_production_config(self):
        """Test the ProductionConfig."""
        self.app = create_app('production')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.assertFalse(self.app.config['DEBUG'])
        self.assertFalse(self.app.config['TESTING'])
        self.assertEqual(self.app.config['SQLALCHEMY_DATABASE_URI'], ProductionConfig.SQLALCHEMY_DATABASE_URI)
        self.assertConfig(ProductionConfig)


if __name__ == '__main__':
    unittest.main()

