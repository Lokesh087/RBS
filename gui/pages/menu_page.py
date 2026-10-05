# gui/pages/menu_page.py – Menu Management CRUD Page
import customtkinter as ctk
from gui.theme import *
from modules.menu import (
    add_menu_item, get_all_menu_items,
    update_menu_item, delete_menu_item,
)

CATEGORIES = ["Starter", "Main Course", "Bread", "Rice", "South Indian",
               "Fast Food", "Beverage", "Dessert", "Other"]


class MenuPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG_DARK)
        self._selected_id = None
        self._build()
        self._load_items()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew", padx=30, pady=(25, 10))
        ctk.CTkLabel(hdr, text="🍽  Menu Management", font=FONT_H1,
                     text_color=TEXT_PRI).pack(side="left")
        ctk.CTkButton(hdr, text="⟳ Refresh", width=90, height=32,
                      font=FONT_SMALL, fg_color=ACCENT2, hover_color="#2563EB",
                      command=self._load_items).pack(side="right")

        # ── Table ──────────────────────────────────────────────────────────────
        table_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=14,
                                   border_width=1, border_color=BORDER)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=(30, 10), pady=10)
        table_frame.grid_rowconfigure(1, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Column headers
        cols = ["ID", "Item Name", "Category", "Price (₹)", "Available"]
        widths = [50, 220, 140, 100, 90]
        hdr_row = ctk.CTkFrame(table_frame, fg_color="#1C2128", corner_radius=8)
        hdr_row.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        for c, (col, w) in enumerate(zip(cols, widths)):
            ctk.CTkLabel(hdr_row, text=col, font=FONT_H3, text_color=ACCENT,
                         width=w, anchor="w").grid(row=0, column=c, padx=8, pady=6, sticky="w")

        self.scroll = ctk.CTkScrollableFrame(table_frame, fg_color="transparent")
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=6)

        # ── Form ──────────────────────────────────────────────────────────────
        form = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=14,
                            border_width=1, border_color=BORDER, width=300)
        form.grid(row=1, column=1, sticky="nsew", padx=(0, 30), pady=10)
        form.grid_propagate(False)
        self._build_form(form)

    def _build_form(self, parent):
        ctk.CTkLabel(parent, text="Add / Edit Item", font=FONT_H2,
                     text_color=TEXT_PRI).pack(pady=(20, 14))

        for label, attr, ph in [
            ("Item Name *", "name_entry", "e.g. Paneer Tikka"),
            ("Price (₹) *", "price_entry", "e.g. 180"),
        ]:
            ctk.CTkLabel(parent, text=label, font=FONT_H3,
                         text_color=TEXT_SEC, anchor="w").pack(fill="x", padx=20)
            e = ctk.CTkEntry(parent, placeholder_text=ph, height=38, font=FONT_BODY,
                             fg_color=ENTRY_FG, border_color=BORDER)
            e.pack(fill="x", padx=20, pady=(4, 12))
            setattr(self, attr, e)

        ctk.CTkLabel(parent, text="Category *", font=FONT_H3,
                     text_color=TEXT_SEC, anchor="w").pack(fill="x", padx=20)
        self.cat_var = ctk.StringVar(value=CATEGORIES[0])
        self.cat_menu = ctk.CTkOptionMenu(parent, values=CATEGORIES,
                                          variable=self.cat_var, height=38, font=FONT_BODY)
        self.cat_menu.pack(fill="x", padx=20, pady=(4, 12))

        self.avail_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(parent, text="Available", variable=self.avail_var,
                        font=FONT_BODY, text_color=TEXT_PRI,
                        checkmark_color=SUCCESS).pack(anchor="w", padx=20, pady=6)

        self.msg_label = ctk.CTkLabel(parent, text="", font=FONT_SMALL,
                                      text_color=SUCCESS, wraplength=260)
        self.msg_label.pack(padx=20, pady=4)

        ctk.CTkButton(parent, text="✅ Save Item", height=42, font=FONT_H3,
                      fg_color=SUCCESS, hover_color="#16A34A",
                      command=self._save).pack(fill="x", padx=20, pady=6)
        ctk.CTkButton(parent, text="🗑 Delete Selected", height=42, font=FONT_H3,
                      fg_color=DANGER, hover_color="#B91C1C",
                      command=self._delete).pack(fill="x", padx=20, pady=4)
        ctk.CTkButton(parent, text="✕ Clear", height=38, font=FONT_BODY,
                      fg_color="#374151", hover_color="#1F2937",
                      command=self._clear).pack(fill="x", padx=20, pady=(4, 20))

    def _load_items(self):
        for w in self.scroll.winfo_children():
            w.destroy()
        items = get_all_menu_items()
        for i, item in enumerate(items):
            row_bg = BG_CARD if i % 2 == 0 else "#1C2128"
            row = ctk.CTkFrame(self.scroll, fg_color=row_bg, corner_radius=6, height=36)
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)
            vals = [str(item["id"]), item["name"], item["category"],
                    f"₹{item['price']:.2f}", "Yes" if item["available"] else "No"]
            widths = [50, 220, 140, 100, 90]
            colors = [TEXT_SEC, TEXT_PRI, TEXT_SEC, ACCENT, SUCCESS if item["available"] else DANGER]
            for c, (v, w, col) in enumerate(zip(vals, widths, colors)):
                ctk.CTkLabel(row, text=v, font=FONT_BODY, text_color=col,
                             width=w, anchor="w").grid(row=0, column=c, padx=8, pady=6, sticky="w")
            row.bind("<Button-1>", lambda e, it=item: self._select(it))
            for child in row.winfo_children():
                child.bind("<Button-1>", lambda e, it=item: self._select(it))

    def _select(self, item: dict):
        self._selected_id = item["id"]
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, item["name"])
        self.price_entry.delete(0, "end")
        self.price_entry.insert(0, str(item["price"]))
        self.cat_var.set(item["category"])
        self.avail_var.set(bool(item["available"]))
        self.msg_label.configure(text=f"Editing: {item['name']}", text_color=ACCENT)

    def _save(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        cat = self.cat_var.get()
        avail = 1 if self.avail_var.get() else 0

        if self._selected_id:
            ok, msg = update_menu_item(self._selected_id, name, cat, price, avail)
        else:
            ok, msg = add_menu_item(name, cat, price)

        self.msg_label.configure(
            text=msg,
            text_color=SUCCESS if ok else DANGER,
        )
        if ok:
            self._clear()
            self._load_items()

    def _delete(self):
        if not self._selected_id:
            self.msg_label.configure(text="Select an item to delete.", text_color=WARNING)
            return
        ok, msg = delete_menu_item(self._selected_id)
        self.msg_label.configure(text=msg, text_color=SUCCESS if ok else DANGER)
        if ok:
            self._clear()
            self._load_items()

    def _clear(self):
        self._selected_id = None
        self.name_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
        self.cat_var.set(CATEGORIES[0])
        self.avail_var.set(True)
        self.msg_label.configure(text="")
