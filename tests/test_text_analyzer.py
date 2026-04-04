import pytest
import sys
import os

# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from text_analyzer import analyze_text

def test_analyze_text_normal():
    # 3 sentences, 8 words
    text = "Hello world. How are you? I am fine!"
    result = analyze_text(text)
    assert result["word_count"] == 8
    assert result["sentence_count"] == 3
    assert result["readability_ratio"] == 8 / 3

def test_analyze_text_empty_and_none():
    with pytest.raises(ValueError):
        analyze_text("")
    with pytest.raises(ValueError):
        analyze_text(None)
    with pytest.raises(ValueError):
        analyze_text("   ")

def test_analyze_text_no_punctuation():
    # 1 sentence, 6 words, no punctuation
    text = "this is a test without punctuation"
    result = analyze_text(text)
    assert result["word_count"] == 6
    assert result["sentence_count"] == 1
    assert result["readability_ratio"] == 6.0
