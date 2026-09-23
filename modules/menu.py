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


def update_menu_item(item_id: int, name: str, category: str, price, available: int = 1) -> tuple[bool, str]:
    """Update an existing menu item."""
    try:
        data = validate_menu_item(name, category, price)
    except ValidationError as ve:
        return False, str(ve)
    try:
        conn = get_connection()
        conn.execute(
            "UPDATE menu_items SET name=?, category=?, price=?, available=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (data["name"], data["category"], data["price"], available, item_id),
        )
        conn.commit()
        conn.close()
        log_info("Menu", f"Updated item id={item_id}")
        return True, "✅ Item updated successfully."
    except Exception as e:
        log_error("Menu", "Failed to update menu item", str(e))
        return False, "⚠️ Unable to update item."


def delete_menu_item(item_id: int) -> tuple[bool, str]:
    """Delete a menu item by ID."""
    try:
        conn = get_connection()
        conn.execute("DELETE FROM menu_items WHERE id=?", (item_id,))
        conn.commit()
        conn.close()
        log_info("Menu", f"Deleted item id={item_id}")
        return True, "✅ Item deleted."
    except Exception as e:
        log_error("Menu", "Failed to delete menu item", str(e))
        return False, "⚠️ Unable to delete item."


def get_categories() -> list[str]:
    """Return distinct categories for dropdowns."""
    try:
        conn = get_connection()
        rows = conn.execute("SELECT DISTINCT category FROM menu_items ORDER BY category").fetchall()
        conn.close()
        return [r["category"] for r in rows]
    except Exception as e:
        log_error("Menu", "Failed to fetch categories", str(e))
        return []