"""math_utils.py — fonctions mathématiques sécurisées."""


def add(a: float, b: float) -> float:
    """Retourne la somme de a et b."""
    return a + b


def safe_divide(a: float, b: float) -> float:
    """Retourne a / b. Lève ValueError si b == 0."""
    if b == 0:
        raise ValueError("Division par zéro interdite.")
    return a / b
