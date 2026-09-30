# tests/test_validation.py
# Q09 Feature 3 – Module Tests: Validation Layer
# Run: pytest tests/ -v

import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from quality.validator import (
    ValidationError,
    require_non_empty,
    require_positive_float,
    require_positive_int,
    validate_phone,
    validate_email,
    validate_menu_item,
    validate_customer,
    validate_order_item,
    validate_login,
)


# ── require_non_empty ──────────────────────────────────────────────────────────

class TestRequireNonEmpty:
    def test_valid_string(self):
        assert require_non_empty("Paneer Tikka", "Item") == "Paneer Tikka"

    def test_strips_whitespace(self):
        assert require_non_empty("  Burger  ", "Item") == "Burger"

    def test_empty_string_raises(self):
        with pytest.raises(ValidationError):
            require_non_empty("", "Item")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValidationError):
            require_non_empty("   ", "Item")

    def test_none_raises(self):
        with pytest.raises(ValidationError):
            require_non_empty(None, "Item")


# ── require_positive_float ─────────────────────────────────────────────────────

class TestRequirePositiveFloat:
    def test_valid_price(self):
        assert require_positive_float(180, "Price") == 180.0

    def test_valid_string_number(self):
        assert require_positive_float("99.5", "Price") == 99.5

    def test_zero_raises(self):
        with pytest.raises(ValidationError, match="greater than 0"):
            require_positive_float(0, "Price")

    def test_negative_raises(self):
        with pytest.raises(ValidationError):
            require_positive_float(-100, "Price")

    def test_string_text_raises(self):
        with pytest.raises(ValidationError, match="valid number"):
            require_positive_float("abc", "Price")

    def test_none_raises(self):
        with pytest.raises(ValidationError):
            require_positive_float(None, "Price")


# ── require_positive_int ───────────────────────────────────────────────────────

class TestRequirePositiveInt:
    def test_valid_quantity(self):
        assert require_positive_int(3, "Quantity") == 3

    def test_valid_string_int(self):
        assert require_positive_int("5", "Quantity") == 5

    def test_zero_raises(self):
        with pytest.raises(ValidationError):
            require_positive_int(0, "Quantity")

    def test_negative_raises(self):
        with pytest.raises(ValidationError):
            require_positive_int(-5, "Quantity")

    def test_float_string_raises(self):
        with pytest.raises(ValidationError):
            require_positive_int("2.5", "Quantity")

    def test_text_raises(self):
        with pytest.raises(ValidationError):
            require_positive_int("five", "Quantity")


# ── validate_phone ─────────────────────────────────────────────────────────────

