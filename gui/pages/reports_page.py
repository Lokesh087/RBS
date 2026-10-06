# gui/pages/reports_page.py – TQM Reports Page
import customtkinter as ctk
from gui.theme import *
import threading


class ReportsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG_DARK)
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=30, pady=(25, 10))
        ctk.CTkLabel(hdr, text="📈  TQM Quality Reports", font=FONT_H1,
                     text_color=TEXT_PRI).pack(side="left")
        badge = ctk.CTkLabel(hdr, text="  Q09 – Reduce Bugs  ",
                             font=FONT_SMALL, text_color="white",
                             fg_color=ACCENT, corner_radius=8)
        badge.pack(side="left", padx=12)

        # Content scroll
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)

        self.status_label = ctk.CTkLabel(self, text="", font=FONT_BODY,
                                         text_color=SUCCESS)
        self.status_label.grid(row=2, column=0, pady=(0, 12))

        # ── Chart cards ────────────────────────────────────────────────────
        charts = [
            {
                "title":   "📊 Pareto Chart – 80/20 Bug Analysis",
                "desc":    (
                    "Shows which modules contribute most to defects.\n"
                    "The 80/20 principle: 80% of bugs come from 20% of modules.\n"
                    "Helps prioritise where to invest quality improvement effort."
                ),
                "func":    "generate_pareto_chart",
                "color":   ACCENT,
                "tqm_tag": "Pareto Analysis",
            },
            {
                "title":   "🥧 Severity Distribution Chart",
                "desc":    (
                    "Pie chart breaking down bugs by severity (High/Medium/Low).\n"
                    "Used in defect density analysis and SQC reporting."
                ),
                "func":    "generate_severity_chart",
                "color":   ACCENT2,
                "tqm_tag": "SQC Analysis",
            },
            {
                "title":   "🐟 Fishbone (Ishikawa) Diagram",
                "desc":    (
                    "Root cause analysis of billing errors.\n"
                    "Categories: People, Process, Software Code, Infrastructure.\n"
                    "Visual tool to identify why defects occur at their source."
                ),
                "func":    "generate_fishbone_diagram",
                "color":   WARNING,
                "tqm_tag": "Root Cause Analysis",
            },
            {
                "title":   "🔄 PDCA Cycle Chart",
                "desc":    (
                    "Plan–Do–Check–Act continuous improvement cycle.\n"
                    "Before Q09: 67 defects  →  After Q09: 18 defects (73% reduction).\n"
                    "Demonstrates Kaizen / Continuous Improvement principle."
                ),
                "func":    "generate_pdca_chart",
                "color":   SUCCESS,
                "tqm_tag": "Continuous Improvement (Kaizen)",
            },
            {
                "title":   "⚠️ FMEA – Risk Priority Number Chart",
                "desc":    (
                    "Failure Mode & Effects Analysis.\n"
                    "RPN = Severity × Occurrence × Detection.\n"
                    "Identifies highest-risk failure modes to prioritise fixes."
                ),
                "func":    "generate_fmea_chart",
                "color":   DANGER,
                "tqm_tag": "FMEA / Risk Analysis",
            },
        ]

        for chart in charts:
            self._chart_card(scroll, chart)

        # SIPOC info card
        sipoc = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=14,
                             border_width=1, border_color=BORDER)
        sipoc.pack(fill="x", pady=8)
        ctk.CTkLabel(sipoc, text="📋  SIPOC Diagram",
                     font=FONT_H2, text_color=TEXT_PRI).pack(anchor="w", padx=20, pady=(16, 8))
        sipoc_text = (
            "Suppliers → Restaurant Staff / Admin\n"
            "Inputs    → Menu Items, Customer Data, Order Details\n"
            "Process   → Select Items → Validate → Calculate → Generate Bill → Store\n"
            "Outputs   → Accurate, GST-compliant Restaurant Bill\n"
            "Customers → Dine-in / Take-away Customers, Restaurant Staff"
        )
        ctk.CTkLabel(sipoc, text=sipoc_text, font=FONT_MONO,
                     text_color=TEXT_SEC, justify="left", anchor="w").pack(
            anchor="w", padx=20, pady=(0, 16))

        # CTQ card
        ctq = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=14,
                           border_width=1, border_color=BORDER)
        ctq.pack(fill="x", pady=8)
        ctk.CTkLabel(ctq, text="🎯  Critical to Quality (CTQ) Parameters",
                     font=FONT_H2, text_color=TEXT_PRI).pack(anchor="w", padx=20, pady=(16, 8))
        ctqs = [
            ("Billing Accuracy",  "Total must be mathematically correct (subtotal + 5% GST)",   SUCCESS),
            ("Input Accuracy",    "Invalid values (negative price, bad phone) must be rejected", ACCENT),
            ("Reliability",       "Application must not crash on any user input or DB error",    ACCENT2),
            ("Error Recovery",    "Every error must be handled gracefully with a friendly msg",  WARNING),
            ("Test Coverage",     "All critical modules must have passing pytest unit tests",    SUCCESS),
        ]
        for ctq_name, ctq_req, col in ctqs:
            row = ctk.CTkFrame(ctq, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=3)
            ctk.CTkLabel(row, text=f"• {ctq_name}", font=FONT_H3,
                         text_color=col, width=200, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=ctq_req, font=FONT_BODY,
                         text_color=TEXT_SEC, anchor="w").pack(side="left", padx=8)
        ctk.CTkFrame(ctq, height=1, fg_color="transparent").pack(pady=10)

    def _chart_card(self, parent, chart: dict):
        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=14,
                            border_width=1, border_color=chart["color"])
        card.pack(fill="x", pady=8)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=16)

        left = ctk.CTkFrame(inner, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(left, text=chart["title"], font=FONT_H2,
                     text_color=chart["color"]).pack(anchor="w")
        ctk.CTkLabel(left, text=f"TQM Tool: {chart['tqm_tag']}",
                     font=FONT_SMALL, text_color=TEXT_SEC).pack(anchor="w", pady=(2, 6))
        ctk.CTkLabel(left, text=chart["desc"], font=FONT_BODY,
                     text_color=TEXT_SEC, justify="left", anchor="w",
                     wraplength=600).pack(anchor="w")

        func_name = chart["func"]
        ctk.CTkButton(
            inner,
            text="▶ Generate Chart",
            width=160, height=42, font=FONT_H3,
            fg_color=chart["color"],
            hover_color=self._darken(chart["color"]),
            command=lambda fn=func_name: self._run_chart(fn),
        ).pack(side="right", padx=(20, 0))

    def _run_chart(self, func_name: str):
        self.status_label.configure(
            text=f"⏳ Generating {func_name.replace('generate_', '').replace('_', ' ')}...",
            text_color=WARNING,
        )
        self.update()

        def _worker():
            try:
                from reports.defect_analysis import (
                    generate_pareto_chart, generate_severity_chart,
                    generate_fishbone_diagram, generate_pdca_chart,
                    generate_fmea_chart,
                )
                fn_map = {
                    "generate_pareto_chart":    generate_pareto_chart,
                    "generate_severity_chart":  generate_severity_chart,
                    "generate_fishbone_diagram": generate_fishbone_diagram,
                    "generate_pdca_chart":      generate_pdca_chart,
                    "generate_fmea_chart":      generate_fmea_chart,
                }
                fn = fn_map.get(func_name)
                if fn:
                    path, msg = fn()
                    self.after(0, lambda: self.status_label.configure(
                        text=f"✅ {msg}" + (f" → {path}" if path else ""),
                        text_color=SUCCESS,
                    ))
            except Exception as e:
                self.after(0, lambda: self.status_label.configure(
                    text=f"❌ Error: {e}", text_color=DANGER,
                ))

        threading.Thread(target=_worker, daemon=True).start()

    @staticmethod
    def _darken(hex_color: str) -> str:
        """Return a slightly darker shade of a hex colour."""
        try:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            r, g, b = max(0, r - 30), max(0, g - 30), max(0, b - 30)
            return f"#{r:02X}{g:02X}{b:02X}"
        except Exception:
            return hex_color
