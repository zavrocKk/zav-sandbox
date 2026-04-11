"""math_utils.py — fonctions mathématiques sécurisées."""

import logging

logger = logging.getLogger(__name__)


def add(a: float, b: float) -> float:
    """Retourne la somme de a et b."""
    result = a + b
    logger.debug("add(%s, %s) = %s", a, b, result)
    return result


def safe_divide(a: float, b: float) -> float:
    """Retourne a / b. Lève ValueError si b == 0."""
    if b == 0:
        logger.warning("Division par zéro tentée: safe_divide(%s, 0)", a)
        raise ValueError("Division par zéro interdite.")
    result = a / b
    logger.debug("safe_divide(%s, %s) = %s", a, b, result)
    return result
