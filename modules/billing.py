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


