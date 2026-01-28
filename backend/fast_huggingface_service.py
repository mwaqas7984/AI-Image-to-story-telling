"""
Fast Hugging Face Vision Service - Small models, instant results!

This module uses lightweight Hugging Face models that download quickly
but still provide excellent image analysis.
"""

import io
import re
import random
import torch
from typing import Dict, List, Optional
from PIL import Image
from transformers import (
    BlipProcessor, BlipForConditionalGeneration,
    DetrImageProcessor, DetrForObjectDetection
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FastHuggingFaceAnalyzer:
    """
    Fast Hugging Face analyzer using small, efficient models.
    """
    
    def __init__(self):
        """Initialize the Fast Hugging Face analyzer."""
        logger.info("Initializing Fast Hugging Face Analyzer...")
        
        # Device configuration
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        # Use smaller, faster models
        self.blip_model_name = "Salesforce/blip-image-captioning-base"  # Much smaller!
        self.detr_model_name = "facebook/detr-resnet-50"  # Keep DETR (it's fast)
        
        # Initialize models
        self.blip_processor = None
        self.blip_model = None
        self.detr_processor = None
        self.detr_model = None
        
        # Load models immediately
        self._load_models()
        
        logger.info("Fast Hugging Face Analyzer ready!")
    
    def _load_models(self):
        """Load the small, fast models."""
        try:
            # Load BLIP (small version - downloads in seconds)
            logger.info("Loading BLIP model (small version)...")
            self.blip_processor = BlipProcessor.from_pretrained(self.blip_model_name)
            self.blip_model = BlipForConditionalGeneration.from_pretrained(self.blip_model_name)
            self.blip_model.to(self.device)
            logger.info("✅ BLIP model loaded!")
            
            # Load DETR (fast object detection)
            logger.info("Loading DETR model...")
            self.detr_processor = DetrImageProcessor.from_pretrained(self.detr_model_name)
            self.detr_model = DetrForObjectDetection.from_pretrained(self.detr_model_name)
            self.detr_model.to(self.device)
            logger.info("✅ DETR model loaded!")
            
        except Exception as e:
            logger.error(f"Failed to load models: {e}")
    
    def _preprocess_image(self, image_bytes: bytes) -> Image.Image:
        """Preprocess image for analysis."""
        try:
            image = Image.open(io.BytesIO(image_bytes))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            return image
        except Exception as e:
            logger.error(f"Failed to preprocess image: {e}")
            raise ValueError(f"Invalid image format: {e}")
    
    def _detect_objects(self, image: Image.Image) -> List[Dict]:
        """Detect objects using DETR."""
        try:
            if self.detr_model is None:
                return []
            
            # Process image
            inputs = self.detr_processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Detect objects
            with torch.no_grad():
                outputs = self.detr_model(**inputs)
            
            # Process results
            target_sizes = torch.tensor([image.size[::-1]]).to(self.device)
            results = self.detr_processor.post_process_object_detection(
                outputs, target_sizes=target_sizes, threshold=0.5
            )[0]
            
            detected_objects = []
            for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
                if score > 0.5:
                    object_name = self.detr_model.config.id2label[label.item()]
                    detected_objects.append({
                        "name": object_name,
                        "confidence": score.item()
                    })
            
            return detected_objects
            
        except Exception as e:
            logger.error(f"Object detection failed: {e}")
            return []
    
    def _generate_caption(self, image: Image.Image) -> str:
        """Generate caption using BLIP."""
        try:
            if self.blip_model is None:
                return "An image with various objects."
            
            # Process image
            inputs = self.blip_processor(image, return_tensors="pt").to(self.device)
            
            # Generate caption
            with torch.no_grad():
                generated_ids = self.blip_model.generate(
                    **inputs,
                    max_length=50,
                    num_beams=3,
                    early_stopping=True
                )
            
            caption = self.blip_processor.decode(generated_ids[0], skip_special_tokens=True)
            return caption
            
        except Exception as e:
            logger.error(f"Caption generation failed: {e}")
            return "An image with various objects."
    
    def _analyze_scene(self, detected_objects: List[Dict], caption: str) -> Dict:
        """Analyze the scene context."""
        scene = {
            "people_count": 0,
            "vehicles": [],
            "clothing": [],
            "nature": [],
            "urban": [],
            "setting": "unknown"
        }
        
        # Analyze detected objects
        object_names = [obj["name"].lower() for obj in detected_objects]
        
        # Count people
        people_words = ["person", "man", "woman", "child", "boy", "girl"]
        scene["people_count"] = sum(1 for name in object_names if name in people_words)
        
        # Find vehicles
        vehicle_words = ["car", "truck", "bus", "van", "motorcycle", "bicycle"]
        scene["vehicles"] = [name for name in object_names if name in vehicle_words]
        
        # Find clothing
        clothing_words = ["tie", "backpack", "handbag", "suitcase"]
        scene["clothing"] = [name for name in object_names if name in clothing_words]
        
        # Find nature
        nature_words = ["tree", "plant", "flower", "grass", "bird"]
        scene["nature"] = [name for name in object_names if name in nature_words]
        
        # Find urban
        urban_words = ["building", "house", "street", "road", "window", "door", "bench"]
        scene["urban"] = [name for name in object_names if name in urban_words]
        
        # Determine setting
        if scene["urban"]:
            scene["setting"] = "urban"
        elif scene["nature"]:
            scene["setting"] = "natural"
        elif scene["vehicles"]:
            scene["setting"] = "transportation"
        else:
            scene["setting"] = "general"
        
        return scene
    
    def _determine_emotion(self, scene: Dict, caption: str) -> List[str]:
        """Determine emotions."""
        emotions = []
        caption_lower = caption.lower()
        
        # Look for emotional cues
        if any(word in caption_lower for word in ["smiling", "happy", "laughing"]):
            emotions.append("happy")
        elif any(word in caption_lower for word in ["sitting", "standing", "waiting"]):
            emotions.append("calm")
        else:
            emotions.append("neutral")
        
        # Add context emotions
        if scene["people_count"] > 1:
            emotions.append("social")
        if scene["vehicles"]:
            emotions.append("active")
        if scene["nature"]:
            emotions.append("peaceful")
        
        return emotions[:3]
    
    def _generate_objects_list(self, detected_objects: List[Dict], scene: Dict, caption: str) -> List[str]:
        """Generate comprehensive objects list with caption consistency."""
        objects = []
        
        # Extract objects from caption first (more reliable for scene context)
        caption_objects = self._extract_objects_from_caption(caption)
        objects.extend(caption_objects)
        
        logger.info(f"🔍 Caption objects extracted: {caption_objects}")
        logger.info(f"🔍 Detected objects from AI: {[obj['name'] for obj in detected_objects]}")
        
        # Add people
        if scene["people_count"] > 0:
            objects.append(f"people ({scene['people_count']} visible)")
            for i in range(scene["people_count"]):
                objects.append("person")
        
        # Add vehicles
        objects.extend(scene["vehicles"])
        
        # Add detected objects, but prioritize caption consistency
        filtered_objects = []
        for obj in detected_objects:
            obj_name = obj["name"]
            # Only add detected object if it doesn't contradict caption
            if not self._contradicts_caption(obj_name, caption_objects) and obj_name not in objects:
                objects.append(obj_name)
                filtered_objects.append(obj_name)
            else:
                logger.info(f"🚫 Filtering out contradictory object: {obj_name}")
        
        logger.info(f"✅ Final objects list: {objects}")
        
        # Add scene context
        if scene["nature"]:
            objects.extend(scene["nature"])
        if scene["urban"]:
            objects.extend(scene["urban"])
        
        return objects[:10]
    
    def _extract_objects_from_caption(self, caption: str) -> List[str]:
        """Extract objects mentioned in the caption."""
        # Common animals and objects to look for in captions
        animals = ["rabbit", "turtle", "dog", "cat", "bird", "horse", "giraffe", "elephant", "lion", "tiger", "bear", "deer", "fox", "wolf"]
        objects = ["car", "truck", "tree", "house", "building", "table", "chair", "book", "computer", "phone"]
        
        caption_lower = caption.lower()
        found_objects = []
        
        # Check for animals
        for animal in animals:
            if animal in caption_lower:
                found_objects.append(animal)
        
        # Check for objects
        for obj in objects:
            if obj in caption_lower:
                found_objects.append(obj)
        
        return found_objects
    
    def _contradicts_caption(self, detected_obj: str, caption_objects: List[str]) -> bool:
        """Check if detected object contradicts caption objects."""
        # Simple contradiction check - can be enhanced
        contradictions = {
            "giraffe": ["rabbit", "turtle", "cat", "dog"],
            "horse": ["rabbit", "turtle", "cat"],
            "elephant": ["rabbit", "turtle", "cat", "dog"],
            "lion": ["rabbit", "turtle", "cat", "dog"],
            "tiger": ["rabbit", "turtle", "cat", "dog"]
        }
        
        detected_lower = detected_obj.lower()
        for caption_obj in caption_objects:
            if detected_lower in contradictions.get(caption_obj.lower(), []):
                return True
            if caption_obj.lower() in contradictions.get(detected_lower, []):
                return True
        
        return False
    
    def _generate_summary(self, caption: str, scene: Dict, detected_objects: List[Dict]) -> List[str]:
        """Generate detailed summary."""
        summary = [caption]
        
        # Add people details
        if scene["people_count"] > 0:
            if scene["people_count"] == 1:
                summary.append("There is one person visible in the scene.")
            else:
                summary.append(f"There are {scene['people_count']} people in the scene.")
        
        # Add vehicle details
        if scene["vehicles"]:
            vehicles_str = ", ".join(scene["vehicles"])
            summary.append(f"Vehicles present: {vehicles_str}.")
        
        # Add setting details
        if scene["setting"] == "urban":
            summary.append("The scene appears to be in an urban environment.")
        elif scene["setting"] == "natural":
            summary.append("The scene contains natural elements.")
        
        # Add object details
        if detected_objects:
            object_names = [obj["name"] for obj in detected_objects[:5]]
            summary.append(f"Detected objects: {', '.join(object_names)}.")
        
        return summary[:5]
    
    def _generate_story(self, caption: str, scene: Dict, emotions: List[str], detected_objects: List[Dict] = None) -> List[str]:
        """Generate enhanced creative story."""
        try:
            # Import the enhanced story generator
            from .enhanced_story_generator import enhanced_story_generator
            
            # Generate objects list for story generation
            objects = self._generate_objects_list(detected_objects or [], scene)
            
            # Use enhanced story generator - CREATIVE and FLOWING
            story = enhanced_story_generator.generate_enhanced_story(objects, caption, ", ".join(emotions))
            return story
            
        except Exception as e:
            logger.error(f"Enhanced story generation failed, using fallback: {e}")
            # Fallback to grounded story generation
            try:
                from .grounded_story_generator import grounded_story_generator
                objects = self._generate_objects_list(detected_objects or [], scene)
                story = grounded_story_generator.generate_grounded_story(objects, caption, ", ".join(emotions))
                return story
            except Exception as e2:
                logger.error(f"Grounded story generation also failed: {e2}")
                # Final fallback to original story generation
                story = []
                
                # Start with setting
                if scene["setting"] == "urban":
                    story.append("In the bustling city, life unfolds in countless small moments.")
                elif scene["setting"] == "natural":
                    story.append("Nature provides a beautiful canvas for human stories.")
                else:
                    story.append("Every image captures a moment worth exploring.")
                
                # Add people context
                if scene["people_count"] > 1:
                    story.append("People come together, creating connections that shape our world.")
                elif scene["people_count"] == 1:
                    story.append("A solitary figure stands, representing individual stories within the collective.")
                
                # Add vehicle context
                if scene["vehicles"]:
                    story.append("Vehicles in motion suggest journeys in progress or destinations reached.")
                
                # Add emotional context
                if emotions:
                    emotion_text = ", ".join(emotions)
                    story.append(f"The atmosphere carries a {emotion_text} energy.")
                
                # Concluding thoughts
                story.append("Such moments, frozen in time, speak volumes about the human experience.")
                story.append("Every image tells a story waiting to be discovered.")
                
                return story
    
    def analyze_image(self, image_bytes: bytes) -> Dict:
        """
        Analyze image using fast Hugging Face models.
        
        Args:
            image_bytes: Raw image data as bytes
            
        Returns:
            Dict: Structured analysis
        """
        try:
            logger.info("Starting Fast Hugging Face analysis...")
            
            # Preprocess
            image = self._preprocess_image(image_bytes)
            
            # Detect objects
            logger.info("Detecting objects...")
            detected_objects = self._detect_objects(image)
            
            # Generate caption
            logger.info("Generating caption...")
            caption = self._generate_caption(image)
            
            # Analyze scene
            logger.info("Analyzing scene...")
            scene = self._analyze_scene(detected_objects, caption)
            
            # Determine emotions
            logger.info("Determining emotions...")
            emotions = self._determine_emotion(scene, caption)
            
            # Generate results
            logger.info("Generating final results...")
            summary = self._generate_summary(caption, scene, detected_objects)
            objects = self._generate_objects_list(detected_objects, scene, caption)
            story = self._generate_story(caption, scene, emotions, detected_objects)
            
            logger.info("Fast Hugging Face analysis completed!")
            
            return {
                "caption": caption,
                "summary": summary,
                "objects": objects,
                "emotion": ", ".join(emotions),
                "story": story
            }
            
        except Exception as e:
            logger.error(f"Fast Hugging Face analysis failed: {e}")
            # Fallback to true vision
            from .true_vision_service import true_vision_analyzer
            return true_vision_analyzer.analyze_image(image_bytes)


# Global fast Hugging Face analyzer instance
fast_huggingface_analyzer = FastHuggingFaceAnalyzer()
