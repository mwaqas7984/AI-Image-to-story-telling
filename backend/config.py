"""
Configuration management for the Image Storyteller backend.

This module handles environment variables and provides defaults
for optional configuration values.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Config:
    """Configuration class for the application."""
    
    def __init__(self):
        """Initialize configuration with environment variables or defaults."""
        # Vision API configuration (for future real AI integration)
        self.vision_api_url: Optional[str] = os.getenv("VISION_API_URL")
        self.vision_api_key: Optional[str] = os.getenv("VISION_API_KEY")
        
        # File upload limits
        self.max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
        self.max_file_size_bytes: int = self.max_file_size_mb * 1024 * 1024
        
        # Server configuration
        self.host: str = os.getenv("HOST", "127.0.0.1")
        self.port: int = int(os.getenv("PORT", "8000"))
        
        # CORS configuration
        self.cors_origins: list = ["*"]  # Allow all origins for local development


# Global config instance
config = Config()
