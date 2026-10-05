# gui/pages/orders_page.py – Order Management Page
import customtkinter as ctk
from gui.theme import *
from modules.orders import (
    create_order, add_order_item, remove_order_item,
    get_order_items, get_all_orders, delete_order,
)
from modules.menu import get_all_menu_items
from modules.customers import get_all_customers


class OrdersPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG_DARK)
        self._current_order_id = None
        self._menu_map: dict[str, dict] = {}   # "Name (₹price)" → item dict
        self._build()
        self._load_orders()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew", padx=30, pady=(25, 10))
        ctk.CTkLabel(hdr, text="📋  Order Management", font=FONT_H1,
                     text_color=TEXT_PRI).pack(side="left")

        # ── Left: existing orders ───────────────────────────────────────────
        left = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=14,
                            border_width=1, border_color=BORDER)
        left.grid(row=1, column=0, sticky="nsew", padx=(30, 8), pady=10)
        left.grid_rowconfigure(2, weight=1)
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text="All Orders", font=FONT_H2,
                     text_color=TEXT_PRI).grid(row=0, column=0, sticky="w", padx=16, pady=(16, 4))

        hrow = ctk.CTkFrame(left, fg_color="#1C2128", corner_radius=6)
        hrow.grid(row=1, column=0, sticky="ew", padx=10)
        for c, (label, w) in enumerate([("Order#", 60), ("Customer", 130), ("Status", 80), ("Total", 90)]):
            ctk.CTkLabel(hrow, text=label, font=FONT_H3, text_color=ACCENT,
                         width=w, anchor="w").grid(row=0, column=c, padx=8, pady=6, sticky="w")

        self.order_scroll = ctk.CTkScrollableFrame(left, fg_color="transparent")
        self.order_scroll.grid(row=2, column=0, sticky="nsew", padx=10, pady=6)

        ctk.CTkButton(left, text="➕ New Order", height=40, font=FONT_H3,
                      fg_color=ACCENT, hover_color=BTN_HOVER,
                      command=self._new_order).grid(row=3, column=0, sticky="ew",
                                                    padx=16, pady=(6, 16))

        # ── Right: active order builder ─────────────────────────────────────
        right = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=14,
                             border_width=1, border_color=BORDER)
        right.grid(row=1, column=1, sticky="nsew", padx=(8, 30), pady=10)
        right.grid_rowconfigure(3, weight=1)
        right.grid_columnconfigure(0, weight=1)
        self._build_order_builder(right)

    def _build_order_builder(self, parent):
        self.order_title = ctk.CTkLabel(parent, text="No active order",
                                        font=FONT_H2, text_color=TEXT_SEC)
        self.order_title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        # Item selector row
        sel_row = ctk.CTkFrame(parent, fg_color="transparent")
        sel_row.grid(row=1, column=0, sticky="ew", padx=16, pady=4)
        self.item_var = ctk.StringVar(value="Select item")
        self.item_menu = ctk.CTkOptionMenu(sel_row, variable=self.item_var,
                                           values=["Select item"], width=220, height=38, font=FONT_BODY)
        self.item_menu.pack(side="left", padx=(0, 8))
        self.qty_entry = ctk.CTkEntry(sel_row, placeholder_text="Qty", width=70,
                                      height=38, font=FONT_BODY, fg_color=ENTRY_FG)
        self.qty_entry.pack(side="left", padx=(0, 8))
        ctk.CTkButton(sel_row, text="Add", width=80, height=38, font=FONT_H3,
                      fg_color=SUCCESS, hover_color="#16A34A",
                      command=self._add_item).pack(side="left")

        self.msg = ctk.CTkLabel(parent, text="", font=FONT_SMALL,
                                text_color=DANGER, wraplength=380)
        self.msg.grid(row=2, column=0, sticky="w", padx=16)

        # Order items list
        self.items_scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.items_scroll.grid(row=3, column=0, sticky="nsew", padx=10, pady=6)

        # Total label + bill button
        self.total_label = ctk.CTkLabel(parent, text="", font=FONT_H2, text_color=ACCENT)
        self.total_label.grid(row=4, column=0, sticky="e", padx=16, pady=4)

        action_row = ctk.CTkFrame(parent, fg_color="transparent")
        action_row.grid(row=5, column=0, sticky="ew", padx=16, pady=(4, 16))
        ctk.CTkButton(action_row, text="🗑 Delete Order", height=40, font=FONT_BODY,
                      fg_color=DANGER, hover_color="#B91C1C",
                      command=self._delete_order).pack(side="left", padx=(0, 8))
        ctk.CTkButton(action_row, text="🧾 Go to Billing →", height=40, font=FONT_H3,
                      fg_color=ACCENT, hover_color=BTN_HOVER,
                      command=self._go_billing).pack(side="right")

        self._reload_menu_options()

    def _reload_menu_options(self):
        items = get_all_menu_items(available_only=True)
        self._menu_map = {}
        for item in items:
            key = f"{item['name']}  (₹{item['price']:.0f})"
            self._menu_map[key] = item
        options = list(self._menu_map.keys()) or ["No items available"]
        self.item_menu.configure(values=options)
        if options:
            self.item_var.set(options[0])

    def _load_orders(self):
        for w in self.order_scroll.winfo_children():
            w.destroy()
        orders = get_all_orders()
        for i, o in enumerate(orders):
            bg = BG_CARD if i % 2 == 0 else "#1C2128"
            row = ctk.CTkFrame(self.order_scroll, fg_color=bg, corner_radius=6)
            row.pack(fill="x", pady=2)
            status_col = SUCCESS if o["status"] == "closed" else WARNING
            for c, (v, w, col) in enumerate(zip(
                [f"#{o['id']}", o["customer_name"], o["status"].upper(), f"₹{o['total']:.2f}"],
                [60, 130, 80, 90],
                [TEXT_SEC, TEXT_PRI, status_col, ACCENT],
            )):
                ctk.CTkLabel(row, text=v, font=FONT_BODY, text_color=col,
                             width=w, anchor="w").grid(row=0, column=c, padx=8, pady=6)
            row.bind("<Button-1>", lambda e, od=o: self._select_order(od["id"]))
            for child in row.winfo_children():
                child.bind("<Button-1>", lambda e, od=o: self._select_order(od["id"]))

    def _select_order(self, order_id: int):
        self._current_order_id = order_id
        self._refresh_items()

    def _new_order(self):
        ok, result = create_order()
        if ok:
            self._current_order_id = result
            self._load_orders()
            self._refresh_items()
            self.msg.configure(text=f"✅ Order #{result} created.", text_color=SUCCESS)
        else:
            self.msg.configure(text=result, text_color=DANGER)

    def _add_item(self):
        if not self._current_order_id:
            self.msg.configure(text="❌ Create or select an order first.", text_color=DANGER)
            return
        key = self.item_var.get()
        item = self._menu_map.get(key)
        if not item:
            self.msg.configure(text="❌ Please select a valid menu item.", text_color=DANGER)
            return
        qty = self.qty_entry.get()
        ok, msg = add_order_item(self._current_order_id, item["id"], qty, item["price"])
        self.msg.configure(text=msg, text_color=SUCCESS if ok else DANGER)
        if ok:
            self.qty_entry.delete(0, "end")
            self._refresh_items()

    def _refresh_items(self):
        if not self._current_order_id:
            return
        self.order_title.configure(
            text=f"Active Order: #{self._current_order_id}", text_color=ACCENT
        )
        for w in self.items_scroll.winfo_children():
            w.destroy()
        items = get_order_items(self._current_order_id)
        total = 0.0
        for item in items:
            total += item["line_total"]
            irow = ctk.CTkFrame(self.items_scroll, fg_color="#1C2128", corner_radius=6)
            irow.pack(fill="x", pady=2)
            ctk.CTkLabel(irow, text=item["name"], font=FONT_BODY,
                         text_color=TEXT_PRI, width=180, anchor="w").grid(row=0, column=0, padx=8, pady=5)
            ctk.CTkLabel(irow, text=f"x{item['quantity']}", font=FONT_BODY,
                         text_color=TEXT_SEC).grid(row=0, column=1, padx=8)
            ctk.CTkLabel(irow, text=f"₹{item['line_total']:.2f}", font=FONT_H3,
                         text_color=ACCENT).grid(row=0, column=2, padx=8)
            ctk.CTkButton(irow, text="✕", width=28, height=28, font=FONT_SMALL,
                          fg_color=DANGER, hover_color="#B91C1C", corner_radius=6,
                          command=lambda oi=item["id"]: self._remove_item(oi),
                          ).grid(row=0, column=3, padx=8)
        self.total_label.configure(text=f"Subtotal: ₹{total:.2f}")

    def _remove_item(self, order_item_id: int):
        remove_order_item(order_item_id)
        self._refresh_items()

    def _delete_order(self):
        if not self._current_order_id:
            return
        ok, msg = delete_order(self._current_order_id)
        if ok:
            self._current_order_id = None
            self.order_title.configure(text="No active order", text_color=TEXT_SEC)
            for w in self.items_scroll.winfo_children():
                w.destroy()
            self.total_label.configure(text="")
            self._load_orders()

    def _go_billing(self):
        """Navigate to Billing page with current order pre-selected."""
        if not self._current_order_id:
            self.msg.configure(text="❌ No active order to bill.", text_color=DANGER)
            return
        # Store in a simple shared var — BillingPage reads it on focus
        import gui.pages.billing_page as bp
        bp._pending_order_id = self._current_order_id
        # Trigger nav
        main = self.master.master
        if hasattr(main, "_show_page"):
            main._show_page("billing")
        # Re-load billing
        if "billing" in main._pages:
            main._pages["billing"]._load_pending()
