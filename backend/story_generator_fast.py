"""
⚡ LIGHTNING FAST STORY GENERATOR ⚡
Quick version using smaller models for instant results
"""

import torch
import logging
from typing import List, Dict
import re
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

logger = logging.getLogger(__name__)


class FastStoryGenerator:
    """
    ⚡ Ultra-fast story generator using lightweight models
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"⚡ Initializing Fast Story Generator on {self.device}")
        
        # Try smaller models first for speed
        models_to_try = [
            "microsoft/DialoGPT-medium",  # 345MB - very fast
            "gpt2",                        # 124MB - fallback
        ]
        
        for model_name in models_to_try:
            try:
                logger.info(f"📦 Loading {model_name}")
                
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
                )
                
                if tokenizer.pad_token is None:
                    tokenizer.pad_token = tokenizer.eos_token
                
                self.generator = pipeline(
                    "text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    max_new_tokens=150,
                    temperature=0.9,
                    top_p=0.95,
                    do_sample=True,
                    repetition_penalty=1.1,
                    pad_token_id=tokenizer.eos_token_id
                )
                
                self.model_name = model_name
                logger.info(f"✅ Fast generator ready with {model_name}")
                break
                
            except Exception as e:
                logger.warning(f"❌ Failed {model_name}: {e}")
                continue
    
    def generate_story(self, caption: str, objects: List[str], emotion: str) -> List[str]:
        """
        ⚡ Generate story quickly
        """
        try:
            # Create smart prompt
            prompt = self._create_smart_prompt(caption, objects, emotion)
            
            # Generate
            result = self.generator(prompt)[0]["generated_text"]
            
            # Clean and return
            story = self._clean_result(result, prompt)
            
            logger.info(f"⚡ Fast story generated using {self.model_name}")
            return story
            
        except Exception as e:
            logger.error(f"❌ Fast generation failed: {e}")
            return self._fallback_story(caption, objects, emotion)
    
    def _create_smart_prompt(self, caption: str, objects: List[str], emotion: str) -> str:
        """
        🧠 Create intelligent prompt based on content
        """
        objects_str = ", ".join(objects[:5])
        
        # Detect context
        if 'garbage' in ' '.join(objects).lower() or 'trash' in ' '.join(objects).lower():
            return f"Write a story about community cleanup workers. Scene: {caption}. Objects: {objects_str}. Mood: {emotion}. Describe their environmental work and community service. Story:"
        elif 'desk' in ' '.join(objects).lower() or 'laptop' in ' '.join(objects).lower():
            return f"Write a story about office productivity. Scene: {caption}. Objects: {objects_str}. Mood: {emotion}. Describe professional work and focus. Story:"
        else:
            return f"Write a vivid story about this scene: {caption}. Objects: {objects_str}. Mood: {emotion}. Describe what's happening with sensory details. Story:"
    
    def _clean_result(self, result: str, prompt: str) -> List[str]:
        """
        🧹 Clean the generated text
        """
        # Remove prompt
        text = result.replace(prompt, "").strip()
        
        # Remove common artifacts
        text = text.replace("Story:", "").strip()
        
        # Split sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Clean and filter
        clean_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 8:
                clean_sentences.append(sentence + ".")
        
        # Ensure minimum length
        if len(clean_sentences) < 3:
            clean_sentences.extend([
                "The scene captures a meaningful moment.",
                "Every element contributes to the story.",
                "The atmosphere reflects the mood perfectly."
            ])
        
        return clean_sentences[:6]
    
    def _fallback_story(self, caption: str, objects: List[str], emotion: str) -> List[str]:
        """
        🛡️ Smart fallback
        """
        return [
            f"The image shows {caption.lower()}.",
            f"Visible elements include {', '.join(objects[:4])}.",
            f"The mood feels distinctly {emotion}.",
            "This moment tells its own visual story.",
            "The composition captures authentic human experience."
        ]


# 🌟 Global instance
try:
    fast_story_generator = FastStoryGenerator()
    logger.info("⚡⚡⚡ FAST STORY GENERATOR READY! ⚡⚡⚡")
except Exception as e:
    logger.error(f"💥 Failed to initialize Fast Generator: {e}")
    fast_story_generator = None

# Backward compatibility
ai_story_generator = fast_story_generator
