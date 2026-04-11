import logging
import re

logger = logging.getLogger(__name__)


def analyze_text(text: str) -> dict:
    if not text or not text.strip():
        raise ValueError("Text cannot be empty or None")

    words = text.split()
    word_count = len(words)

    # Count sentences based on delimiters
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    sentence_count = len(sentences)

    # Edge case: text without final punctuation
    if sentence_count == 0 and word_count > 0:
        sentence_count = 1

    readability_ratio = word_count / sentence_count if sentence_count > 0 else 0.0

    result = {"word_count": word_count, "sentence_count": sentence_count, "readability_ratio": readability_ratio}
    logger.debug("analyze_text: %s", result)
    return result
