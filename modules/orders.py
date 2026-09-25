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


