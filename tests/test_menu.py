# tests/test_menu.py
# Q09 Feature 3 – Module Tests: Menu Module

import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modules.menu import add_menu_item, get_all_menu_items, update_menu_item, delete_menu_item
# DB isolation handled by tests/conftest.py


class TestAddMenuItem:
    def test_add_valid_item(self):
        ok, msg = add_menu_item("Samosa", "Starter", 30)
        assert ok
        assert "✅" in msg

    def test_add_negative_price_fails(self):
        ok, msg = add_menu_item("Samosa", "Starter", -30)
        assert not ok
        assert "❌" in msg

    def test_add_zero_price_fails(self):
        ok, msg = add_menu_item("Samosa", "Starter", 0)
        assert not ok

    def test_add_empty_name_fails(self):
        ok, msg = add_menu_item("", "Starter", 50)
        assert not ok
        assert "❌" in msg

    def test_add_empty_category_fails(self):
        ok, msg = add_menu_item("Samosa", "", 50)
        assert not ok

    def test_add_text_price_fails(self):
        ok, msg = add_menu_item("Samosa", "Starter", "free")
        assert not ok


class TestGetMenuItems:
    def test_returns_list(self):
        items = get_all_menu_items()
        assert isinstance(items, list)

    def test_seeded_items_exist(self):
        items = get_all_menu_items()
        assert len(items) > 0

    def test_item_has_required_fields(self):
        items = get_all_menu_items()
        item = items[0]
        assert "id" in item
        assert "name" in item
        assert "price" in item
        assert "category" in item


