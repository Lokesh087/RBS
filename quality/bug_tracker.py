# quality/bug_tracker.py
# Q09 Feature 4 – Bug Tracker
# CRUD interface for the bug_tracker table used in TQM analysis.

from database.db import get_connection
from quality.error_logger import log_error
from datetime import datetime


def add_bug(bug_id: str, module: str, description: str, severity: str, status: str = "Open"):
    """Insert a new bug record."""
    try:
        conn = get_connection()
        conn.execute(
            """INSERT INTO bug_tracker (bug_id, module, description, severity, status)
               VALUES (?, ?, ?, ?, ?)""",
            (bug_id, module, description, severity, status),
        )
        conn.commit()
        conn.close()
        return True, "Bug added successfully."
    except Exception as e:
        log_error("BugTracker", "Failed to add bug", str(e))
        return False, f"Error: {e}"


