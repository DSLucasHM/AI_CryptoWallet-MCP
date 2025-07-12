"""
Database operations for portfolio management.
"""

import sqlite3
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from config import get_settings

logger = logging.getLogger(__name__)

class Transaction(BaseModel):
    """Transaction model."""
    crypto_symbol: str
    quantity: float
    price_usd_at_transaction: float
    exchange: str
    transaction_type: str

def get_db_connection():
    """Get a database connection."""
    settings = get_settings()
    conn = sqlite3.connect(settings.database_file)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crypto_symbol TEXT NOT NULL,
                quantity REAL NOT NULL,
                price_usd_at_transaction REAL NOT NULL,
                exchange TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
    finally:
        conn.close()

def add_transaction(tx_data: Transaction) -> int:
    """
    Add a transaction to the database.
    
    Args:
        tx_data: Transaction data
        
    Returns:
        The ID of the inserted transaction
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO transactions 
            (crypto_symbol, quantity, price_usd_at_transaction, exchange, transaction_type)
            VALUES (?, ?, ?, ?, ?)
        """, (
            tx_data.crypto_symbol.lower(),
            tx_data.quantity,
            tx_data.price_usd_at_transaction,
            tx_data.exchange,
            tx_data.transaction_type
        ))
        
        transaction_id = cursor.lastrowid
        conn.commit()
        
        logger.info(f"Transaction added with ID: {transaction_id}")
        return transaction_id
        
    except Exception as e:
        logger.error(f"Error adding transaction: {e}")
        raise
    finally:
        conn.close()

def get_transactions(crypto_symbol: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get transactions from the database.
    
    Args:
        crypto_symbol: Optional filter by crypto symbol
        
    Returns:
        List of transactions
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if crypto_symbol:
            cursor.execute(
                "SELECT * FROM transactions WHERE crypto_symbol = ? ORDER BY created_at DESC",
                (crypto_symbol.lower(),)
            )
        else:
            cursor.execute("SELECT * FROM transactions ORDER BY created_at DESC")
        
        transactions = [dict(row) for row in cursor.fetchall()]
        
        logger.info(f"Retrieved {len(transactions)} transactions")
        return transactions
        
    except Exception as e:
        logger.error(f"Error retrieving transactions: {e}")
        raise
    finally:
        conn.close()

def get_portfolio_summary() -> Dict[str, Any]:
    """
    Get a summary of the portfolio.
    
    Returns:
        Portfolio summary with holdings by crypto symbol
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                crypto_symbol,
                SUM(CASE WHEN transaction_type = 'buy' THEN quantity ELSE -quantity END) as net_quantity,
                AVG(price_usd_at_transaction) as avg_price,
                COUNT(*) as transaction_count
            FROM transactions 
            GROUP BY crypto_symbol
            HAVING net_quantity > 0
            ORDER BY crypto_symbol
        """)
        
        holdings = []
        for row in cursor.fetchall():
            holdings.append({
                'crypto_symbol': row['crypto_symbol'],
                'net_quantity': row['net_quantity'],
                'avg_price': row['avg_price'],
                'transaction_count': row['transaction_count']
            })
        
        logger.info(f"Portfolio summary generated for {len(holdings)} holdings")
        return {
            'holdings': holdings,
            'total_holdings': len(holdings)
        }
        
    except Exception as e:
        logger.error(f"Error generating portfolio summary: {e}")
        raise
    finally:
        conn.close()

