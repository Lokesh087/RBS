# gui/login_page.py – Login Screen

import customtkinter as ctk
from gui.theme import *
from database.db import get_connection
from quality.validator import validate_login, ValidationError
from quality.error_logger import log_info, log_error


class LoginPage(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master, fg_color=BG_DARK)
        self.on_login_success = on_login_success
        self._build()

    def _build(self):
        # Centre column
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        card = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=20,
                            border_width=1, border_color=BORDER)
        card.grid(row=0, column=0, padx=40, pady=40, ipadx=40, ipady=40)

        # Logo / Title
        ctk.CTkLabel(card, text="🍽", font=("Segoe UI", 56)).pack(pady=(30, 0))
        ctk.CTkLabel(card, text="Spice Garden", font=("Segoe UI", 28, "bold"),
                     text_color=ACCENT).pack()
        ctk.CTkLabel(card, text="Restaurant Billing System",
                     font=FONT_BODY, text_color=TEXT_SEC).pack(pady=(0, 30))

        ctk.CTkLabel(card, text="TQM Project — Q09: Reduce Bugs",
                     font=FONT_SMALL, text_color="#555").pack(pady=(0, 20))

        # ── Fields ──
        ctk.CTkLabel(card, text="Username", font=FONT_H3, text_color=TEXT_PRI,
                     anchor="w").pack(fill="x", padx=30)
        self.username_entry = ctk.CTkEntry(
            card, placeholder_text="Enter username", width=320, height=42,
            font=FONT_BODY, fg_color=ENTRY_FG, border_color=BORDER,
            border_width=1, corner_radius=8,
        )
        self.username_entry.pack(padx=30, pady=(4, 14))
        self.username_entry.insert(0, "admin")

        ctk.CTkLabel(card, text="Password", font=FONT_H3, text_color=TEXT_PRI,
                     anchor="w").pack(fill="x", padx=30)
        self.password_entry = ctk.CTkEntry(
            card, placeholder_text="Enter password", width=320, height=42,
            font=FONT_BODY, fg_color=ENTRY_FG, border_color=BORDER,
            border_width=1, corner_radius=8, show="•",
        )
        self.password_entry.pack(padx=30, pady=(4, 6))
        self.password_entry.insert(0, "admin123")

        self.error_label = ctk.CTkLabel(card, text="", text_color=DANGER,
                                        font=FONT_SMALL)
        self.error_label.pack()

        login_btn = ctk.CTkButton(
            card, text="Login →", command=self._login,
            width=320, height=46, font=FONT_H3,
            fg_color=ACCENT, hover_color=BTN_HOVER,
            corner_radius=10,
        )
        login_btn.pack(padx=30, pady=(16, 30))

        # Bind Enter key
        self.password_entry.bind("<Return>", lambda _: self._login())
        self.username_entry.bind("<Return>", lambda _: self.password_entry.focus())

    def _login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Q09 Feature 1 – Strict Validation
        try:
            creds = validate_login(username, password)
        except ValidationError as ve:
            self.error_label.configure(text=str(ve))
            return

        # Q09 Feature 2 – Exception Handling
        try:
            conn = get_connection()
            user = conn.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (creds["username"], creds["password"]),
            ).fetchone()
            conn.close()
        except Exception as e:
            log_error("Login", "DB error during login", str(e))
            self.error_label.configure(
                text="⚠️ Unable to connect to database. Please try again."
            )
            return

        if user:
            log_info("Login", f"User '{username}' logged in.")
            self.on_login_success(dict(user))
        else:
            log_error("Login", f"Failed login attempt for user '{username}'")
            self.error_label.configure(
                text="❌ Invalid username or password. Please try again."
            )
