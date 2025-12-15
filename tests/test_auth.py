import unittest
from unittest.mock import patch, MagicMock
from src.config import Config

class TestAuth(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.api_key = "test_api_key"
        self.api_secret = "test_api_secret"
        self.request_token = "test_request_token"
        self.access_token = "test_access_token"

    @patch('kiteconnect.KiteConnect')
    def test_kite_initialization(self, mock_kite_class):
        """Test if KiteConnect is initialized with correct API key."""
        # Setup
        Config.KITE_API_KEY = self.api_key
        mock_kite = mock_kite_class.return_value
        
        # Execute
        kite = Config.get_kite()
        
        # Assert
        mock_kite_class.assert_called_once_with(api_key=self.api_key)

    @patch('kiteconnect.KiteConnect')
    def test_login_url_generation(self, mock_kite_class):
        """Test if login URL is generated correctly."""
        # Setup
        expected_url = "https://kite.zerodha.com/connect/login?api_key=test_api_key"
        mock_kite = mock_kite_class.return_value
        mock_kite.login_url.return_value = expected_url
        
        # Execute
        login_url = Config.generate_login_url()
        
        # Assert
        self.assertEqual(login_url, expected_url)

    @patch('kiteconnect.KiteConnect')
    def test_set_session(self, mock_kite_class):
        """Test session generation with request token."""
        # Setup
        mock_kite = mock_kite_class.return_value
        mock_kite.generate_session.return_value = {
            "access_token": self.access_token,
            "user_id": "test_user"
        }
        
        # Execute
        result = Config.set_session(self.request_token)
        
        # Assert
        self.assertTrue(result)
        mock_kite.generate_session.assert_called_once_with(
            self.request_token, 
            api_secret=Config.KITE_API_SECRET
        )
        mock_kite.set_access_token.assert_called_once_with(self.access_token)

if __name__ == '__main__':
    unittest.main()