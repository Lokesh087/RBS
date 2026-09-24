# modules/customers.py  – Customer Management CRUD
from database.db import get_connection
from quality.validator import validate_customer, ValidationError
from quality.error_logger import log_error, log_info


def add_customer(name: str, phone: str, email: str) -> tuple[bool, str]:
    try:
        data = validate_customer(name, phone, email)
    except ValidationError as ve:
        return False, str(ve)
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)",
            (data["name"], data["phone"], data["email"]),
        )
        conn.commit()
        conn.close()
        log_info("Customer", f"Added customer: {data['name']}")
        return True, f"✅ Customer '{data['name']}' added."
    except Exception as e:
        log_error("Customer", "Failed to add customer", str(e))
        return False, "⚠️ Unable to save customer."


def get_all_customers() -> list[dict]:
    try:
        conn = get_connection()
        rows = conn.execute("SELECT * FROM customers ORDER BY name").fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        log_error("Customer", "Failed to fetch customers", str(e))
        return []


def update_customer(cust_id: int, name: str, phone: str, email: str) -> tuple[bool, str]:
    try:
        data = validate_customer(name, phone, email)
    except ValidationError as ve:
        return False, str(ve)
    try:
        conn = get_connection()
        conn.execute(
            "UPDATE customers SET name=?, phone=?, email=? WHERE id=?",
            (data["name"], data["phone"], data["email"], cust_id),
        )
        conn.commit()
        conn.close()
        log_info("Customer", f"Updated customer id={cust_id}")
        return True, "✅ Customer updated."
    except Exception as e:
        log_error("Customer", "Failed to update customer", str(e))
        return False, "⚠️ Unable to update customer."


def delete_customer(cust_id: int) -> tuple[bool, str]:
    try:
        conn = get_connection()
        conn.execute("DELETE FROM customers WHERE id=?", (cust_id,))
        conn.commit()
        conn.close()
        log_info("Customer", f"Deleted customer id={cust_id}")
        return True, "✅ Customer deleted."
    except Exception as e:
        log_error("Customer", "Failed to delete customer", str(e))
        return False, "⚠️ Unable to delete customer."