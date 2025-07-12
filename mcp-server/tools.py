"""
Market Data Tools
Provides cryptocurrency and financial market data through various APIs.
"""

import httpx
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def get_crypto_prices(coin_ids: str) -> Dict[str, Any]:
    """
    Gets the current price in USD for one or more cryptocurrencies.
    
    Args:
        coin_ids: Comma-separated list of CoinGecko coin IDs (e.g., "bitcoin,ethereum")
    
    Returns:
        Dictionary containing price data for the requested cryptocurrencies
    """
    try:
        coin_id_list = [c.strip() for c in coin_ids.split(',') if c.strip()]
        logger.info(f"Fetching crypto prices for: {coin_id_list}")
        
        if not coin_id_list:
            return {"error": "No valid coin IDs provided"}
        
        ids_string = ",".join([coin_id.lower() for coin_id in coin_id_list])
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_string}&vs_currencies=usd"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Successfully fetched prices for {len(data)} cryptocurrencies")
            return data
            
    except httpx.HTTPStatusError as e:
        error_msg = f"API request failed with status {e.response.status_code}"
        logger.error(error_msg)
        return {"error": error_msg}
    except httpx.TimeoutException:
        error_msg = "Request timed out"
        logger.error(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

async def get_fear_and_greed_index() -> Dict[str, Any]:
    """
    Gets the current Crypto Fear & Greed Index.
    
    Returns:
        Dictionary containing the current fear and greed index data
    """
    try:
        logger.info("Fetching Fear & Greed Index")
        url = "https://api.alternative.me/fng/?limit=1"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            logger.info("Successfully fetched Fear & Greed Index")
            return data
            
    except httpx.HTTPStatusError as e:
        error_msg = f"API request failed with status {e.response.status_code}"
        logger.error(error_msg)
        return {"error": error_msg}
    except httpx.TimeoutException:
        error_msg = "Request timed out"
        logger.error(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

async def get_bitcoin_dominance() -> Dict[str, Any]:
    """
    Gets the current Bitcoin Dominance percentage (BTC.D).
    
    Returns:
        Dictionary containing Bitcoin dominance percentage
    """
    try:
        logger.info("Fetching Bitcoin Dominance")
        url = "https://api.coingecko.com/api/v3/global"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            data = response.json().get('data', {})
            btc_dominance = data.get('market_cap_percentage', {}).get('btc', 0.0)
            
            result = {"bitcoin_dominance_percentage": btc_dominance}
            logger.info(f"Successfully fetched Bitcoin Dominance: {btc_dominance}%")
            return result
            
    except httpx.HTTPStatusError as e:
        error_msg = f"API request failed with status {e.response.status_code}"
        logger.error(error_msg)
        return {"error": error_msg}
    except httpx.TimeoutException:
        error_msg = "Request timed out"
        logger.error(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

async def get_fiat_exchange_rates(base_currency: str) -> Dict[str, Any]:
    """
    Gets the latest exchange rates for fiat currencies.
    
    Args:
        base_currency: The base currency code (e.g., "USD", "EUR")
    
    Returns:
        Dictionary containing exchange rates relative to the base currency
    """
    try:
        base_currency = base_currency.upper().strip()
        logger.info(f"Fetching exchange rates for base currency: {base_currency}")
        
        if not base_currency or len(base_currency) != 3:
            return {"error": "Invalid currency code. Please provide a 3-letter currency code."}
        
        url = f"https://open.er-api.com/v6/latest/{base_currency}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Successfully fetched exchange rates for {base_currency}")
            return data
            
    except httpx.HTTPStatusError as e:
        error_msg = f"API request failed with status {e.response.status_code}"
        logger.error(error_msg)
        return {"error": error_msg}
    except httpx.TimeoutException:
        error_msg = "Request timed out"
        logger.error(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

