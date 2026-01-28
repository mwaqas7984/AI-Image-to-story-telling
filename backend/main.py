"""
FastAPI backend for the Image Storyteller application.

Clean, simple implementation with minimal dependencies.
"""

import io
import logging
from typing import Dict, List

from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import config
from vision_service import analyze_image

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Image Storyteller API",
    description="AI-powered image analysis and storytelling service",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Image Storyteller API is running!"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "2.0.0"}


@app.post("/api/image-analyze")
async def analyze_image_endpoint(file: UploadFile = File(...)):
    """
    Analyze an uploaded image and return analysis with story.
    
    Args:
        file: Uploaded image file
        
    Returns:
        Dict: Analysis results including caption, summary, objects, emotion, and story
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image"
            )
        
        # Read image bytes
        image_bytes = await file.read()
        
        # Check file size (limit to 10MB)
        if len(image_bytes) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must be less than 10MB"
            )
        
        logger.info(f"Processing image: {file.filename}, size: {len(image_bytes)} bytes")
        
        # Analyze image
        result = await analyze_image(image_bytes)
        
        logger.info("Analysis completed successfully")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze image"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
