# quality/error_logger.py
# Q09 Feature 5 – Error Logging
# Logs errors to both a file (logs/error.log) and the DB error_logs table.

import logging
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "error.log")

# Configure Python logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

_file_logger = logging.getLogger("RBS")


def log_error(module: str, message: str, details: str = ""):
    """Log an ERROR to file and database."""
    _write_log("ERROR", module, message, details)


def log_warning(module: str, message: str, details: str = ""):
    """Log a WARNING to file and database."""
    _write_log("WARNING", module, message, details)


def log_info(module: str, message: str, details: str = ""):
    """Log an INFO entry to file."""
    _file_logger.info(f"[{module}] {message}")


def get_all_logs(limit: int = 200) -> list[dict]:
    """Fetch recent error_logs entries from DB."""
    try:
        from database.db import get_connection
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM error_logs ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


def _write_log(level: str, module: str, message: str, details: str):
    """Write to file logger and insert into DB."""
    full_msg = f"[{module}] {message}"
    if level == "ERROR":
        _file_logger.error(full_msg + (f" | {details}" if details else ""))
    elif level == "WARNING":
        _file_logger.warning(full_msg + (f" | {details}" if details else ""))

    # Persist to DB (import here to avoid circular)
    try:
        from database.db import get_connection
        conn = get_connection()
        conn.execute(
            "INSERT INTO error_logs (level, module, message, details) VALUES (?,?,?,?)",
            (level, module, message, details),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass  # Never let logging break the app
