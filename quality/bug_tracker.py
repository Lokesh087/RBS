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


def get_all_bugs():
    """Return all bugs as a list of dicts."""
    try:
        conn = get_connection()
        rows = conn.execute("SELECT * FROM bug_tracker ORDER BY reported_at DESC").fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        log_error("BugTracker", "Failed to fetch bugs", str(e))
        return []


def update_bug_status(bug_id: str, new_status: str):
    """Update the status of a bug; if Fixed, record timestamp."""
    try:
        conn = get_connection()
        resolved_at = datetime.now().isoformat() if new_status == "Fixed" else None
        conn.execute(
            "UPDATE bug_tracker SET status=?, resolved_at=? WHERE bug_id=?",
            (new_status, resolved_at, bug_id),
        )
        conn.commit()
        conn.close()
        return True, "Status updated."
    except Exception as e:
        log_error("BugTracker", "Failed to update bug", str(e))
        return False, str(e)


def delete_bug(bug_id: str):
    """Delete a bug record by bug_id."""
    try:
        conn = get_connection()
        conn.execute("DELETE FROM bug_tracker WHERE bug_id=?", (bug_id,))
        conn.commit()
        conn.close()
        return True, "Bug deleted."
    except Exception as e:
        log_error("BugTracker", "Failed to delete bug", str(e))
        return False, str(e)


def get_bug_summary_by_module():
    """Return a dict of {module: count} for Pareto analysis."""
    try:
        conn = get_connection()
        rows = conn.execute(
            "SELECT module, COUNT(*) as cnt FROM bug_tracker GROUP BY module ORDER BY cnt DESC"
        ).fetchall()
        conn.close()
        return {r["module"]: r["cnt"] for r in rows}
    except Exception as e:
        log_error("BugTracker", "Failed to get summary", str(e))
        return {}
