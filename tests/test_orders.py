# tests/test_orders.py
# Q09 Feature 3 – Module Tests: Order Module

import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modules.orders import (
    create_order, add_order_item, remove_order_item,
    get_order_items, get_all_orders, delete_order
)
# DB isolation handled by tests/conftest.py


class TestCreateOrder:
    def test_create_order_returns_id(self):
        ok, order_id = create_order()
        assert ok
        assert isinstance(order_id, int)
        assert order_id > 0

    def test_create_order_with_customer(self):
        ok, order_id = create_order(customer_id=None)
        assert ok


class TestAddOrderItem:
    def test_add_valid_item(self):
        _, order_id = create_order()
        ok, msg = add_order_item(order_id, 1, 2, 180.0)
        assert ok
        assert "✅" in msg

    def test_add_zero_quantity_fails(self):
        _, order_id = create_order()
        ok, msg = add_order_item(order_id, 1, 0, 180.0)
        assert not ok
        assert "❌" in msg

    def test_add_negative_quantity_fails(self):
        _, order_id = create_order()
        ok, msg = add_order_item(order_id, 1, -3, 180.0)
        assert not ok

    def test_add_no_menu_item_fails(self):
        _, order_id = create_order()
        ok, msg = add_order_item(order_id, None, 2, 180.0)
        assert not ok

    def test_duplicate_item_merges_quantity(self):
        _, order_id = create_order()
        add_order_item(order_id, 1, 2, 180.0)
        add_order_item(order_id, 1, 3, 180.0)
        items = get_order_items(order_id)
        item = next(i for i in items if i["menu_item_id"] == 1)
        assert item["quantity"] == 5  # merged


class TestGetOrderItems:
    def test_empty_order_returns_empty_list(self):
        _, order_id = create_order()
        items = get_order_items(order_id)
        assert items == []

    def test_items_have_line_total(self):
        _, order_id = create_order()
        add_order_item(order_id, 1, 3, 100.0)
        items = get_order_items(order_id)
        assert items[0]["line_total"] == 300.0

    def test_multiple_items(self):
        _, order_id = create_order()
        add_order_item(order_id, 1, 2, 180.0)
        add_order_item(order_id, 2, 1, 120.0)
        items = get_order_items(order_id)
        assert len(items) == 2


class TestRemoveOrderItem:
    def test_remove_item(self):
        _, order_id = create_order()
        add_order_item(order_id, 1, 2, 180.0)
        items = get_order_items(order_id)
        oi_id = items[0]["id"]
        ok, msg = remove_order_item(oi_id)
        assert ok
        assert get_order_items(order_id) == []


class TestDeleteOrder:
    def test_delete_order(self):
        _, order_id = create_order()
        add_order_item(order_id, 1, 1, 100.0)
        ok, _ = delete_order(order_id)
        assert ok
        items = get_order_items(order_id)
        assert items == []
