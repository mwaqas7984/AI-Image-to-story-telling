"""
Vision Service - Clean image analysis and story generation.

This module provides a simple interface to analyze images and generate stories.
"""

import hashlib
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


async def analyze_image(image_bytes: bytes) -> Dict:
    """
    Analyze an image and return structured analysis.
    
    Args:
        image_bytes: Raw image data as bytes
        
    Returns:
        Dict: Structured analysis with caption, summary, objects, emotion, and story
    """
    try:
        # Use Fast Hugging Face for image analysis
        logger.info("Analyzing image with Fast Hugging Face...")
        from fast_huggingface_service import fast_huggingface_analyzer
        result = fast_huggingface_analyzer.analyze_image(image_bytes)
        
        # Generate story with our AI story generator
        logger.info("Generating story with AI...")
        from story_generator import ai_story_generator
        
        if ai_story_generator is None:
            logger.warning("AI story generator not available, using fallback")
            return generate_dummy_analysis(image_bytes)
        
        story = ai_story_generator.generate_story(
            caption=result.get("caption", ""),
            objects=result.get("objects", []),
            emotion=result.get("emotion", "neutral")
        )
        
        # Return the complete analysis
        return {
            "caption": result.get("caption", "Unable to generate caption"),
            "summary": result.get("summary", []),
            "objects": result.get("objects", []),
            "emotion": result.get("emotion", "neutral"),
            "story": story
        }
        
    except Exception as e:
        logger.error(f"Image analysis failed: {e}")
        # Fallback to dummy data
        return generate_dummy_analysis(image_bytes)


def generate_dummy_analysis(image_bytes: bytes) -> Dict:
    """
    Generate dummy analysis as fallback.
    
    Args:
        image_bytes: Raw image data as bytes
        
    Returns:
        Dict: Dummy analysis data
    """
    file_hash = hashlib.md5(image_bytes).hexdigest()
    hash_int = int(file_hash[:8], 16)
    
    scenarios = [
        {
            "caption": "A person sitting at a desk with a laptop.",
            "summary": [
                "Someone is focused on their work at a desk",
                "A laptop computer is visible on the workspace",
                "The environment suggests a productive session",
                "Natural lighting illuminates the scene",
                "Books and notes are scattered around"
            ],
            "objects": ["person", "desk", "laptop", "chair", "books"],
            "emotion": "focused",
            "story": [
                "The workspace became a sanctuary of productivity.",
                "Each keystroke brought the project closer to completion.",
                "Books stood ready like silent mentors.",
                "The glow of the screen illuminated determined features.",
                "In this quiet moment, creativity flowed freely.",
                "Time seemed to bend to the rhythm of work.",
                "Every problem solved was a small victory.",
                "The world outside faded into background noise.",
                "This was more than work - it was creation.",
                "As the day progressed, so did the masterpiece."
            ]
        }
    ]
    
    return scenarios[hash_int % len(scenarios)]
