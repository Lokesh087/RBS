# app.py – Spice Garden Restaurant Billing System
# TQM Project: Q09 – Reduce Bugs
# Main entry point: initialises DB, loads GUI

import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(__file__))

from database.db import init_db
from quality.error_logger import log_info, log_error

try:
    import customtkinter as ctk
except ImportError:
    print("ERROR: customtkinter not installed. Run: pip install customtkinter")
    sys.exit(1)

# ── GUI Pages ──────────────────────────────────────────────────────────────────
from gui.login_page import LoginPage
from gui.main_window import MainWindow


def main():
    log_info("App", "Application starting...")
    try:
        init_db()
        log_info("App", "Database initialised.")
    except Exception as e:
        log_error("App", "Failed to initialise database", str(e))
        print(f"[FATAL] DB init failed: {e}")
        sys.exit(1)

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("🍽  Spice Garden – Restaurant Billing System")
    root.geometry("1200x750")
    root.minsize(1100, 680)

    # Start with login
    app = LoginPage(root, on_login_success=lambda user: _launch_main(root, user))
    app.pack(fill="both", expand=True)

    root.mainloop()


def _launch_main(root: ctk.CTk, user: dict):
    """Destroy login frame, load main window."""
    for widget in root.winfo_children():
        widget.destroy()
    main_win = MainWindow(root, user=user)
    main_win.pack(fill="both", expand=True)


if __name__ == "__main__":
    main()
