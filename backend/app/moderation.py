import os
import json
from typing import Tuple, List
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# Configure Gemini AI
api_key = os.environ.get('GEMINI_API_KEY')
if api_key:
    genai.configure(api_key=api_key)

# Constants
MIN_CONTENT_LENGTH = 50
MAX_CONTENT_LENGTH = 2000

def get_banned_words():
    """Load banned words from file"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        banned_words_path = os.path.join(os.path.dirname(script_dir), "banned_words.txt")
        
        with open(banned_words_path, "r") as file:
            return [line.strip().lower() for line in file if line.strip()]
    except Exception as e:
        print(f"Error loading banned words: {e}")
        return ["profanity", "offensive", "obscene"]  # Fallback

async def check_tone_with_gemini(content: str) -> Tuple[bool, str]:
    """
    Use Gemini AI to check if content has an aggressive tone
    
    Returns:
        Tuple[bool, str]: (is_aggressive, explanation)
    """
    try:
        if not api_key:
            # Fallback to basic rules if no API key
            return is_aggressive_tone(content), "Aggressive tone detected (basic rules)"
            
        # Configure the model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Prompt
        prompt = f"""
        Analyze the following text and determine if it has an aggressive tone. 
        Consider factors like word choice, punctuation, and overall sentiment.
        
        Text to analyze:
        "{content}"
        
        Respond with:
        1. A clear YES or NO if the text is aggressive
        2. A brief explanation of why
        
        Format: YES/NO|Explanation
        """
        
        # Generate response
        response = await model.generate_content_async(prompt)
        result = response.text.strip()
        
        # Parse the result
        parts = result.split('|', 1)
        if len(parts) < 2:
            # If format doesn't match, check basic rule as fallback
            return is_aggressive_tone(content), "Unable to parse AI response, using basic rules"
        
        is_aggressive = parts[0].strip().upper() == "YES"
        explanation = parts[1].strip() if len(parts) > 1 else "No explanation provided"
        
        return is_aggressive, explanation
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        # Fallback to basic rules
        return is_aggressive_tone(content), f"Error using AI service: {str(e)[:100]}..."

def is_aggressive_tone(content: str) -> bool:
    """Check if content has an aggressive tone using basic rules"""
    # Simple check for all caps (shouting)
    if content.isupper() and len(content) > 5:
        return True
    
    # Check for excessive exclamation marks
    if re.search(r'!{3,}', content):
        return True
    
    return False

async def moderate_content(content: str) -> Tuple[str, List[str]]:
    """
    Moderate content and return status and reasons if flagged
    
    Returns:
        Tuple[str, List[str]]: ("approved", []) or ("flagged", ["reason1", "reason2"])
    """
    reasons = []
    
    # Check content length
    if len(content) < MIN_CONTENT_LENGTH:
        reasons.append("too short")
    if len(content) > MAX_CONTENT_LENGTH:
        reasons.append("too long")
    
    # Check for banned words
    banned_words = get_banned_words()
    content_lower = content.lower()
    found_banned_words = [word for word in banned_words if word in content_lower]
    if found_banned_words:
        reasons.append("banned words detected")
    
    # Check tone
    if api_key:
        # Use Gemini AI for tone detection if API key is available
        is_aggressive, explanation = await check_tone_with_gemini(content)
        if is_aggressive:
            reasons.append(f"aggressive tone: {explanation}")
    else:
        # Fallback to basic rules
        if is_aggressive_tone(content):
            reasons.append("aggressive tone")
    
    # Return result
    if reasons:
        return "flagged", reasons
    else:
        return "approved", [] 