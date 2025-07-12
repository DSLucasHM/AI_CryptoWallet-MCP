"""
AI Agent configuration and initialization.
"""

import logging
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP

from tools import register_transaction, query_portfolio, send_whatsapp_message
from config import get_settings

logger = logging.getLogger(__name__)

def create_agent() -> Agent:
    """
    Create and configure the AI agent with local tools and MCP server connection.
    
    Returns:
        Configured Agent instance
    """
    try:
        settings = get_settings()
        
        # Define local tools
        local_tools = [
            register_transaction,
            query_portfolio,
            send_whatsapp_message
        ]
        
        mcp_connection = MCPServerHTTP(url=settings.mcp_server_url)
        
        agent = Agent(
            model="gpt-4o",
            tools=local_tools,
            mcp_servers=[mcp_connection],
            system_prompt="""
You are a helpful cryptocurrency portfolio management assistant integrated with WhatsApp.

Your capabilities include:
1. **Portfolio Management**: Register buy/sell transactions and query portfolio data
2. **Market Data**: Get real-time cryptocurrency prices, Fear & Greed Index, Bitcoin dominance, and fiat exchange rates
3. **WhatsApp Integration**: Send messages and respond to user queries

Key guidelines:
- Always be helpful, accurate, and concise in your responses
- When registering transactions, use the full CoinGecko coin ID (e.g., 'bitcoin', 'ethereum', 'solana')
- Format numbers clearly with appropriate decimal places
- Use emojis to make responses more engaging and readable
- If you need current market data to calculate portfolio values, use the market data tools first
- Always confirm transaction registrations with clear details
- Be proactive in providing relevant market insights when appropriate

For portfolio queries:
- Show transaction history when requested
- Calculate current portfolio values using live market data
- Provide insights on portfolio performance
- Suggest relevant market information based on holdings

Remember: You can access real-time market data through the MCP server tools, so always use current prices for calculations and insights.
            """.strip()
        )
        
        logger.info("AI Agent created successfully with local tools and MCP server connection")
        return agent
        
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise

