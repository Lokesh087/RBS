# gui/pages/bugs_page.py – Bug Tracker Page (Q09 Feature 4)
import customtkinter as ctk
from gui.theme import *
from quality.bug_tracker import (
    add_bug, get_all_bugs, update_bug_status, delete_bug,
)

SEVERITIES = ["High", "Medium", "Low"]
STATUSES   = ["Open", "In Progress", "Fixed", "Closed"]


class BugsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG_DARK)
        self._selected_bug_id = None
        self._build()
        self._load()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew", padx=30, pady=(25, 10))
        ctk.CTkLabel(hdr, text="🐛  Bug Tracker", font=FONT_H1,
                     text_color=TEXT_PRI).pack(side="left")
        q09_badge = ctk.CTkLabel(
            hdr,
            text="  Q09 Feature 4 – Defect Tracking  ",
            font=FONT_SMALL, text_color="white",
            fg_color=ACCENT2, corner_radius=8,
        )
        q09_badge.pack(side="left", padx=16)
        ctk.CTkButton(hdr, text="⟳ Refresh", width=90, height=32,
                      font=FONT_SMALL, fg_color=ACCENT2, hover_color="#2563EB",
                      command=self._load).pack(side="right")

        # ── Table ──────────────────────────────────────────────────────────
        tbl = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=14,
                           border_width=1, border_color=BORDER)
        tbl.grid(row=1, column=0, sticky="nsew", padx=(30, 10), pady=10)
        tbl.grid_rowconfigure(2, weight=1)
        tbl.grid_columnconfigure(0, weight=1)

        # Summary strip
        self.summary_label = ctk.CTkLabel(tbl, text="", font=FONT_BODY,
                                          text_color=TEXT_SEC)
        self.summary_label.grid(row=0, column=0, sticky="w", padx=16, pady=(12, 4))

        cols   = ["Bug ID", "Module",    "Description",        "Severity", "Status",  "Reported"]
        widths = [80,        110,          260,                   90,         110,        110]
        hrow   = ctk.CTkFrame(tbl, fg_color="#1C2128", corner_radius=6)
        hrow.grid(row=1, column=0, sticky="ew", padx=10)
        for c, (col, w) in enumerate(zip(cols, widths)):
            ctk.CTkLabel(hrow, text=col, font=FONT_H3, text_color=ACCENT,
                         width=w, anchor="w").grid(row=0, column=c, padx=8, pady=6, sticky="w")

        self.scroll = ctk.CTkScrollableFrame(tbl, fg_color="transparent")
        self.scroll.grid(row=2, column=0, sticky="nsew", padx=10, pady=6)

        # ── Form ──────────────────────────────────────────────────────────
        form = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=14,
                            border_width=1, border_color=BORDER, width=300)
        form.grid(row=1, column=1, sticky="nsew", padx=(0, 30), pady=10)
        form.grid_propagate(False)
        self._build_form(form)

    def _build_form(self, p):
        ctk.CTkLabel(p, text="Add / Update Bug", font=FONT_H2,
                     text_color=TEXT_PRI).pack(pady=(20, 10))

        for label, attr, ph in [
            ("Bug ID *",     "bugid_entry",  "e.g. BUG011"),
            ("Module *",     "module_entry", "e.g. Billing"),
            ("Description *","desc_entry",   "Short description"),
        ]:
            ctk.CTkLabel(p, text=label, font=FONT_H3,
                         text_color=TEXT_SEC, anchor="w").pack(fill="x", padx=20)
            e = ctk.CTkEntry(p, placeholder_text=ph, height=38, font=FONT_BODY,
                             fg_color=ENTRY_FG, border_color=BORDER)
            e.pack(fill="x", padx=20, pady=(4, 10))
            setattr(self, attr, e)

        ctk.CTkLabel(p, text="Severity *", font=FONT_H3,
                     text_color=TEXT_SEC, anchor="w").pack(fill="x", padx=20)
        self.sev_var = ctk.StringVar(value="High")
        ctk.CTkOptionMenu(p, values=SEVERITIES, variable=self.sev_var,
                          height=38, font=FONT_BODY).pack(fill="x", padx=20, pady=(4, 10))

        ctk.CTkLabel(p, text="Status", font=FONT_H3,
                     text_color=TEXT_SEC, anchor="w").pack(fill="x", padx=20)
        self.status_var = ctk.StringVar(value="Open")
        ctk.CTkOptionMenu(p, values=STATUSES, variable=self.status_var,
                          height=38, font=FONT_BODY).pack(fill="x", padx=20, pady=(4, 10))

        self.msg = ctk.CTkLabel(p, text="", font=FONT_SMALL,
                                text_color=SUCCESS, wraplength=260)
        self.msg.pack(padx=20, pady=4)

        ctk.CTkButton(p, text="✅ Save Bug", height=42, font=FONT_H3,
                      fg_color=SUCCESS, hover_color="#16A34A",
                      command=self._save).pack(fill="x", padx=20, pady=6)
        ctk.CTkButton(p, text="🔄 Update Status", height=42, font=FONT_H3,
                      fg_color=ACCENT2, hover_color="#2563EB",
                      command=self._update_status).pack(fill="x", padx=20, pady=4)
        ctk.CTkButton(p, text="🗑 Delete", height=42, font=FONT_H3,
                      fg_color=DANGER, hover_color="#B91C1C",
                      command=self._delete).pack(fill="x", padx=20, pady=4)
        ctk.CTkButton(p, text="✕ Clear", height=36, font=FONT_BODY,
                      fg_color="#374151", hover_color="#1F2937",
                      command=self._clear).pack(fill="x", padx=20, pady=(4, 20))

    def _load(self):
        for w in self.scroll.winfo_children():
            w.destroy()
        bugs = get_all_bugs()

        open_cnt  = sum(1 for b in bugs if b["status"] == "Open")
        fixed_cnt = sum(1 for b in bugs if b["status"] == "Fixed")
        self.summary_label.configure(
            text=f"Total: {len(bugs)}  |  Open: {open_cnt}  |  Fixed: {fixed_cnt}"
        )

        sev_colors = {"High": DANGER, "Medium": WARNING, "Low": SUCCESS}
        stat_colors = {"Open": DANGER, "In Progress": WARNING,
                       "Fixed": SUCCESS, "Closed": TEXT_SEC}

        for i, bug in enumerate(bugs):
            bg = BG_CARD if i % 2 == 0 else "#1C2128"
            row = ctk.CTkFrame(self.scroll, fg_color=bg, corner_radius=6)
            row.pack(fill="x", pady=2)
            vals   = [bug["bug_id"], bug["module"], bug["description"],
                      bug["severity"], bug["status"], bug["reported_at"][:10]]
            widths = [80, 110, 260, 90, 110, 110]
            colors = [TEXT_SEC, TEXT_PRI, TEXT_SEC,
                      sev_colors.get(bug["severity"], TEXT_SEC),
                      stat_colors.get(bug["status"], TEXT_SEC),
                      TEXT_SEC]
            for c, (v, w, col) in enumerate(zip(vals, widths, colors)):
                ctk.CTkLabel(row, text=v, font=FONT_BODY, text_color=col,
                             width=w, anchor="w").grid(row=0, column=c, padx=8, pady=6)
            row.bind("<Button-1>", lambda e, b=bug: self._select(b))
            for child in row.winfo_children():
                child.bind("<Button-1>", lambda e, b=bug: self._select(b))

    def _select(self, bug: dict):
        self._selected_bug_id = bug["bug_id"]
        self.bugid_entry.delete(0, "end"); self.bugid_entry.insert(0, bug["bug_id"])
        self.module_entry.delete(0, "end"); self.module_entry.insert(0, bug["module"])
        self.desc_entry.delete(0, "end"); self.desc_entry.insert(0, bug["description"])
        self.sev_var.set(bug["severity"])
        self.status_var.set(bug["status"])
        self.msg.configure(text=f"Selected: {bug['bug_id']}", text_color=ACCENT)

    def _save(self):
        bug_id = self.bugid_entry.get().strip()
        module = self.module_entry.get().strip()
        desc   = self.desc_entry.get().strip()
        sev    = self.sev_var.get()
        status = self.status_var.get()
        if not bug_id or not module or not desc:
            self.msg.configure(text="❌ Bug ID, Module and Description are required.",
                               text_color=DANGER)
            return
        ok, msg = add_bug(bug_id, module, desc, sev, status)
        self.msg.configure(text=msg, text_color=SUCCESS if ok else DANGER)
        if ok:
            self._clear(); self._load()

    def _update_status(self):
        if not self._selected_bug_id:
            self.msg.configure(text="Select a bug first.", text_color=WARNING)
            return
        ok, msg = update_bug_status(self._selected_bug_id, self.status_var.get())
        self.msg.configure(text=msg, text_color=SUCCESS if ok else DANGER)
        if ok:
            self._load()

    def _delete(self):
        if not self._selected_bug_id:
            self.msg.configure(text="Select a bug first.", text_color=WARNING)
            return
        ok, msg = delete_bug(self._selected_bug_id)
        self.msg.configure(text=msg, text_color=SUCCESS if ok else DANGER)
        if ok:
            self._clear(); self._load()

    def _clear(self):
        self._selected_bug_id = None
        for e in [self.bugid_entry, self.module_entry, self.desc_entry]:
            e.delete(0, "end")
        self.sev_var.set("High")
        self.status_var.set("Open")
        self.msg.configure(text="")
