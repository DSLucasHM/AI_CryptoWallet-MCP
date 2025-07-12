"""
Local tools for the WhatsApp bot agent.
"""

import httpx
import logging
from typing import Optional

from database import Transaction, add_transaction, get_transactions, get_portfolio_summary
from config import get_settings

logger = logging.getLogger(__name__)

def register_transaction(
    crypto_symbol: str,
    quantity: float,
    price_usd: float,
    exchange: str,
    transaction_type: str
) -> str:
    """
    Register a new crypto transaction in the portfolio.
    
    Args:
        crypto_symbol: The cryptocurrency symbol (use CoinGecko ID format, e.g., 'bitcoin', 'ethereum')
        quantity: The quantity of cryptocurrency
        price_usd: The price in USD at the time of transaction
        exchange: The exchange where the transaction occurred
        transaction_type: Either 'buy' or 'sell'
    
    Returns:
        Confirmation message
    """
    try:
        # Validate transaction type
        if transaction_type.lower() not in ['buy', 'sell']:
            return "❌ Error: Transaction type must be either 'buy' or 'sell'"
        
        # Validate quantity and price
        if quantity <= 0:
            return "❌ Error: Quantity must be greater than 0"
        
        if price_usd <= 0:
            return "❌ Error: Price must be greater than 0"
        
        # Create transaction
        tx = Transaction(
            crypto_symbol=crypto_symbol.lower(),
            quantity=quantity,
            price_usd_at_transaction=price_usd,
            exchange=exchange,
            transaction_type=transaction_type.lower()
        )
        
        # Add to database
        transaction_id = add_transaction(tx)
        
        logger.info(f"Transaction registered: {transaction_type} {quantity} {crypto_symbol} at ${price_usd}")
        
        return (
            f"✅ Transaction registered successfully!\n"
            f"📝 ID: {transaction_id}\n"
            f"🪙 {transaction_type.capitalize()}: {quantity} {crypto_symbol.upper()}\n"
            f"💰 Price: ${price_usd:,.2f}\n"
            f"🏪 Exchange: {exchange}"
        )
        
    except Exception as e:
        logger.error(f"Error registering transaction: {e}")
        return f"❌ Error registering transaction: {str(e)}"

def query_portfolio(crypto_symbol: Optional[str] = None) -> str:
    """
    Query the portfolio database and return transaction history.
    
    Args:
        crypto_symbol: Optional filter by specific cryptocurrency
    
    Returns:
        Portfolio information as a formatted string
    """
    try:
        if crypto_symbol:
            transactions = get_transactions(crypto_symbol.lower())
            if not transactions:
                return f"📊 No transactions found for {crypto_symbol.upper()}"
            
            result = f"📊 Transaction history for {crypto_symbol.upper()}:\n\n"
        else:
            transactions = get_transactions()
            if not transactions:
                return "📊 No transactions found in portfolio"
            
            result = "📊 Complete transaction history:\n\n"
        
        # Format transactions
        for i, tx in enumerate(transactions[:10], 1):  # Limit to 10 most recent
            result += (
                f"{i}. {tx['transaction_type'].upper()}: {tx['quantity']} {tx['crypto_symbol'].upper()}\n"
                f"   💰 Price: ${tx['price_usd_at_transaction']:,.2f}\n"
                f"   🏪 Exchange: {tx['exchange']}\n"
                f"   📅 Date: {tx['created_at']}\n\n"
            )
        
        if len(transactions) > 10:
            result += f"... and {len(transactions) - 10} more transactions\n\n"
        
        # Add portfolio summary
        summary = get_portfolio_summary()
        if summary['holdings']:
            result += "💼 Current Holdings:\n"
            for holding in summary['holdings']:
                result += (
                    f"• {holding['crypto_symbol'].upper()}: {holding['net_quantity']:.6f} "
                    f"(avg: ${holding['avg_price']:,.2f})\n"
                )
        
        return result
        
    except Exception as e:
        logger.error(f"Error querying portfolio: {e}")
        return f"❌ Error querying portfolio: {str(e)}"

async def send_whatsapp_message(phone_number: str, message: str) -> str:
    """
    Send a text message to a specified phone number via WhatsApp using Evolution API.
    
    Args:
        phone_number: The recipient's phone number (with or without @s.whatsapp.net)
        message: The message text to send
    
    Returns:
        Status message indicating success or failure
    """
    try:
        settings = get_settings()
        
        # Check if sender is authorized
        if settings.allowed_whatsapp_number not in phone_number:
            logger.warning(f"BLOCKED sending message to unauthorized number: {phone_number}")
            return "❌ Error: This bot can only send messages to the authorized number."
        
        # Clean phone number (remove @s.whatsapp.net if present)
        phone_number_cleaned = phone_number.split('@')[0]
        
        # Prepare API request
        url = f"{settings.evolution_api_url}/message/sendText/{settings.evolution_instance_name}"
        headers = {
            "apikey": settings.evolution_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "number": phone_number_cleaned,
            "text": message
        }
        
        logger.info(f"Sending message to {phone_number_cleaned}: '{message[:50]}...'")
        
        # Send request
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            
            logger.info(f"Message sent successfully to {phone_number_cleaned}")
            return "✅ Message sent successfully"
            
    except httpx.HTTPStatusError as e:
        error_response = e.response.text
        logger.error(f"Evolution API error: {error_response}")
        return f"❌ Failed to send message. API Error: {error_response}"
        
    except httpx.TimeoutException:
        logger.error("Request to Evolution API timed out")
        return "❌ Failed to send message: Request timed out"
        
    except Exception as e:
        logger.error(f"Unexpected error in send_whatsapp_message: {e}", exc_info=True)
        return f"❌ Failed to send message: {str(e)}"

