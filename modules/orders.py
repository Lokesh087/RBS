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


def get_order_items(order_id: int) -> list[dict]:
    """Return all items for an order with menu item details."""
    try:
        conn = get_connection()
        rows = conn.execute(
            """SELECT oi.id, oi.menu_item_id, m.name, oi.quantity, oi.unit_price,
                      (oi.quantity * oi.unit_price) AS line_total
               FROM order_items oi
               JOIN menu_items m ON m.id = oi.menu_item_id
               WHERE oi.order_id = ?""",
            (order_id,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        log_error("Order", "Failed to fetch order items", str(e))
        return []


def get_all_orders() -> list[dict]:
    """Return all orders with customer name and bill total."""
    try:
        conn = get_connection()
        rows = conn.execute(
            """SELECT o.id, o.status, o.created_at,
                      COALESCE(c.name, 'Walk-in') AS customer_name,
                      COALESCE(b.total, 0) AS total
               FROM orders o
               LEFT JOIN customers c ON c.id = o.customer_id
               LEFT JOIN bills b ON b.order_id = o.id
               ORDER BY o.created_at DESC"""
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        log_error("Order", "Failed to fetch orders", str(e))
        return []


def close_order(order_id: int) -> tuple[bool, str]:
    """Mark order as 'closed' after billing."""
    try:
        conn = get_connection()
        conn.execute("UPDATE orders SET status='closed' WHERE id=?", (order_id,))
        conn.commit()
        conn.close()
        return True, "Order closed."
    except Exception as e:
        log_error("Order", "Failed to close order", str(e))
        return False, "⚠️ Unable to close order."


def delete_order(order_id: int) -> tuple[bool, str]:
    """Delete an open order and its items."""
    try:
        conn = get_connection()
        conn.execute("DELETE FROM order_items WHERE order_id=?", (order_id,))
        conn.execute("DELETE FROM orders WHERE id=?", (order_id,))
        conn.commit()
        conn.close()
        return True, "✅ Order deleted."
    except Exception as e:
        log_error("Order", "Failed to delete order", str(e))
        return False, "⚠️ Unable to delete order."
