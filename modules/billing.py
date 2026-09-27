# modules/billing.py  – Billing & Bill Generation
from database.db import get_connection
from modules.orders import get_order_items, close_order
from quality.error_logger import log_error, log_info
from quality.validator import ValidationError

GST_RATE = 5.0  # percent


def calculate_bill(order_id: int) -> tuple[bool, dict | str]:
    """
    Calculate subtotal, GST, and total for an order.
    Returns (True, bill_dict) or (False, error_message).
    """
    items = get_order_items(order_id)
    if not items:
        return False, "❌ Cannot generate bill for an empty order."

    subtotal = sum(item["line_total"] for item in items)
    if subtotal <= 0:
        return False, "❌ Order total must be greater than ₹0."

    gst_amount = round(subtotal * GST_RATE / 100, 2)
    total = round(subtotal + gst_amount, 2)

    return True, {
        "order_id": order_id,
        "items": items,
        "subtotal": subtotal,
        "gst_rate": GST_RATE,
        "gst_amount": gst_amount,
        "total": total,
    }


def save_bill(order_id: int) -> tuple[bool, str]:
    """
    Persist the calculated bill in the bills table and close the order.
    Idempotent — if a bill already exists, returns it.
    """
    ok, result = calculate_bill(order_id)
    if not ok:
        return False, result

    try:
        conn = get_connection()
        # Upsert the bill
        conn.execute(
            """INSERT INTO bills (order_id, subtotal, gst_rate, gst_amount, total)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(order_id) DO UPDATE SET
                   subtotal=excluded.subtotal,
                   gst_amount=excluded.gst_amount,
                   total=excluded.total""",
            (
                order_id,
                result["subtotal"],
                result["gst_rate"],
                result["gst_amount"],
                result["total"],
            ),
        )
        conn.commit()
        conn.close()
        close_order(order_id)
        log_info("Billing", f"Bill saved for order id={order_id}, total=₹{result['total']}")
        return True, "✅ Bill generated successfully."
    except Exception as e:
        log_error("Billing", "Failed to save bill", str(e))
        return False, "⚠️ Unable to generate bill. Please try again."


def get_bill(order_id: int) -> dict | None:
    """Retrieve a saved bill with its items."""
    try:
        conn = get_connection()
        bill = conn.execute(
            "SELECT * FROM bills WHERE order_id=?", (order_id,)
        ).fetchone()
        conn.close()
        if not bill:
            return None
        bill_dict = dict(bill)
        bill_dict["items"] = get_order_items(order_id)
        return bill_dict
    except Exception as e:
        log_error("Billing", "Failed to fetch bill", str(e))
        return None


def get_dashboard_stats() -> dict:
    """Return aggregated stats for the dashboard."""
    try:
        conn = get_connection()
        today_revenue = conn.execute(
            "SELECT COALESCE(SUM(total),0) FROM bills WHERE DATE(created_at)=DATE('now')"
        ).fetchone()[0]
        total_orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        items_sold = conn.execute(
            "SELECT COALESCE(SUM(quantity),0) FROM order_items"
        ).fetchone()[0]
        pending = conn.execute(
            "SELECT COUNT(*) FROM orders WHERE status='open'"
        ).fetchone()[0]
        conn.close()
        return {
            "today_revenue": today_revenue,
            "total_orders": total_orders,
            "items_sold": items_sold,
            "pending_orders": pending,
        }
    except Exception as e:
        log_error("Billing", "Failed to get dashboard stats", str(e))
        return {"today_revenue": 0, "total_orders": 0, "items_sold": 0, "pending_orders": 0}


def format_bill_text(bill: dict, restaurant_name: str = "SPICE GARDEN RESTAURANT") -> str:
    """Return a formatted bill string for display/printing."""
    lines = []
    sep = "─" * 48
    lines.append(sep)
    lines.append(f"{'🍽  ' + restaurant_name:^48}")
    lines.append(f"{'Order #' + str(bill['order_id']):^48}")
    lines.append(sep)
    lines.append(f"{'Item':<22} {'Qty':>4} {'Price':>10} {'Total':>10}")
    lines.append(sep)
    for item in bill["items"]:
        lines.append(
            f"{item['name']:<22} {item['quantity']:>4} {item['unit_price']:>9.2f} {item['line_total']:>9.2f}"
        )
    lines.append(sep)
    lines.append(f"{'Subtotal':>37}  ₹{bill['subtotal']:>8.2f}")
    lines.append(f"{'GST (' + str(bill['gst_rate']) + '%)':>37}  ₹{bill['gst_amount']:>8.2f}")
    lines.append(sep)
    lines.append(f"{'TOTAL':>37}  ₹{bill['total']:>8.2f}")
    lines.append(sep)
    lines.append(f"{'Thank you! Visit again 😊':^48}")
    lines.append(sep)
    return "\n".join(lines)