import pytest
from app.moderation import moderate_content

def test_moderation_short_content():
    """Test that content shorter than 50 characters is flagged"""
    content = "This is too short"
    status, reasons = moderate_content(content)
    assert status == "flagged"
    assert "too short" in reasons

def test_moderation_long_content():
    """Test that content longer than 2000 characters is flagged"""
    content = "a" * 2001
    status, reasons = moderate_content(content)
    assert status == "flagged"
    assert "too long" in reasons

def test_moderation_banned_words():
    """Test that content with banned words is flagged"""
    content = "This text contains profanity which should be flagged"
    status, reasons = moderate_content(content)
    assert status == "flagged"
    assert "banned words detected" in reasons

def test_moderation_aggressive_tone():
    """Test that content with aggressive tone is flagged"""
    content = "THIS IS ALL CAPS AND SHOULD BE FLAGGED!!!"
    status, reasons = moderate_content(content)
    assert status == "flagged"
    assert "aggressive tone" in reasons

def test_moderation_multiple_issues():
    """Test that content with multiple issues has multiple reasons"""
    content = "DAMN!!!"  # Short, aggressive, and contains banned word
    status, reasons = moderate_content(content)
    assert status == "flagged"
    assert len(reasons) > 1

def test_moderation_valid_content():
    """Test that valid content is approved"""
    content = "This is a perfectly normal blog post that is long enough to pass the minimum length requirement and does not contain any banned words or aggressive tone."
    status, reasons = moderate_content(content)
    assert status == "approved"
    assert not reasons 