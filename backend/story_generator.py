"""
🎯 Clean GPT-2 Story Generator
Simple, reliable, with smart prompting
"""

import torch
import logging
from typing import List, Dict
import re
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

logger = logging.getLogger(__name__)


class CleanStoryGenerator:
    """
    🎯 Clean GPT-2 generator with smart prompting
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"🎯 Initializing Clean GPT-2 Generator on {self.device}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
            self.model = AutoModelForCausalLM.from_pretrained("gpt2")
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=200,
                temperature=0.8,
                top_p=0.9,
                do_sample=True,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            logger.info("✅ Clean GPT-2 Generator ready!")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize: {e}")
            self.generator = None
    
    def generate_story(self, caption: str, objects: List[str], emotion: str) -> List[str]:
        """
        🎯 Generate story with enhanced caption prompting
        """
        if not self.generator:
            return self._fallback_story(caption, objects, emotion)
        
        try:
            # Create enhanced detailed caption
            detailed_caption = self._create_detailed_caption(caption, objects, emotion)
            
            # Use the detailed caption as the prompt for GPT-2
            result = self.generator(detailed_caption)[0]["generated_text"]
            
            # Clean and format
            story = self._clean_and_format(result, detailed_caption)
            
            logger.info("✅ Story generated from detailed caption")
            return story
            
        except Exception as e:
            logger.error(f"❌ Generation failed: {e}")
            return self._fallback_story(caption, objects, emotion)
    
    def _create_detailed_caption(self, caption: str, objects: List[str], emotion: str) -> str:
        """
        🎭 Create a story prompt based on image analysis - this will be fed to GPT-2 to generate a narrative
        """
        objects_str = ", ".join(objects[:6])
        objects_lower = " ".join(objects).lower()
        
        # Detect the "air" or atmosphere of the picture
        air_detection = self._detect_picture_air(objects_lower, emotion)
        
        # Build story prompt based on detected context
        if air_detection["activity_type"] == "cleanup_work":
            return f"""Once upon a time, {air_detection['participants']} were on a mission to clean up their community. {caption}. Armed with {objects_str}, they worked together with determination. {air_detection['atmosphere']} Their journey that day would become a story of hope and environmental stewardship. The mood was {emotion} as they began their important work. """
        
        elif air_detection["activity_type"] == "office_work":
            return f"""In the world of professional ambition, {air_detection['participants']} found themselves immersed in their daily tasks. {caption}. Surrounded by {objects_str}, they navigated the challenges of their work environment. {air_detection['atmosphere']} This particular day would bring unexpected opportunities and lessons. The mood was {emotion} as they pursued their goals. """
        
        elif air_detection["activity_type"] == "play_recreation":
            return f"""On a bright and cheerful day, {air_detection['participants']} discovered the joy of play and recreation. {caption}. With {objects_str} adding to the fun, they embraced the moment with pure delight. {air_detection['atmosphere']} This day would become a cherished memory of laughter and friendship. The mood was {emotion} as they lost themselves in the joy of the moment. """
        
        elif air_detection["activity_type"] == "transportation":
            return f"""In the bustling world of movement and journey, {air_detection['participants']} embarked on an important trip. {caption}. With {objects_str} as their companions, they navigated the paths before them. {air_detection['atmosphere']} This journey would teach them valuable lessons about patience and direction. The mood was {emotion} as they moved toward their destination. """
        
        elif air_detection["activity_type"] == "nature_outdoor":
            return f"""Deep in the embrace of nature, {air_detection['participants']} discovered the beauty of the natural world. {caption}. Surrounded by {objects_str}, they felt a profound connection to the environment. {air_detection['atmosphere']} This experience would transform their understanding of life and tranquility. The mood was {emotion} as they immersed themselves in natural wonder. """
        
        elif air_detection["activity_type"] == "social_gathering":
            return f"""In a moment of human connection, {air_detection['participants']} came together to share their lives. {caption}. With {objects_str} creating the perfect setting, they opened their hearts to one another. {air_detection['atmosphere']} This gathering would strengthen bonds and create lasting memories. The mood was {emotion} as they celebrated their community. """
        
        elif air_detection["activity_type"] == "relaxation":
            return f"""In the peaceful sanctuary of rest, {air_detection['participants']} found solace from the busy world. {caption}. With {objects_str} providing comfort, they surrendered to moments of pure tranquility. {air_detection['atmosphere']} This time of rest would rejuvenate their spirits and restore their energy. The mood was {emotion} as they embraced the gift of relaxation. """
        
        else:
            return f"""In a moment captured in time, {air_detection['participants']} found themselves in an extraordinary situation. {caption}. With {objects_str} around them, they faced the circumstances before them. {air_detection['atmosphere']} This moment would reveal their true character and shape their future. The mood was {emotion} as they stood at this crossroads of experience. """
    
    def _detect_picture_air(self, objects: List[str], emotion: str) -> Dict[str, str]:
        """
        🎭 Detect the "air" or atmosphere of the picture
        """
        objects_text = " ".join(objects).lower()
        
        # Detect participants
        if any(word in objects_text for word in ["men", "people", "person", "man", "woman"]):
            if "men" in objects_text:
                participants = "men"
            elif "people" in objects_text:
                participants = "people"
            else:
                participants = "individuals"
        else:
            participants = "figures"
        
        # Detect activity type and atmosphere
        if any(word in objects_text for word in ["garbage", "trash", "bag", "clean", "waste"]):
            return {
                "activity_type": "cleanup_work",
                "participants": participants,
                "atmosphere": "The air is filled with purpose and community service."
            }
        
        elif any(word in objects_text for word in ["desk", "laptop", "computer", "work", "office"]):
            return {
                "activity_type": "office_work", 
                "participants": participants,
                "atmosphere": "The air is focused and professional."
            }
        
        elif any(word in objects_text for word in ["ball", "game", "play", "sport", "toy", "fun"]):
            return {
                "activity_type": "play_recreation",
                "participants": participants, 
                "atmosphere": "The air is filled with joy and playful energy."
            }
        
        elif any(word in objects_text for word in ["car", "vehicle", "truck", "street", "road", "traffic"]):
            return {
                "activity_type": "transportation",
                "participants": participants,
                "atmosphere": "The air is dynamic and filled with movement."
            }
        
        elif any(word in objects_text for word in ["tree", "grass", "park", "nature", "outdoor", "garden"]):
            return {
                "activity_type": "nature_outdoor",
                "participants": participants,
                "atmosphere": "The air is fresh and natural."
            }
        
        elif any(word in objects_text for word in ["chair", "table", "gathering", "group", "together", "social"]):
            return {
                "activity_type": "social_gathering",
                "participants": participants,
                "atmosphere": "The air is social and interactive."
            }
        
        elif any(word in objects_text for word in ["sofa", "couch", "relax", "rest", "comfortable", "lounge"]):
            return {
                "activity_type": "relaxation",
                "participants": participants,
                "atmosphere": "The air is calm and relaxing."
            }
        
        else:
            return {
                "activity_type": "general",
                "participants": participants,
                "atmosphere": "The air captures a moment of authentic human experience."
            }
    
    def _clean_and_format(self, result: str, prompt: str) -> List[str]:
        """
        🧹 Clean and format the generated story as a single paragraph
        """
        # Extract the caption from the prompt (first sentence)
        caption_part = prompt.split('.')[0] + '.'
        
        # Remove the prompt from the result
        story_text = result.replace(prompt, "").strip()
        
        # Remove common artifacts
        story_text = story_text.replace("Story:", "").strip()
        story_text = story_text.replace("Write a story", "").strip()
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', story_text)
        
        # Clean and filter sentences
        clean_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10 and not self._is_prompt_fragment(sentence):
                clean_sentences.append(sentence.strip())
        
        # If we don't have enough good sentences, create contextual content
        if len(clean_sentences) < 2:
            clean_sentences = self._create_contextual_sentences(clean_sentences)
        
        # Combine caption with generated sentences into a single paragraph
        full_story = caption_part + " " + ". ".join(clean_sentences) + "."
        
        # Return as single item list (one paragraph)
        return [full_story]
    
    def _is_prompt_fragment(self, sentence: str) -> bool:
        """Check if sentence is a prompt fragment"""
        prompt_words = ["write", "describe", "story", "scene", "mood", "objects", "visible"]
        return any(word in sentence.lower() for word in prompt_words)
    
    def _create_contextual_sentences(self, existing_sentences: List[str]) -> List[str]:
        """Create contextual sentences based on the story"""
        contextual = [
            "The scene captures a moment of authentic human activity.",
            "Every element in the frame contributes to the narrative.",
            "The atmosphere reflects the emotional tone perfectly.",
            "This moment tells a meaningful visual story.",
            "The composition reveals deeper layers of meaning."
        ]
        
        # Combine existing with contextual
        return existing_sentences + contextual[:7-len(existing_sentences)]
    
    def _fallback_story(self, caption: str, objects: List[str], emotion: str) -> List[str]:
        """
        🛡️ Smart contextual fallback
        """
        return [
            f"The image depicts {caption.lower()}.",
            f"Visible elements include {', '.join(objects[:5])}.",
            f"The overall mood feels distinctly {emotion}.",
            "This moment captures a genuine human experience.",
            "The scene tells its own compelling visual story.",
            "Every detail adds depth to the composition."
        ]


# 🌟 Global instance
try:
    clean_story_generator = CleanStoryGenerator()
    logger.info("🎯🎯🎯 CLEAN STORY GENERATOR READY! 🎯🎯🎯")
except Exception as e:
    logger.error(f"💥 Failed to initialize Clean Generator: {e}")
    clean_story_generator = None

# Backward compatibility
ai_story_generator = clean_story_generator
