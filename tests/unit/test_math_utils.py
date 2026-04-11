"""test_math_utils.py — tests unitaires pour math_utils."""
import pytest

from src.math_utils import add, safe_divide

pytestmark = pytest.mark.unit


class TestAdd:
    def test_integers(self):
        assert add(2, 3) == 5

    def test_floats(self):
        assert add(0.1, 0.2) == pytest.approx(0.3)

    def test_negative(self):
        assert add(-4, 4) == 0

    def test_zero(self):
        assert add(0, 0) == 0


class TestSafeDivide:
    def test_normal(self):
        assert safe_divide(10, 2) == 5.0

    def test_float_result(self):
        assert safe_divide(1, 3) == pytest.approx(0.3333, rel=1e-3)

    def test_negative_divisor(self):
        assert safe_divide(-9, 3) == -3.0

    def test_zero_divisor_raises(self):
        with pytest.raises(ValueError, match="Division par zéro interdite."):
            safe_divide(5, 0)

    def test_zero_dividend(self):
        assert safe_divide(0, 5) == 0.0
