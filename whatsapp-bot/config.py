"""
Configuration management for the WhatsApp bot.
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import validator
from typing import Optional

class Settings(BaseSettings):
    """Application settings."""
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # OpenAI API
    openai_api_key: str
    
    # Evolution API configuration
    evolution_api_url: str
    evolution_instance_name: str
    evolution_api_key: str
    
    # MCP Server configuration
    mcp_server_url: str = "http://127.0.0.1:7860/gradio_api/mcp/sse"
    
    # Database configuration
    database_file: str = "portfolio.db"
    
    # WhatsApp configuration
    allowed_whatsapp_number: str
    
    # Logfire configuration 
    logfire_token: Optional[str] = None
    
    @validator('openai_api_key')
    def validate_openai_api_key(cls, v):
        if not v:
            raise ValueError('OPENAI_API_KEY is required')
        return v
    
    @validator('evolution_api_url')
    def validate_evolution_api_url(cls, v):
        if not v:
            raise ValueError('EVOLUTION_API_URL is required')
        return v.rstrip('/')
    
    @validator('evolution_instance_name')
    def validate_evolution_instance_name(cls, v):
        if not v:
            raise ValueError('EVOLUTION_INSTANCE_NAME is required')
        return v
    
    @validator('evolution_api_key')
    def validate_evolution_api_key(cls, v):
        if not v:
            raise ValueError('EVOLUTION_API_KEY is required')
        return v
    
    @validator('allowed_whatsapp_number')
    def validate_allowed_whatsapp_number(cls, v):
        if not v:
            raise ValueError('ALLOWED_WHATSAPP_NUMBER is required')
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()

