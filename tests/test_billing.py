# tests/test_billing.py
# Q09 Feature 3 – Module Tests: Billing Module

import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modules.billing import calculate_bill, save_bill, format_bill_text, GST_RATE
from modules.orders import create_order, add_order_item
# DB isolation handled by tests/conftest.py


# ── GST Calculation ────────────────────────────────────────────────────────────

class TestGSTCalculation:
    def test_gst_rate_is_five_percent(self):
        assert GST_RATE == 5.0

    def test_gst_amount_correct(self):
        """Manually verify GST on a known subtotal."""
        subtotal = 200.0
        expected_gst = round(subtotal * 5 / 100, 2)
        assert expected_gst == 10.0

    def test_total_equals_subtotal_plus_gst(self):
        subtotal = 580.0
        gst = round(subtotal * GST_RATE / 100, 2)
        total = round(subtotal + gst, 2)
        assert total == subtotal + gst


# ── Empty Order ────────────────────────────────────────────────────────────────

class TestEmptyOrderBilling:
    def test_empty_order_fails(self):
        ok, order_id = create_order()
        assert ok
        success, msg = calculate_bill(order_id)
        assert not success
        assert "empty" in msg.lower() or "❌" in msg

    def test_save_bill_empty_order_fails(self):
        ok, order_id = create_order()
        assert ok
        success, msg = save_bill(order_id)
        assert not success


# ── Valid Order Billing ────────────────────────────────────────────────────────

class TestValidBilling:
    def test_calculate_bill_with_items(self):
        ok, order_id = create_order()
        assert ok
        add_ok, _ = add_order_item(order_id, 1, 2, 180.0)  # 2x Paneer Tikka ₹360
        assert add_ok
        add_ok2, _ = add_order_item(order_id, 3, 1, 100.0)  # 1x Masala Dosa ₹100
        assert add_ok2

        success, bill = calculate_bill(order_id)
        assert success
        assert bill["subtotal"] == 460.0
        assert bill["gst_amount"] == 23.0
        assert bill["total"] == 483.0

    def test_save_bill_persists(self):
        ok, order_id = create_order()
        assert ok
        add_order_item(order_id, 1, 1, 180.0)
        success, msg = save_bill(order_id)
        assert success
        assert "✅" in msg

    def test_bill_total_is_correct(self):
        ok, order_id = create_order()
        assert ok
        add_order_item(order_id, 2, 2, 120.0)  # 240
        add_order_item(order_id, 4, 3, 40.0)   # 120
        _, bill = calculate_bill(order_id)
        expected_sub = 240 + 120
        assert bill["subtotal"] == expected_sub
        assert bill["total"] == round(expected_sub * 1.05, 2)


# ── Bill Formatting ────────────────────────────────────────────────────────────

class TestBillFormatting:
    def _make_bill(self):
        ok, order_id = create_order()
        add_order_item(order_id, 1, 1, 180.0)
        _, bill = calculate_bill(order_id)
        return bill

    def test_format_contains_total(self):
        bill = self._make_bill()
        text = format_bill_text(bill)
        assert "TOTAL" in text

    def test_format_contains_gst(self):
        bill = self._make_bill()
        text = format_bill_text(bill)
        assert "GST" in text

    def test_format_contains_restaurant_name(self):
        bill = self._make_bill()
        text = format_bill_text(bill, "TEST RESTAURANT")
        assert "TEST RESTAURANT" in text
