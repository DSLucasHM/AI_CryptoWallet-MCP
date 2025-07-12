#!/usr/bin/env python3
"""
WhatsApp Bot with MCP Integration
A FastAPI-based WhatsApp bot that integrates with an MCP server for market data.
"""

import os
import logging
import uvicorn
from fastapi import FastAPI, Body, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import init_db
from agent import create_agent
from config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global agent instance
agent = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global agent
    
    # Startup
    logger.info("Starting WhatsApp Bot application...")
    
    # Initialize database
    init_db()
    logger.info("Database initialized")
    
    # Create agent
    agent = create_agent()
    logger.info("AI Agent initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down WhatsApp Bot application...")

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="WhatsApp Bot with MCP Integration",
        description="A WhatsApp bot that provides cryptocurrency market data and portfolio management",
        version="1.0.0",
        lifespan=lifespan
    )
    

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

app = create_app()

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "WhatsApp Bot with MCP Integration",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    settings = get_settings()
    return {
        "status": "healthy",
        "database": "connected",
        "mcp_server": settings.mcp_server_url,
        "evolution_api": settings.evolution_api_url
    }

@app.post("/webhook/messages-upsert")
async def receive_webhook(background_tasks: BackgroundTasks, payload: dict = Body(...)):
    """
    Webhook endpoint for receiving WhatsApp messages from Evolution API.
    """
    logger.info("Webhook received at /messages-upsert")
    
    try:
        settings = get_settings()
        data = payload.get('data', {})
        key = data.get('key', {})
        message = data.get('message', {})

        # Extract message content and sender
        conversation = message.get('conversation')
        sender_jid = key.get('remoteJid')

        if conversation and sender_jid:
            # Check if sender is authorized
            if settings.allowed_whatsapp_number not in sender_jid:
                logger.warning(f"IGNORING message from unauthorized sender: {sender_jid}")
                return {"status": "message ignored - unauthorized sender"}

            message_text = conversation.strip()
            logger.info(f"VALID message received from {sender_jid}: '{message_text[:50]}...'")
            
            # Process message in background
            background_tasks.add_task(process_agent_and_reply, sender_jid, message_text)
            
            return {"status": "message queued for processing"}
        else:
            logger.debug("Webhook payload missing conversation or sender info")
            return {"status": "webhook acknowledged - no action needed"}

    except Exception as e:
        logger.error(f"Error in webhook endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

async def process_agent_and_reply(sender: str, text: str):
    """
    Process the message with the AI agent and send a reply.
    """
    global agent
    
    logger.info(f"Processing message from {sender}: '{text[:100]}...'")
    
    try:
        # Import here to avoid circular imports
        from tools import send_whatsapp_message
        
        # Run the agent with MCP servers
        async with agent.run_mcp_servers():
            response = await agent.run(text)
        
        reply_text = response.output
        logger.info(f"Agent response generated: '{reply_text[:100]}...'")
        
        # Send reply via WhatsApp
        result = await send_whatsapp_message(phone_number=sender, message=reply_text)
        logger.info(f"Reply sent to {sender}: {result}")
        
    except Exception as e:
        logger.error(f"Error processing agent for {sender}: {e}", exc_info=True)
        
        # Send error message to user
        try:
            from tools import send_whatsapp_message
            await send_whatsapp_message(
                phone_number=sender,
                message="Sorry, an error occurred while processing your request. Please try again later."
            )
        except Exception as send_error:
            logger.error(f"Failed to send error message: {send_error}")

def main():
    """Main entry point for the WhatsApp bot."""
    settings = get_settings()
    
    logger.info(f"Starting WhatsApp Bot Server on {settings.host}:{settings.port}")
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )

if __name__ == "__main__":
    main()

