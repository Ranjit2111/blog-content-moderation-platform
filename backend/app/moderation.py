import os
import json
from typing import Tuple, List
import re

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

def is_aggressive_tone(content: str) -> bool:
    """Check if content has an aggressive tone"""
    # Simple check for all caps (shouting)
    if content.isupper() and len(content) > 5:
        return True
    
    # Check for excessive exclamation marks
    if re.search(r'!{3,}', content):
        return True
    
    return False

def moderate_content(content: str) -> Tuple[str, List[str]]:
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
    if is_aggressive_tone(content):
        reasons.append("aggressive tone")
    
    # Return result
    if reasons:
        return "flagged", reasons
    else:
        return "approved", [] 