# tests/conftest.py
# Shared pytest configuration — uses a temp file DB for isolation

import sys
import os
import pytest
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import database.db as _db_module


@pytest.fixture(autouse=True, scope="function")
def isolate_db(tmp_path):
    """
    Each test function gets its own fresh SQLite database file.
    Uses tmp_path (pytest temp dir) so tests never share state.
    Prevents test pollution across modules.
    """
    original = _db_module.DB_PATH
    test_db = str(tmp_path / "test_restaurant.db")
    _db_module.DB_PATH = test_db

    from database.db import init_db
    init_db()

    yield

    _db_module.DB_PATH = original
