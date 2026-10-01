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

class TestValidatePhone:
    def test_valid_phone(self):
        assert validate_phone("9876543210") == "9876543210"

    def test_empty_phone_allowed(self):
        assert validate_phone("") == ""

    def test_short_phone_raises(self):
        with pytest.raises(ValidationError):
            validate_phone("98765")

    def test_starts_with_wrong_digit(self):
        with pytest.raises(ValidationError):
            validate_phone("1234567890")

    def test_alpha_in_phone_raises(self):
        with pytest.raises(ValidationError):
            validate_phone("abc1234567")

    def test_11_digits_raises(self):
        with pytest.raises(ValidationError):
            validate_phone("98765432100")


# ── validate_email ─────────────────────────────────────────────────────────────

class TestValidateEmail:
    def test_valid_email(self):
        assert validate_email("user@example.com") == "user@example.com"

    def test_empty_email_allowed(self):
        assert validate_email("") == ""

    def test_missing_at_raises(self):
        with pytest.raises(ValidationError):
            validate_email("userexample.com")

    def test_missing_domain_raises(self):
        with pytest.raises(ValidationError):
            validate_email("user@")


# ── validate_menu_item ─────────────────────────────────────────────────────────

class TestValidateMenuItem:
    def test_valid_item(self):
        result = validate_menu_item("Paneer Tikka", "Starter", 180)
        assert result["name"] == "Paneer Tikka"
        assert result["price"] == 180.0

    def test_empty_name_raises(self):
        with pytest.raises(ValidationError):
            validate_menu_item("", "Starter", 180)

    def test_negative_price_raises(self):
        with pytest.raises(ValidationError):
            validate_menu_item("Burger", "Fast Food", -50)

    def test_zero_price_raises(self):
        with pytest.raises(ValidationError):
            validate_menu_item("Burger", "Fast Food", 0)

    def test_empty_category_raises(self):
        with pytest.raises(ValidationError):
            validate_menu_item("Burger", "", 120)


# ── validate_customer ──────────────────────────────────────────────────────────

class TestValidateCustomer:
    def test_valid_customer(self):
        result = validate_customer("Rahul Sharma", "9876543210", "rahul@example.com")
        assert result["name"] == "Rahul Sharma"

    def test_empty_name_raises(self):
        with pytest.raises(ValidationError):
            validate_customer("", "9876543210", "")

    def test_invalid_phone_raises(self):
        with pytest.raises(ValidationError):
            validate_customer("Rahul", "abc123", "")

    def test_invalid_email_raises(self):
        with pytest.raises(ValidationError):
            validate_customer("Rahul", "", "notanemail")

    def test_optional_fields_empty_ok(self):
        result = validate_customer("Meera", "", "")
        assert result["name"] == "Meera"
        assert result["phone"] == ""
        assert result["email"] == ""


# ── validate_order_item ────────────────────────────────────────────────────────

class TestValidateOrderItem:
    def test_valid_order_item(self):
        result = validate_order_item(1, 2)
        assert result["quantity"] == 2

    def test_no_menu_item_raises(self):
        with pytest.raises(ValidationError):
            validate_order_item(None, 2)

    def test_zero_quantity_raises(self):
        with pytest.raises(ValidationError):
            validate_order_item(1, 0)

    def test_negative_quantity_raises(self):
        with pytest.raises(ValidationError):
            validate_order_item(1, -3)


# ── validate_login ─────────────────────────────────────────────────────────────

class TestValidateLogin:
    def test_valid_login(self):
        result = validate_login("admin", "admin123")
        assert result["username"] == "admin"

    def test_empty_username_raises(self):
        with pytest.raises(ValidationError):
            validate_login("", "admin123")

    def test_empty_password_raises(self):
        with pytest.raises(ValidationError):
            validate_login("admin", "")
