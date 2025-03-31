import os
from datetime import datetime
from dotenv import load_dotenv
from kiteconnect import KiteConnect

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class to store environment variables and manage sessions."""
    KITE_API_KEY = os.getenv('KITE_API_KEY')
    KITE_API_SECRET = os.getenv('KITE_API_SECRET')
    _access_token = None
    _kite = None

    @classmethod
    def validate(cls):
        """Validate that all required environment variables are set."""
        if not all([cls.KITE_API_KEY, cls.KITE_API_SECRET]):
            raise ValueError("Missing required environment variables. Please check your .env file.")

    @classmethod
    def get_kite(cls):
        """Get or create KiteConnect instance."""
        if not cls._kite:
            cls._kite = KiteConnect(api_key=cls.KITE_API_KEY)
            if cls._access_token:
                cls._kite.set_access_token(cls._access_token)
        return cls._kite

    @classmethod
    def generate_login_url(cls):
        """Generate login URL for getting request token."""
        return cls.get_kite().login_url()

    @classmethod
    def set_session(cls, request_token):
        """Generate session and set access token."""
        try:
            data = cls.get_kite().generate_session(
                request_token, 
                api_secret=cls.KITE_API_SECRET
            )
            cls._access_token = data["access_token"]
            cls._kite.set_access_token(cls._access_token)
            
            # Optionally save access token to file for reuse
            with open('.access_token', 'w') as f:
                f.write(cls._access_token)
            
            return True
        except Exception as e:
            print(f"Error setting session: {str(e)}")
            return False

    @classmethod
    def load_saved_session(cls):
        """Load previously saved access token if available."""
        try:
            if os.path.exists('.access_token'):
                with open('.access_token', 'r') as f:
                    cls._access_token = f.read().strip()
                cls.get_kite().set_access_token(cls._access_token)
                return True
        except Exception as e:
            print(f"Error loading saved session: {str(e)}")
        return False