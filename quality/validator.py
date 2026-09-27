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


