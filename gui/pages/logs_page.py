# gui/pages/logs_page.py – Error Logs Viewer (Q09 Feature 5)
import customtkinter as ctk
from gui.theme import *
from database.db import get_connection
from quality.error_logger import log_error


def _get_all_logs() -> list[dict]:
    try:
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM error_logs ORDER BY timestamp DESC LIMIT 200"
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        log_error("LogsPage", "Failed to fetch logs", str(e))
        return []


class LogsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG_DARK)
        self._build()
        self._load()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=30, pady=(25, 10))
        ctk.CTkLabel(hdr, text="📄  Error Logs", font=FONT_H1,
                     text_color=TEXT_PRI).pack(side="left")
        badge = ctk.CTkLabel(hdr, text="  Q09 Feature 5 – Error Logging  ",
                             font=FONT_SMALL, text_color="white",
                             fg_color="#7C3AED", corner_radius=8)
        badge.pack(side="left", padx=12)
        ctk.CTkButton(hdr, text="⟳ Refresh", width=90, height=32,
                      font=FONT_SMALL, fg_color=ACCENT2, hover_color="#2563EB",
                      command=self._load).pack(side="right")

        # Filter strip
        filter_row = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=10,
                                  border_width=1, border_color=BORDER)
        filter_row.grid(row=0, column=0, sticky="ew", padx=30, pady=(80, 0))
        ctk.CTkLabel(filter_row, text="Filter by level:", font=FONT_BODY,
                     text_color=TEXT_SEC).pack(side="left", padx=12, pady=8)
        self.filter_var = ctk.StringVar(value="ALL")
        for level in ["ALL", "ERROR", "WARNING", "INFO"]:
            col = {"ERROR": DANGER, "WARNING": WARNING, "INFO": ACCENT2, "ALL": TEXT_SEC}[level]
            ctk.CTkButton(
                filter_row, text=level, width=80, height=30, font=FONT_SMALL,
                fg_color=col if level != "ALL" else "#374151",
                hover_color="#1F2937",
                command=lambda lv=level: self._filter(lv),
            ).pack(side="left", padx=4, pady=6)

        # Table frame
        tbl = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=14,
                           border_width=1, border_color=BORDER)
        tbl.grid(row=1, column=0, sticky="nsew", padx=30, pady=(60, 10))
        tbl.grid_rowconfigure(1, weight=1)
        tbl.grid_columnconfigure(0, weight=1)

        self.count_label = ctk.CTkLabel(tbl, text="", font=FONT_BODY, text_color=TEXT_SEC)
        self.count_label.grid(row=0, column=0, sticky="w", padx=16, pady=(10, 4))

        cols   = ["#",  "Timestamp",         "Level",   "Module",  "Message",              "Details"]
        widths = [40,   160,                  80,        100,       280,                    200]
        hrow   = ctk.CTkFrame(tbl, fg_color="#1C2128", corner_radius=6)
        hrow.grid(row=1, column=0, sticky="ew", padx=10)
        for c, (col, w) in enumerate(zip(cols, widths)):
            ctk.CTkLabel(hrow, text=col, font=FONT_H3, text_color=ACCENT,
                         width=w, anchor="w").grid(row=0, column=c, padx=8, pady=6, sticky="w")

        self.scroll = ctk.CTkScrollableFrame(tbl, fg_color="transparent")
        self.scroll.grid(row=2, column=0, sticky="nsew", padx=10, pady=6)

        # Log file path notice
        import os
        log_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs", "error.log"
        )
        ctk.CTkLabel(
            self,
            text=f"📁  File log: {log_path}",
            font=FONT_SMALL, text_color="#444",
        ).grid(row=2, column=0, sticky="w", padx=30, pady=(0, 10))

        self._all_logs: list[dict] = []

    def _load(self):
        self._all_logs = _get_all_logs()
        self._render(self._all_logs)

    def _filter(self, level: str):
        if level == "ALL":
            self._render(self._all_logs)
        else:
            self._render([l for l in self._all_logs if l["level"] == level])

    def _render(self, logs: list[dict]):
        for w in self.scroll.winfo_children():
            w.destroy()
        self.count_label.configure(text=f"Showing {len(logs)} entries (latest 200 max)")

        level_colors = {"ERROR": DANGER, "WARNING": WARNING, "INFO": ACCENT2}

        for i, log in enumerate(logs):
            bg = BG_CARD if i % 2 == 0 else "#1C2128"
            row = ctk.CTkFrame(self.scroll, fg_color=bg, corner_radius=6)
            row.pack(fill="x", pady=2)
            col = level_colors.get(log["level"], TEXT_SEC)
            vals   = [str(log["id"]), log["timestamp"][:19], log["level"],
                      log["module"], log["message"], log.get("details") or ""]
            widths = [40, 160, 80, 100, 280, 200]
            colors = [TEXT_SEC, TEXT_SEC, col, TEXT_PRI, TEXT_PRI, TEXT_SEC]
            for c, (v, w, clr) in enumerate(zip(vals, widths, colors)):
                ctk.CTkLabel(row, text=v[:60] + ("…" if len(v) > 60 else ""),
                             font=FONT_SMALL, text_color=clr,
                             width=w, anchor="w").grid(row=0, column=c,
                                                       padx=8, pady=5, sticky="w")
