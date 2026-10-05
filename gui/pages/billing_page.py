# gui/pages/billing_page.py – Billing Page
import customtkinter as ctk
from gui.theme import *
from modules.billing import calculate_bill, save_bill, format_bill_text, get_bill
from modules.orders import get_all_orders

_pending_order_id = None   # Set by OrdersPage when navigating here


class BillingPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG_DARK)
        self._current_order_id = None
        self._build()
        self._load_orders()

    def _build(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew", padx=30, pady=(25, 10))
        ctk.CTkLabel(hdr, text="🧾  Billing", font=FONT_H1,
                     text_color=TEXT_PRI).pack(side="left")
        ctk.CTkButton(hdr, text="⟳ Refresh", width=90, height=32,
                      font=FONT_SMALL, fg_color=ACCENT2, hover_color="#2563EB",
                      command=self._load_orders).pack(side="right")

        # ── Left: order selector ───────────────────────────────────────────
        left = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=14,
                            border_width=1, border_color=BORDER, width=280)
        left.grid(row=1, column=0, sticky="nsew", padx=(30, 8), pady=10)
        left.grid_propagate(False)
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text="Open Orders", font=FONT_H2,
                     text_color=TEXT_PRI).grid(row=0, column=0, sticky="w",
                                               padx=16, pady=(16, 8))
        self.order_scroll = ctk.CTkScrollableFrame(left, fg_color="transparent")
        self.order_scroll.grid(row=1, column=0, sticky="nsew", padx=8, pady=6)

        # ── Right: bill preview ─────────────────────────────────────────────
        right = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=14,
                             border_width=1, border_color=BORDER)
        right.grid(row=1, column=1, sticky="nsew", padx=(8, 30), pady=10)
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        self.bill_title = ctk.CTkLabel(right, text="Select an order to generate bill",
                                       font=FONT_H2, text_color=TEXT_SEC)
        self.bill_title.grid(row=0, column=0, sticky="w", padx=20, pady=(16, 8))

        self.bill_text = ctk.CTkTextbox(right, font=FONT_MONO, fg_color="#0D1117",
                                        text_color=TEXT_PRI, wrap="none",
                                        border_color=BORDER, border_width=1)
        self.bill_text.grid(row=1, column=0, sticky="nsew", padx=16, pady=6)
        self.bill_text.configure(state="disabled")

        btn_row = ctk.CTkFrame(right, fg_color="transparent")
        btn_row.grid(row=2, column=0, sticky="ew", padx=16, pady=(4, 16))

        ctk.CTkButton(btn_row, text="🔍 Preview Bill", height=42, font=FONT_H3,
                      fg_color=ACCENT2, hover_color="#2563EB",
                      command=self._preview).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_row, text="✅ Generate & Save Bill", height=42, font=FONT_H3,
                      fg_color=SUCCESS, hover_color="#16A34A",
                      command=self._generate).pack(side="left")

        self.status_label = ctk.CTkLabel(btn_row, text="", font=FONT_BODY,
                                         text_color=SUCCESS)
        self.status_label.pack(side="right", padx=10)

    def _load_orders(self):
        for w in self.order_scroll.winfo_children():
            w.destroy()
        orders = get_all_orders()
        for o in orders:
            is_open = o["status"] == "open"
            color = TEXT_PRI if is_open else TEXT_SEC
            btn = ctk.CTkButton(
                self.order_scroll,
                text=f"#{o['id']}  {o['customer_name']}\n{o['status'].upper()}  ₹{o['total']:.2f}",
                anchor="w", height=52, font=FONT_SMALL,
                fg_color="#1C2128" if is_open else "#111",
                hover_color="#1F2937",
                text_color=color,
                corner_radius=8,
                command=lambda oid=o["id"]: self._select_order(oid),
            )
            btn.pack(fill="x", pady=3, padx=4)

    def _load_pending(self):
        """Called from OrdersPage to pre-select an order."""
        global _pending_order_id
        if _pending_order_id:
            self._select_order(_pending_order_id)
            _pending_order_id = None

    def _select_order(self, order_id: int):
        self._current_order_id = order_id
        self.bill_title.configure(
            text=f"Order #{order_id}", text_color=ACCENT
        )
        self.status_label.configure(text="")
        # Check if already billed
        existing = get_bill(order_id)
        if existing:
            text = format_bill_text(existing)
            self._set_bill_text(text)
            self.status_label.configure(
                text="✅ Already billed", text_color=WARNING
            )
        else:
            self._preview_inner(order_id)

    def _preview(self):
        if not self._current_order_id:
            self.status_label.configure(
                text="❌ Select an order first.", text_color=DANGER
            )
            return
        self._preview_inner(self._current_order_id)

    def _preview_inner(self, order_id: int):
        ok, result = calculate_bill(order_id)
        if ok:
            text = format_bill_text(result)
            self._set_bill_text(text)
            self.status_label.configure(
                text="Preview only – not saved yet.", text_color=WARNING
            )
        else:
            self._set_bill_text(result)
            self.status_label.configure(text=result, text_color=DANGER)

    def _generate(self):
        if not self._current_order_id:
            self.status_label.configure(
                text="❌ Select an order first.", text_color=DANGER
            )
            return
        ok, msg = save_bill(self._current_order_id)
        self.status_label.configure(
            text=msg, text_color=SUCCESS if ok else DANGER
        )
        if ok:
            bill = get_bill(self._current_order_id)
            if bill:
                self._set_bill_text(format_bill_text(bill))
            self._load_orders()

    def _set_bill_text(self, text: str):
        self.bill_text.configure(state="normal")
        self.bill_text.delete("1.0", "end")
        self.bill_text.insert("1.0", text)
        self.bill_text.configure(state="disabled")
