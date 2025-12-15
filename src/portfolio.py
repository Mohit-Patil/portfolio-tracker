from config import Config
import pandas as pd
from datetime import datetime
import logging

# Configure pandas display options
pd.set_option('display.float_format', lambda x: '₹{:,.2f}'.format(x) if isinstance(x, float) else x)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Portfolio:
    def __init__(self):
        self.kite = Config.get_kite()

    def get_holdings(self):
        """Get current holdings/investments."""
        try:
            holdings = self.kite.holdings()
            if not holdings:
                logger.info("No holdings found")
                return pd.DataFrame()
            
            # Convert to pandas DataFrame for better visualization
            df = pd.DataFrame(holdings)
            # Calculate current value and P&L
            df['current_value'] = df['last_price'] * df['quantity']
            df['total_pnl'] = df['current_value'] - (df['average_price'] * df['quantity'])
            
            # Select relevant columns
            columns = [
                'tradingsymbol', 'quantity', 'average_price', 
                'last_price', 'current_value', 'total_pnl'
            ]
            return df[columns].sort_values('current_value', ascending=False)
            
        except Exception as e:
            logger.error(f"Error fetching holdings: {str(e)}")
            return pd.DataFrame()

    def get_positions(self):
        """Get current day's positions."""
        try:
            positions = self.kite.positions()
            if not positions.get('net', []):
                logger.info("No positions found")
                return pd.DataFrame()
            
            # Convert to pandas DataFrame
            df = pd.DataFrame(positions['net'])
            # Calculate P&L percentages
            df['pnl_percentage'] = (df['pnl'] / abs(df['value'])) * 100
            
            # Select relevant columns
            columns = [
                'tradingsymbol', 'quantity', 'average_price',
                'last_price', 'value', 'pnl', 'pnl_percentage'
            ]
            return df[columns].sort_values('pnl', ascending=False)
            
        except Exception as e:
            logger.error(f"Error fetching positions: {str(e)}")
            return pd.DataFrame()

    def get_portfolio_summary(self):
        """Get summary of current portfolio."""
        try:
            holdings_df = self.get_holdings()
            positions_df = self.get_positions()
            available_margin = self.kite.margins()['equity']['available']['cash']
      
            
            summary = {
                "total_investment": holdings_df['average_price'].mul(holdings_df['quantity']).sum(),
                "current_value": holdings_df['current_value'].sum(),
                "total_pnl": holdings_df['total_pnl'].sum(),
                "day_pnl": positions_df['pnl'].sum() if not positions_df.empty else 0,
            }
            
            summary["pnl_percentage"] = (
                (summary["current_value"] - summary["total_investment"]) 
                / summary["total_investment"] * 100
            )

            summary["available_margin"] = available_margin
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating portfolio summary: {str(e)}")
            return {}