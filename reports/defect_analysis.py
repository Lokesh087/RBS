# reports/defect_analysis.py
# TQM Analysis: Pareto Chart, Fishbone, PDCA, FMEA using Matplotlib + Pandas

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import os

from quality.bug_tracker import get_all_bugs, get_bug_summary_by_module
from quality.error_logger import get_all_logs

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "output")
os.makedirs(REPORTS_DIR, exist_ok=True)

# ── Colour palette ─────────────────────────────────────────────────────────────
C1 = "#E63946"   # red
C2 = "#457B9D"   # steel blue
C3 = "#2A9D8F"   # teal
C4 = "#E9C46A"   # gold
C5 = "#264653"   # dark
BG = "#1A1A2E"
FG = "#EAEAEA"


def _apply_dark_style(fig, axes):
    fig.patch.set_facecolor(BG)
    for ax in (axes if isinstance(axes, (list, tuple)) else [axes]):
        ax.set_facecolor("#16213E")
        ax.tick_params(colors=FG)
        ax.xaxis.label.set_color(FG)
        ax.yaxis.label.set_color(FG)
        ax.title.set_color(FG)
        for spine in ax.spines.values():
            spine.set_edgecolor("#444")


# ── 1. Pareto Chart ────────────────────────────────────────────────────────────

def generate_pareto_chart():
    """Generate Pareto (80/20) chart of bugs by module."""
    summary = get_bug_summary_by_module()
    if not summary:
        return None, "No bug data found."

    df = pd.DataFrame(list(summary.items()), columns=["Module", "Count"])
    df = df.sort_values("Count", ascending=False).reset_index(drop=True)
    df["CumulativePct"] = df["Count"].cumsum() / df["Count"].sum() * 100

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    bars = ax1.bar(df["Module"], df["Count"], color=[C1, C2, C3, C4, C5, "#A8DADC", "#F4A261"][:len(df)], zorder=3)
    ax2.plot(df["Module"], df["CumulativePct"], color=C4, marker="o", linewidth=2.5, markersize=8, zorder=4)
    ax2.axhline(80, color="#FF6B6B", linestyle="--", linewidth=1.5, label="80% line")

    ax1.set_ylabel("Number of Bugs", fontsize=12)
    ax2.set_ylabel("Cumulative %", fontsize=12)
    ax1.set_xlabel("Module", fontsize=12)
    ax1.set_title("🔍  Pareto Chart – Bug Distribution by Module\n(Q09: Reduce Bugs)", fontsize=14, fontweight="bold", pad=20)
    ax2.set_ylim(0, 115)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}%"))

    for bar, val in zip(bars, df["Count"]):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, str(val),
                 ha="center", va="bottom", color=FG, fontweight="bold")

    _apply_dark_style(fig, [ax1, ax2])
    ax2.tick_params(colors=FG)
    ax2.yaxis.label.set_color(FG)

    plt.tight_layout()
    path = os.path.join(REPORTS_DIR, "pareto_chart.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()
    return path, "Pareto chart generated."


# ── 2. Severity Distribution ───────────────────────────────────────────────────

def generate_severity_chart():
    """Pie chart of bugs by severity."""
    bugs = get_all_bugs()
    if not bugs:
        return None, "No bug data."

    df = pd.DataFrame(bugs)
    counts = df["severity"].value_counts()

    colors = {"High": C1, "Medium": C4, "Low": C3}
    clr = [colors.get(s, C2) for s in counts.index]

    fig, ax = plt.subplots(figsize=(7, 6))
    wedges, texts, autotexts = ax.pie(
        counts.values, labels=counts.index, autopct="%1.0f%%",
        colors=clr, startangle=140,
        wedgeprops={"edgecolor": BG, "linewidth": 2},
    )
    for t in texts + autotexts:
        t.set_color(FG)
    ax.set_title("Bug Severity Distribution", fontsize=14, fontweight="bold", color=FG, pad=15)
    _apply_dark_style(fig, ax)
    plt.tight_layout()
    path = os.path.join(REPORTS_DIR, "severity_chart.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()
    return path, "Severity chart generated."


# ── 3. Fishbone Diagram ────────────────────────────────────────────────────────

