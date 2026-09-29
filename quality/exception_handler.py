# quality/exception_handler.py
# Q09 Feature 2 – Exception Handling
# Wraps risky operations so the app never crashes on the user.

from quality.error_logger import log_error


def safe_db_operation(func, module: str, user_msg: str = None):
    """
    Execute *func* safely.
    Returns (result, None) on success or (None, error_message) on failure.
    """
    try:
        result = func()
        return result, None
    except Exception as exc:
        details = str(exc)
        log_error(module, f"Exception in safe_db_operation: {user_msg}", details)
        friendly = user_msg or "An unexpected error occurred. Please try again."
        return None, friendly


def handle_exception(exc: Exception, module: str, context: str = "") -> str:
    """
    Log an exception and return a user-friendly message string.
    Used inside GUI event handlers.
    """
    details = str(exc)
    log_error(module, context or "Unhandled exception", details)
    return f"⚠️ {context or 'An error occurred.'}\nPlease check the error logs."
