# modules/menu.py  – Menu Management CRUD
from database.db import get_connection
from quality.validator import validate_menu_item, ValidationError
from quality.error_logger import log_error, log_info


def add_menu_item(name: str, category: str, price) -> tuple[bool, str]:
    """Add a new menu item after strict validation."""
    try:
        data = validate_menu_item(name, category, price)
    except ValidationError as ve:
        return False, str(ve)
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO menu_items (name, category, price) VALUES (?, ?, ?)",
            (data["name"], data["category"], data["price"]),
        )
        conn.commit()
        conn.close()
        log_info("Menu", f"Added item: {data['name']}")
        return True, f"✅ '{data['name']}' added successfully."
    except Exception as e:
        log_error("Menu", "Failed to add menu item", str(e))
        return False, "⚠️ Unable to save item. Please try again."


def get_all_menu_items(available_only: bool = False) -> list[dict]:
    """Fetch all (or only available) menu items."""
    try:
        conn = get_connection()
        query = "SELECT * FROM menu_items"
        if available_only:
            query += " WHERE available = 1"
        query += " ORDER BY category, name"
        rows = conn.execute(query).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        log_error("Menu", "Failed to fetch menu items", str(e))
        return []


