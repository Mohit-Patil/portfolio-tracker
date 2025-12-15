from config import Config
from portfolio import Portfolio
import logging
import pandas as pd

# Set display options for pandas
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_session():
    """Initialize Kite session with proper authentication"""
    Config.validate()
    
    # Try loading existing session first
    if Config.load_saved_session():
        try:
            # Verify if session is still valid
            Config.get_kite().profile()
            logger.info("Successfully loaded saved session")
            return True
        except Exception as e:
            logger.info("Saved session expired or invalid")
    
    # If no saved session or expired, start new login process
    login_url = Config.generate_login_url()
    logger.info(f"\nPlease visit this URL to login:\n{login_url}")
    
    # Get request token from user
    request_token = input("\nEnter the request token from the redirect URL: ")
    
    if Config.set_session(request_token):
        logger.info("Successfully established new session")
        return True
    else:
        logger.error("Failed to establish session")
        return False

def display_portfolio():
    """Display portfolio information"""
    portfolio = Portfolio()
    
    # Get and display portfolio summary
    summary = portfolio.get_portfolio_summary()
    print("\n=== Portfolio Summary ===")
    print(f"Total Investment: ₹{summary['total_investment']:,.2f}")
    print(f"Current Value: ₹{summary['current_value']:,.2f}")
    print(f"Overall P&L: ₹{summary['total_pnl']:,.2f} ({summary['pnl_percentage']:.2f}%)")
    print(f"Day's P&L: ₹{summary['day_pnl']:,.2f}")
    print(f"Available Margin: ₹{summary['available_margin']:,.2f}")
    print(f"Total Account Value: ₹{summary['available_margin'] + summary['current_value']:,.2f}")
    
    # Get and display holdings
    print("\n=== Current Holdings ===")
    holdings_df = portfolio.get_holdings()
    if not holdings_df.empty:
        print(holdings_df)
    else:
        print("No holdings found")
    
    # Get and display positions
    print("\n=== Current Positions ===")
    positions_df = portfolio.get_positions()
    if not positions_df.empty:
        print(positions_df)
    else:
        print("No positions found")

if __name__ == "__main__":
    if initialize_session():
        try:
            display_portfolio()
        except Exception as e:
            logger.error(f"Error: {str(e)}")
    else:
        logger.error("Failed to load session. Please authenticate first.")