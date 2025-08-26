"""
Investor ITR & GST Calculator - Calculation Logic Module

This module contains the core calculation logic for:
- FIFO method for matching buy/sell transactions
- Capital gains calculation (STCG/LTCG)
- GST calculation on brokerage
- Summary calculations for tax reporting
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Tuple, Dict
import numpy as np


class Trade:
    """Represents a single trade transaction"""
    
    def __init__(self, date: datetime, trade_type: str, stock: str, 
                 qty: int, price: float, brokerage: float, dividend: float = 0):
        self.date = date
        self.trade_type = trade_type.upper()
        self.stock = stock
        self.qty = qty
        self.price = price
        self.brokerage = brokerage
        self.dividend = dividend
        self.remaining_qty = qty  # For FIFO tracking
    
    def __repr__(self):
        return f"Trade({self.date.date()}, {self.trade_type}, {self.stock}, {self.qty}, {self.price})"


class MatchedTrade:
    """Represents a matched buy-sell pair for capital gains calculation"""
    
    def __init__(self, buy_trade: Trade, sell_trade: Trade, matched_qty: int):
        self.buy_date = buy_trade.date
        self.sell_date = sell_trade.date
        self.stock = buy_trade.stock
        self.matched_qty = matched_qty
        self.buy_price = buy_trade.price
        self.sell_price = sell_trade.price
        self.buy_brokerage = (buy_trade.brokerage * matched_qty) / buy_trade.qty
        self.sell_brokerage = (sell_trade.brokerage * matched_qty) / sell_trade.qty
        self.total_brokerage = self.buy_brokerage + self.sell_brokerage
        
        # Calculate gain/loss
        self.buy_value = self.buy_price * matched_qty
        self.sell_value = self.sell_price * matched_qty
        self.gain = self.sell_value - self.buy_value - self.total_brokerage
        
        # Determine STCG/LTCG (12 months threshold for equity)
        days_held = (self.sell_date - self.buy_date).days
        self.is_ltcg = days_held > 365  # More than 12 months
        self.gain_type = "LTCG" if self.is_ltcg else "STCG"
        
        # Calculate GST on brokerage (18%)
        self.gst_on_brokerage = self.total_brokerage * 0.18
    
    def to_dict(self):
        """Convert to dictionary for DataFrame creation"""
        return {
            'Buy Date': self.buy_date.strftime('%Y-%m-%d'),
            'Sell Date': self.sell_date.strftime('%Y-%m-%d'),
            'Stock': self.stock,
            'Qty': self.matched_qty,
            'Buy Price': round(self.buy_price, 2),
            'Sell Price': round(self.sell_price, 2),
            'Buy Value': round(self.buy_value, 2),
            'Sell Value': round(self.sell_value, 2),
            'Brokerage': round(self.total_brokerage, 2),
            'Gain/Loss': round(self.gain, 2),
            'Type': self.gain_type,
            'GST on Brokerage': round(self.gst_on_brokerage, 2),
            'Days Held': (self.sell_date - self.buy_date).days
        }


class InvestorCalculator:
    """Main calculator class for processing trades and calculating taxes"""
    
    def __init__(self):
        self.trades = []
        self.matched_trades = []
        self.buy_trades_by_stock = {}  # For FIFO tracking
    
    def load_csv_data(self, csv_file) -> bool:
        """Load and validate CSV data"""
        try:
            df = pd.read_csv(csv_file)
            
            # Validate required columns
            required_columns = ['Date', 'Type', 'Stock', 'Qty', 'Price', 'Brokerage']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Process each row
            for _, row in df.iterrows():
                try:
                    date = pd.to_datetime(row['Date']).to_pydatetime()
                    trade_type = str(row['Type']).strip()
                    stock = str(row['Stock']).strip()
                    qty = int(row['Qty'])
                    price = float(row['Price'])
                    brokerage = float(row['Brokerage'])
                    
                    # Handle optional dividend column
                    dividend = 0
                    if 'Dividend' in df.columns and pd.notna(row['Dividend']):
                        dividend = float(row['Dividend'])
                    
                    trade = Trade(date, trade_type, stock, qty, price, brokerage, dividend)
                    self.trades.append(trade)
                    
                except (ValueError, TypeError) as e:
                    raise ValueError(f"Error processing row: {row.to_dict()}. Error: {str(e)}")
            
            return True
            
        except Exception as e:
            raise Exception(f"Error loading CSV: {str(e)}")
    
    def calculate_fifo_matching(self):
        """Calculate capital gains using FIFO method"""
        # Group trades by stock and sort by date
        trades_by_stock = {}
        for trade in self.trades:
            if trade.stock not in trades_by_stock:
                trades_by_stock[trade.stock] = []
            trades_by_stock[trade.stock].append(trade)
        
        # Sort trades by date for each stock
        for stock in trades_by_stock:
            trades_by_stock[stock].sort(key=lambda x: x.date)
        
        # Process FIFO matching for each stock
        self.matched_trades = []
        
        for stock, stock_trades in trades_by_stock.items():
            buy_queue = []  # Queue of buy trades with remaining quantities
            
            for trade in stock_trades:
                if trade.trade_type == 'BUY':
                    buy_queue.append(trade)
                
                elif trade.trade_type == 'SELL':
                    remaining_sell_qty = trade.qty
                    
                    while remaining_sell_qty > 0 and buy_queue:
                        buy_trade = buy_queue[0]
                        
                        if buy_trade.remaining_qty <= 0:
                            buy_queue.pop(0)
                            continue
                        
                        # Match quantity (minimum of remaining buy and sell quantities)
                        matched_qty = min(buy_trade.remaining_qty, remaining_sell_qty)
                        
                        # Create matched trade
                        matched_trade = MatchedTrade(buy_trade, trade, matched_qty)
                        self.matched_trades.append(matched_trade)
                        
                        # Update remaining quantities
                        buy_trade.remaining_qty -= matched_qty
                        remaining_sell_qty -= matched_qty
                        
                        # Remove buy trade if fully consumed
                        if buy_trade.remaining_qty <= 0:
                            buy_queue.pop(0)
                    
                    # If there's remaining sell quantity, it means insufficient buy trades
                    if remaining_sell_qty > 0:
                        print(f"Warning: Insufficient buy quantity for {stock}. "
                              f"Remaining sell qty: {remaining_sell_qty}")
    
    def calculate_summary(self) -> Dict:
        """Calculate summary statistics for tax reporting"""
        total_stcg = sum(mt.gain for mt in self.matched_trades if mt.gain_type == 'STCG')
        total_ltcg = sum(mt.gain for mt in self.matched_trades if mt.gain_type == 'LTCG')
        total_gst = sum(mt.gst_on_brokerage for mt in self.matched_trades)
        total_dividends = sum(trade.dividend for trade in self.trades if trade.dividend > 0)
        
        # Calculate total brokerage
        total_brokerage = sum(trade.brokerage for trade in self.trades)
        
        # Final taxable income calculation
        taxable_income = total_stcg + total_ltcg + total_dividends
        
        return {
            'Total STCG': round(total_stcg, 2),
            'Total LTCG': round(total_ltcg, 2),
            'Total Dividends': round(total_dividends, 2),
            'Total Brokerage': round(total_brokerage, 2),
            'Total GST on Brokerage': round(total_gst, 2),
            'Final Taxable Income': round(taxable_income, 2),
            'Total Trades Matched': len(self.matched_trades),
            'Total Buy Trades': len([t for t in self.trades if t.trade_type == 'BUY']),
            'Total Sell Trades': len([t for t in self.trades if t.trade_type == 'SELL'])
        }
    
    def get_results_dataframe(self) -> pd.DataFrame:
        """Get matched trades as DataFrame for display and export"""
        if not self.matched_trades:
            return pd.DataFrame()
        
        results = [mt.to_dict() for mt in self.matched_trades]
        df = pd.DataFrame(results)
        return df
    
    def process_portfolio(self, csv_file) -> Tuple[pd.DataFrame, Dict]:
        """Main method to process portfolio and return results"""
        # Load data
        self.load_csv_data(csv_file)
        
        # Calculate FIFO matching
        self.calculate_fifo_matching()
        
        # Get results
        results_df = self.get_results_dataframe()
        summary = self.calculate_summary()
        
        return results_df, summary