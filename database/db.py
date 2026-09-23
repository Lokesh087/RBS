# database/db.py
# Restaurant Billing System – Database Layer
# TQM Q09: Exception Handling + Error Logging

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "restaurant.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_connection():
    """Return a new SQLite connection with row_factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initialize the database from schema.sql and seed default data."""
    conn = get_connection()
    try:
        with open(SCHEMA_PATH, "r") as f:
            conn.executescript(f.read())
        _seed_defaults(conn)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"DB init failed: {e}") from e
    finally:
        conn.close()


def _seed_defaults(conn):
    """Insert default admin user and sample menu items if empty."""
    cur = conn.cursor()

    # Default admin
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", "admin123", "admin"),
        )

    # Sample menu items
    cur.execute("SELECT COUNT(*) FROM menu_items")
    if cur.fetchone()[0] == 0:
        items = [
            ("Paneer Tikka",    "Starter",      180.0),
            ("Veg Burger",      "Fast Food",    120.0),
            ("Masala Dosa",     "South Indian", 100.0),
            ("Butter Naan",     "Bread",         40.0),
            ("Dal Makhani",     "Main Course",  160.0),
            ("Mango Lassi",     "Beverage",      80.0),
            ("Gulab Jamun",     "Dessert",       60.0),
            ("Cold Drink",      "Beverage",      50.0),
            ("Chicken Biryani", "Main Course",  250.0),
            ("Veg Fried Rice",  "Rice",         130.0),
        ]
        cur.executemany(
            "INSERT INTO menu_items (name, category, price) VALUES (?, ?, ?)", items
        )

    # Seed sample bugs for demonstration / Pareto
    cur.execute("SELECT COUNT(*) FROM bug_tracker")
    if cur.fetchone()[0] == 0:
        bugs = [
            ("BUG001", "Billing",    "Incorrect GST calculation",        "High",   "Fixed"),
            ("BUG002", "Menu",       "Negative price accepted",          "High",   "Fixed"),
            ("BUG003", "Order",      "Zero quantity accepted",           "High",   "Fixed"),
            ("BUG004", "Customer",   "Invalid phone number accepted",    "Medium", "Fixed"),
            ("BUG005", "Billing",    "Bill generated for empty order",   "High",   "Fixed"),
            ("BUG006", "Login",      "No error on wrong password",       "Medium", "Fixed"),
            ("BUG007", "Database",   "DB error not handled gracefully",  "High",   "Fixed"),
            ("BUG008", "Validation", "Empty item name allowed",          "Medium", "Fixed"),
            ("BUG009", "Billing",    "Subtotal not updated on remove",   "Medium", "Fixed"),
            ("BUG010", "Order",      "Duplicate order items merged",     "Low",    "Open"),
        ]
        cur.executemany(
            "INSERT INTO bug_tracker (bug_id, module, description, severity, status) VALUES (?,?,?,?,?)",
            bugs,
        )
