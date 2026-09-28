# quality/validator.py
# Q09 Feature 1 – Strict Validation (Poka-Yoke)
# Central validation library used across all modules.

import re


class ValidationError(Exception):
    """Raised when input fails validation."""
    pass


# ─── Primitive validators ────────────────────────────────────────────────────

def require_non_empty(value: str, field_name: str) -> str:
    """Ensure a string field is not blank."""
    if not value or not str(value).strip():
        raise ValidationError(f"❌ {field_name} is required and cannot be empty.")
    return str(value).strip()


def require_positive_float(value, field_name: str) -> float:
    """Ensure a value is a positive float."""
    try:
        num = float(value)
    except (ValueError, TypeError):
        raise ValidationError(f"❌ {field_name} must be a valid number.")
    if num <= 0:
        raise ValidationError(f"❌ {field_name} must be greater than 0.")
    return num


def require_positive_int(value, field_name: str) -> int:
    """Ensure a value is a positive integer."""
    try:
        num = int(value)
    except (ValueError, TypeError):
        raise ValidationError(f"❌ {field_name} must be a valid whole number.")
    if num <= 0:
        raise ValidationError(f"❌ {field_name} must be greater than 0.")
    return num


def validate_phone(phone: str) -> str:
    """Validate an Indian-style 10-digit phone number (optional field)."""
    phone = phone.strip()
    if phone == "":
        return phone  # Optional field
    pattern = r"^[6-9]\d{9}$"
    if not re.fullmatch(pattern, phone):
        raise ValidationError(
            "❌ Enter a valid 10-digit phone number starting with 6–9."
        )
    return phone


def validate_email(email: str) -> str:
    """Validate email format (optional field)."""
    email = email.strip()
    if email == "":
        return email  # Optional field
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if not re.fullmatch(pattern, email):
        raise ValidationError("❌ Enter a valid email address.")
    return email


# ─── Domain-level validators ─────────────────────────────────────────────────

def validate_menu_item(name: str, category: str, price) -> dict:
    """Validate menu item fields and return cleaned dict."""
    return {
        "name":     require_non_empty(name, "Item Name"),
        "category": require_non_empty(category, "Category"),
        "price":    require_positive_float(price, "Price"),
    }


def validate_customer(name: str, phone: str, email: str) -> dict:
    """Validate customer fields and return cleaned dict."""
    return {
        "name":  require_non_empty(name, "Customer Name"),
        "phone": validate_phone(phone),
        "email": validate_email(email),
    }


def validate_order_item(menu_item_id, quantity) -> dict:
    """Validate an order line — item must be selected and quantity positive."""
    if not menu_item_id:
        raise ValidationError("❌ Please select a menu item.")
    qty = require_positive_int(quantity, "Quantity")
    return {"menu_item_id": menu_item_id, "quantity": qty}


def validate_login(username: str, password: str) -> dict:
    """Validate login credentials (non-empty check only)."""
    return {
        "username": require_non_empty(username, "Username"),
        "password": require_non_empty(password, "Password"),
    }
