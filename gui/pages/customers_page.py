# gui/pages/customers_page.py – Customer Management CRUD Page
import customtkinter as ctk
from gui.theme import *
from modules.customers import add_customer, get_all_customers, update_customer, delete_customer


class CustomersPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG_DARK)
        self._selected_id = None
        self._build()
        self._load()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(1, weight=1)

        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew", padx=30, pady=(25, 10))
        ctk.CTkLabel(hdr, text="👥  Customer Management", font=FONT_H1,
                     text_color=TEXT_PRI).pack(side="left")
        ctk.CTkButton(hdr, text="⟳ Refresh", width=90, height=32,
                      font=FONT_SMALL, fg_color=ACCENT2, hover_color="#2563EB",
                      command=self._load).pack(side="right")

        # Table
        tbl = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=14,
                           border_width=1, border_color=BORDER)
        tbl.grid(row=1, column=0, sticky="nsew", padx=(30, 10), pady=10)
        tbl.grid_rowconfigure(1, weight=1)
        tbl.grid_columnconfigure(0, weight=1)

        cols  = ["ID", "Name",    "Phone",       "Email",             "Joined"]
        widths = [50,   200,       130,            220,                120]
        hrow = ctk.CTkFrame(tbl, fg_color="#1C2128", corner_radius=8)
        hrow.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        for c, (col, w) in enumerate(zip(cols, widths)):
            ctk.CTkLabel(hrow, text=col, font=FONT_H3, text_color=ACCENT,
                         width=w, anchor="w").grid(row=0, column=c, padx=8, pady=6, sticky="w")

        self.scroll = ctk.CTkScrollableFrame(tbl, fg_color="transparent")
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=6)

        # Form
        form = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=14,
                            border_width=1, border_color=BORDER, width=300)
        form.grid(row=1, column=1, sticky="nsew", padx=(0, 30), pady=10)
        form.grid_propagate(False)
        self._build_form(form)

    def _build_form(self, p):
        ctk.CTkLabel(p, text="Add / Edit Customer", font=FONT_H2,
                     text_color=TEXT_PRI).pack(pady=(20, 14))

        fields = [
            ("Name *",  "name_entry",  "e.g. Rahul Sharma"),
            ("Phone",   "phone_entry", "e.g. 9876543210"),
            ("Email",   "email_entry", "e.g. rahul@example.com"),
        ]
        for label, attr, ph in fields:
            ctk.CTkLabel(p, text=label, font=FONT_H3,
                         text_color=TEXT_SEC, anchor="w").pack(fill="x", padx=20)
            e = ctk.CTkEntry(p, placeholder_text=ph, height=38, font=FONT_BODY,
                             fg_color=ENTRY_FG, border_color=BORDER)
            e.pack(fill="x", padx=20, pady=(4, 12))
            setattr(self, attr, e)

        self.msg = ctk.CTkLabel(p, text="", font=FONT_SMALL,
                                text_color=SUCCESS, wraplength=260)
        self.msg.pack(padx=20, pady=4)

        ctk.CTkButton(p, text="✅ Save", height=42, font=FONT_H3,
                      fg_color=SUCCESS, hover_color="#16A34A",
                      command=self._save).pack(fill="x", padx=20, pady=6)
        ctk.CTkButton(p, text="🗑 Delete", height=42, font=FONT_H3,
                      fg_color=DANGER, hover_color="#B91C1C",
                      command=self._delete).pack(fill="x", padx=20, pady=4)
        ctk.CTkButton(p, text="✕ Clear", height=38, font=FONT_BODY,
                      fg_color="#374151", hover_color="#1F2937",
                      command=self._clear).pack(fill="x", padx=20, pady=(4, 20))

    def _load(self):
        for w in self.scroll.winfo_children():
            w.destroy()
        customers = get_all_customers()
        for i, c in enumerate(customers):
            bg = BG_CARD if i % 2 == 0 else "#1C2128"
            row = ctk.CTkFrame(self.scroll, fg_color=bg, corner_radius=6, height=36)
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)
            vals   = [str(c["id"]), c["name"], c["phone"] or "—", c["email"] or "—",
                      c["created_at"][:10]]
            widths = [50, 200, 130, 220, 120]
            colors = [TEXT_SEC, TEXT_PRI, TEXT_SEC, TEXT_SEC, TEXT_SEC]
            for ci, (v, w, col) in enumerate(zip(vals, widths, colors)):
                ctk.CTkLabel(row, text=v, font=FONT_BODY, text_color=col,
                             width=w, anchor="w").grid(row=0, column=ci, padx=8, pady=6, sticky="w")
            row.bind("<Button-1>", lambda e, cu=c: self._select(cu))
            for child in row.winfo_children():
                child.bind("<Button-1>", lambda e, cu=c: self._select(cu))

    def _select(self, c: dict):
        self._selected_id = c["id"]
        self.name_entry.delete(0, "end"); self.name_entry.insert(0, c["name"])
        self.phone_entry.delete(0, "end"); self.phone_entry.insert(0, c["phone"] or "")
        self.email_entry.delete(0, "end"); self.email_entry.insert(0, c["email"] or "")
        self.msg.configure(text=f"Editing: {c['name']}", text_color=ACCENT)

    def _save(self):
        name  = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        if self._selected_id:
            ok, msg = update_customer(self._selected_id, name, phone, email)
        else:
            ok, msg = add_customer(name, phone, email)
        self.msg.configure(text=msg, text_color=SUCCESS if ok else DANGER)
        if ok:
            self._clear(); self._load()

    def _delete(self):
        if not self._selected_id:
            self.msg.configure(text="Select a customer to delete.", text_color=WARNING)
            return
        ok, msg = delete_customer(self._selected_id)
        self.msg.configure(text=msg, text_color=SUCCESS if ok else DANGER)
        if ok:
            self._clear(); self._load()

    def _clear(self):
        self._selected_id = None
        for entry in [self.name_entry, self.phone_entry, self.email_entry]:
            entry.delete(0, "end")
        self.msg.configure(text="")
