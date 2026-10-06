# gui/main_window.py – Main application shell with sidebar navigation

import customtkinter as ctk
from gui.theme import *

from gui.pages.dashboard_page import DashboardPage
from gui.pages.menu_page import MenuPage
from gui.pages.customers_page import CustomersPage
from gui.pages.orders_page import OrdersPage
from gui.pages.billing_page import BillingPage
from gui.pages.bugs_page import BugsPage
from gui.pages.reports_page import ReportsPage
from gui.pages.logs_page import LogsPage


PAGE_MAP = {
    "dashboard": DashboardPage,
    "menu":       MenuPage,
    "customers":  CustomersPage,
    "orders":     OrdersPage,
    "billing":    BillingPage,
    "bugs":       BugsPage,
    "reports":    ReportsPage,
    "logs":       LogsPage,
}


class MainWindow(ctk.CTkFrame):
    def __init__(self, master, user: dict):
        super().__init__(master, fg_color=BG_DARK)
        self.user = user
        self._pages: dict[str, ctk.CTkFrame] = {}
        self._nav_buttons: dict[str, ctk.CTkButton] = {}
        self._build()
        self._show_page("dashboard")

    # ── Layout ─────────────────────────────────────────────────────────────────
    def _build(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        sidebar = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        self._build_sidebar(sidebar)

        # Content area
        self.content = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

    def _build_sidebar(self, sidebar):
        sidebar.grid_rowconfigure(len(NAV_ITEMS) + 2, weight=1)

        # Logo area
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", pady=(20, 10), padx=14)
        ctk.CTkLabel(logo_frame, text="🍽", font=("Segoe UI", 32)).pack()
        ctk.CTkLabel(logo_frame, text="Spice Garden", font=("Segoe UI", 14, "bold"),
                     text_color=ACCENT).pack()
        ctk.CTkLabel(logo_frame, text="Billing System",
                     font=FONT_SMALL, text_color=TEXT_SEC).pack()

        ctk.CTkFrame(sidebar, height=1, fg_color=BORDER).pack(fill="x", padx=14, pady=10)

        # Nav buttons
        for label, icon, key in NAV_ITEMS:
            btn = ctk.CTkButton(
                sidebar, text=f"  {icon}  {label}",
                anchor="w", height=42,
                font=FONT_BODY,
                fg_color="transparent",
                hover_color="#1F2937",
                text_color=TEXT_SEC,
                corner_radius=8,
                command=lambda k=key: self._show_page(k),
            )
            btn.pack(fill="x", padx=10, pady=2)
            self._nav_buttons[key] = btn

        # Spacer + User info at bottom
        ctk.CTkFrame(sidebar, fg_color="transparent").pack(expand=True, fill="both")
        ctk.CTkFrame(sidebar, height=1, fg_color=BORDER).pack(fill="x", padx=14, pady=6)
        user_frame = ctk.CTkFrame(sidebar, fg_color="#1C2128", corner_radius=10)
        user_frame.pack(fill="x", padx=10, pady=(0, 14))
        ctk.CTkLabel(user_frame, text=f"👤 {self.user['username']}",
                     font=FONT_H3, text_color=TEXT_PRI).pack(pady=(8, 2))
        ctk.CTkLabel(user_frame, text=self.user.get("role", "staff").upper(),
                     font=FONT_SMALL, text_color=ACCENT).pack(pady=(0, 4))
        ctk.CTkButton(user_frame, text="Logout", height=30, font=FONT_SMALL,
                      fg_color=DANGER, hover_color="#B91C1C",
                      command=self._logout).pack(pady=(4, 8))

    # ── Navigation ─────────────────────────────────────────────────────────────
    def _show_page(self, key: str):
        # Reset all nav buttons
        for k, btn in self._nav_buttons.items():
            btn.configure(
                fg_color="#1C2128" if k == key else "transparent",
                text_color=ACCENT if k == key else TEXT_SEC,
                font=("Segoe UI", 12, "bold") if k == key else FONT_BODY,
            )

        # Lazy-create page
        if key not in self._pages:
            PageClass = PAGE_MAP.get(key)
            if PageClass is None:
                return
            page = PageClass(self.content)
            page.grid(row=0, column=0, sticky="nsew")
            self._pages[key] = page

        # Show selected, hide others
        for k, page in self._pages.items():
            if k == key:
                page.lift()
            # else page stays in grid but under

    def _logout(self):
        """Return to login screen."""
        from gui.login_page import LoginPage
        master = self.master
        for widget in master.winfo_children():
            widget.destroy()
        from app import _launch_main
        login = LoginPage(master, on_login_success=lambda u: _launch_main(master, u))
        login.pack(fill="both", expand=True)
