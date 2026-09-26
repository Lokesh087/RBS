# modules/orders.py  – Order Management
from database.db import get_connection
from quality.validator import validate_order_item, ValidationError
from quality.error_logger import log_error, log_info


def create_order(customer_id=None) -> tuple[bool, str | int]:
    """Create an empty order shell and return its ID."""
    try:
        conn = get_connection()
        cur = conn.execute(
            "INSERT INTO orders (customer_id, status) VALUES (?, 'open')", (customer_id,)
        )
        order_id = cur.lastrowid
        conn.commit()
        conn.close()
        log_info("Order", f"Created order id={order_id}")
        return True, order_id
    except Exception as e:
        log_error("Order", "Failed to create order", str(e))
        return False, "⚠️ Unable to create order."


def add_order_item(order_id: int, menu_item_id: int, quantity, unit_price: float) -> tuple[bool, str]:
    """Add a line item to an existing order."""
    try:
        data = validate_order_item(menu_item_id, quantity)
    except ValidationError as ve:
        return False, str(ve)
    try:
        conn = get_connection()
        # Check if item already exists in order — update quantity instead
        existing = conn.execute(
            "SELECT id, quantity FROM order_items WHERE order_id=? AND menu_item_id=?",
            (order_id, data["menu_item_id"]),
        ).fetchone()
        if existing:
            new_qty = existing["quantity"] + data["quantity"]
            conn.execute(
                "UPDATE order_items SET quantity=? WHERE id=?",
                (new_qty, existing["id"]),
            )
        else:
            conn.execute(
                "INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price) VALUES (?,?,?,?)",
                (order_id, data["menu_item_id"], data["quantity"], unit_price),
            )
        conn.commit()
        conn.close()
        return True, "✅ Item added to order."
    except Exception as e:
        log_error("Order", "Failed to add order item", str(e))
        return False, "⚠️ Unable to add item."


def remove_order_item(order_item_id: int) -> tuple[bool, str]:
    try:
        conn = get_connection()
        conn.execute("DELETE FROM order_items WHERE id=?", (order_item_id,))
        conn.commit()
        conn.close()
        return True, "✅ Item removed."
    except Exception as e:
        log_error("Order", "Failed to remove order item", str(e))
        return False, "⚠️ Unable to remove item."


