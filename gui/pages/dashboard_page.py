# gui/pages/dashboard_page.py
import customtkinter as ctk
from gui.theme import *
from modules.billing import get_dashboard_stats


class DashboardPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG_DARK)
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=30, pady=(25, 10))
        ctk.CTkLabel(header, text="📊  Dashboard", font=FONT_H1,
                     text_color=TEXT_PRI).pack(side="left")
        self.refresh_btn = ctk.CTkButton(
            header, text="⟳ Refresh", width=100, height=32,
            font=FONT_SMALL, fg_color=ACCENT2, hover_color="#2563EB",
            command=self._refresh,
        )
        self.refresh_btn.pack(side="right")

        # Stats cards row
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        self._refresh()

    def _refresh(self):
        for w in self.cards_frame.winfo_children():
            w.destroy()

        stats = get_dashboard_stats()

        card_data = [
            ("Today's Revenue", f"₹{stats['today_revenue']:,.2f}", "💰", ACCENT),
            ("Total Orders",    str(stats["total_orders"]),         "📋", ACCENT2),
            ("Items Sold",      str(stats["items_sold"]),           "🍽", SUCCESS),
            ("Pending Orders",  str(stats["pending_orders"]),       "⏳", WARNING),
        ]

        self.cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        for col, (title, value, icon, color) in enumerate(card_data):
            self._stat_card(self.cards_frame, title, value, icon, color, col)

        # Quality info section
        info = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=14,
                            border_width=1, border_color=BORDER)
        info.grid(row=2, column=0, sticky="ew", padx=30, pady=10)
        self._build_quality_section(info)

        # Q09 features list
        q09 = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=14,
                            border_width=1, border_color=BORDER)
        q09.grid(row=3, column=0, sticky="nsew", padx=30, pady=(0, 20))
        self.grid_rowconfigure(3, weight=1)
        self._build_q09_section(q09)

    def _stat_card(self, parent, title, value, icon, color, col):
        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=14,
                            border_width=1, border_color=color)
        card.grid(row=0, column=col, padx=8, pady=8, sticky="ew")
        ctk.CTkLabel(card, text=icon, font=("Segoe UI", 30)).pack(pady=(18, 4))
        ctk.CTkLabel(card, text=value, font=("Segoe UI", 26, "bold"),
                     text_color=color).pack()
        ctk.CTkLabel(card, text=title, font=FONT_SMALL,
                     text_color=TEXT_SEC).pack(pady=(2, 18))

    def _build_quality_section(self, parent):
        ctk.CTkLabel(parent, text="🏆  TQM Quality Goal: Q09 – Reduce Bugs",
                     font=FONT_H2, text_color=ACCENT).pack(anchor="w", padx=20, pady=(16, 6))
        ctk.CTkLabel(
            parent,
            text=(
                "This system implements five Q09 quality features to systematically reduce software defects:\n"
                "Strict Validation (Poka-Yoke) • Exception Handling • Module Testing (pytest) "
                "• Bug Tracker • Error Logging"
            ),
            font=FONT_BODY, text_color=TEXT_SEC, wraplength=900, justify="left",
        ).pack(anchor="w", padx=20, pady=(0, 16))

    def _build_q09_section(self, parent):
        ctk.CTkLabel(parent, text="✅  Q09 Feature Implementation Status",
                     font=FONT_H2, text_color=TEXT_PRI).pack(anchor="w", padx=20, pady=(16, 8))

        features = [
            ("✅", "Strict Validation",   "Poka-Yoke: rejects negative prices, invalid phones, empty fields",       SUCCESS),
            ("✅", "Exception Handling",  "All DB operations wrapped; friendly messages, never crashes",             SUCCESS),
            ("✅", "Module Testing",      "pytest suite: 40+ tests across Validation, Menu, Order, Billing modules", SUCCESS),
            ("✅", "Bug Tracker",         "Dedicated CRUD module + DB table for tracking & resolving defects",       SUCCESS),
            ("✅", "Error Logging",       "File + DB dual logging for every error & warning event",                  SUCCESS),
        ]

        for icon, name, desc, color in features:
            row = ctk.CTkFrame(parent, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=4)
            ctk.CTkLabel(row, text=f"{icon}  {name}", font=FONT_H3,
                         text_color=color, width=220, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=desc, font=FONT_BODY,
                         text_color=TEXT_SEC, anchor="w").pack(side="left", padx=10)

        ctk.CTkFrame(parent, height=1, fg_color=BORDER).pack(fill="x", padx=20, pady=8)
        ctk.CTkLabel(parent,
                     text="Default login: username = admin | password = admin123",
                     font=FONT_SMALL, text_color="#555").pack(pady=(0, 12))
