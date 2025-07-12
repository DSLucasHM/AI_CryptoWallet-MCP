#!/usr/bin/env python3
"""
Market Data MCP Server
A Gradio-based MCP server that provides cryptocurrency and financial market data tools.
"""

import os
import logging
import gradio as gr
from tools import (
    get_crypto_prices,
    get_fear_and_greed_index,
    get_bitcoin_dominance,
    get_fiat_exchange_rates
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

def create_gradio_interface():
    """Create and configure the Gradio interface."""
    with gr.Blocks(
        theme='soft',
        title="Market Data MCP Server",
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        """
    ) as demo:
        gr.Markdown("# 🛠️ Market Data Tool Server (MCP)")
        gr.Markdown(
            "This server exposes market data functions as tools for AI Agents. "
            "You can also test the tools directly using the interface below."
        )

        with gr.Tabs():
            with gr.TabItem("🪙 Crypto Prices"):
                gr.Markdown("Get current cryptocurrency prices in USD")
                crypto_in = gr.Textbox(
                    label="Coin IDs (comma-separated)",
                    value="bitcoin,ethereum,solana",
                    placeholder="bitcoin,ethereum,cardano"
                )
                crypto_out = gr.JSON(label="Price Data")
                crypto_btn = gr.Button("Get Prices", variant="primary")
                crypto_btn.click(
                    get_crypto_prices,
                    inputs=crypto_in,
                    outputs=crypto_out
                )

            with gr.TabItem("😨 Fear & Greed Index"):
                gr.Markdown("Get the current Crypto Fear & Greed Index")
                fng_out = gr.JSON(label="Fear & Greed Data")
                fng_btn = gr.Button("Get Index", variant="primary")
                fng_btn.click(
                    get_fear_and_greed_index,
                    inputs=None,
                    outputs=fng_out
                )

            with gr.TabItem("₿ Bitcoin Dominance"):
                gr.Markdown("Get Bitcoin's market cap dominance percentage")
                btcd_out = gr.JSON(label="Dominance Data")
                btcd_btn = gr.Button("Get Dominance", variant="primary")
                btcd_btn.click(
                    get_bitcoin_dominance,
                    inputs=None,
                    outputs=btcd_out
                )
                
            with gr.TabItem("💱 Fiat Exchange Rates"):
                gr.Markdown("Get current fiat currency exchange rates")
                fiat_in = gr.Textbox(
                    label="Base Currency (3-letter code)",
                    value="USD",
                    placeholder="USD, EUR, GBP, etc."
                )
                fiat_out = gr.JSON(label="Exchange Rates")
                fiat_btn = gr.Button("Get Rates", variant="primary")
                fiat_btn.click(
                    get_fiat_exchange_rates,
                    inputs=fiat_in,
                    outputs=fiat_out
                )

        gr.Markdown("---")
        gr.Markdown("**Note:** This server runs as an MCP (Model Context Protocol) server for AI agents.")

    return demo

def main():
    """Main entry point for the MCP server."""
    # Get configuration from environment variables
    port = int(os.getenv("MCP_SERVER_PORT", "7860"))
    host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
    
    logger.info(f"Starting Market Data MCP Server on {host}:{port}")
    
    # Create the Gradio interface
    demo = create_gradio_interface()
    
    # Launch the server with MCP support
    demo.launch(
        server_port=port,
        server_name=host,
        mcp_server=True,
        share=False,
        show_error=True
    )

if __name__ == "__main__":
    main()

