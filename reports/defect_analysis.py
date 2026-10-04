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

def generate_fishbone_diagram():
    """Draw a Fishbone (Ishikawa) diagram for 'Billing Errors'."""
    fig, ax = plt.subplots(figsize=(14, 8))
    _apply_dark_style(fig, ax)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    # Spine
    ax.annotate("", xy=(13, 4), xytext=(1, 4),
                 arrowprops=dict(arrowstyle="-|>", color=C1, lw=2.5))
    ax.text(13.1, 4, "BILLING\nERRORS", fontsize=11, color=C1,
            fontweight="bold", va="center")

    categories = {
        "People\n(2 o'clock)": {
            "pos": (9.5, 6.5), "dir": "down",
            "causes": ["Wrong data entry", "Lack of training", "Inattention"],
        },
        "Process\n(10 o'clock)": {
            "pos": (4.5, 6.5), "dir": "down",
            "causes": ["No validation step", "Poor workflow", "Missing sign-off"],
        },
        "Software\n(4 o'clock)": {
            "pos": (9.5, 1.5), "dir": "up",
            "causes": ["Calculation bug", "Missing exception", "No unit tests"],
        },
        "Infrastructure\n(8 o'clock)": {
            "pos": (4.5, 1.5), "dir": "up",
            "causes": ["DB failure", "Concurrent writes", "No backup"],
        },
    }

    colors_cat = [C2, C3, C4, "#A8DADC"]
    for (cat_label, info), col in zip(categories.items(), colors_cat):
        px, py = info["pos"]
        # Branch line to spine
        ax.annotate("", xy=(px if px > 7 else px, 4),
                     xytext=(px, py),
                     arrowprops=dict(arrowstyle="-", color=col, lw=2))
        ax.text(px, py + (0.3 if info["dir"] == "down" else -0.3),
                cat_label, fontsize=9, color=col, fontweight="bold",
                ha="center", va="bottom" if info["dir"] == "down" else "top")

        for i, cause in enumerate(info["causes"], 1):
            cx = px + (i * 0.5 if px > 7 else -i * 0.5)
            cy = py - (i * 0.4) if info["dir"] == "down" else py + (i * 0.4)
            mid_y = 4 + (py - 4) * (1 - i * 0.25)
            ax.plot([cx, px], [cy, py], color=col, lw=1, alpha=0.6)
            ax.text(cx, cy, f"• {cause}", fontsize=7.5, color=FG, va="center")

    ax.set_title("🐟  Fishbone (Ishikawa) Diagram – Root Cause Analysis of Billing Errors",
                 fontsize=13, fontweight="bold", color=FG, pad=15)
    plt.tight_layout()
    path = os.path.join(REPORTS_DIR, "fishbone_diagram.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()
    return path, "Fishbone diagram generated."


# ── 4. PDCA Chart ─────────────────────────────────────────────────────────────

def generate_pdca_chart():
    """Visual PDCA cycle + before/after defect comparison."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    _apply_dark_style(fig, [ax1, ax2])

    # PDCA wheel
    phases = ["PLAN", "DO", "CHECK", "ACT"]
    descriptions = [
        "Identify frequent\nbilling & validation\ndefects",
        "Implement strict\nvalidation, exception\nhandling, unit tests",
        "Before: 67 defects\nAfter: 18 defects\n(73% reduction)",
        "Standardize improved\nvalidation & testing\nprocess (Kaizen)",
    ]
    colors_pdca = [C2, C3, C1, C4]
    angles = np.linspace(0, 2 * np.pi, 5)[:-1] + np.pi / 4

    for i, (phase, desc, col, angle) in enumerate(zip(phases, descriptions, colors_pdca, angles)):
        x, y = np.cos(angle) * 0.6, np.sin(angle) * 0.6
        circle = plt.Circle((x, y), 0.32, color=col, zorder=3)
        ax1.add_patch(circle)
        ax1.text(x, y + 0.06, phase, ha="center", va="center",
                 fontsize=11, fontweight="bold", color="white", zorder=4)
        ax1.text(x, y - 0.13, desc, ha="center", va="top",
                 fontsize=6.5, color="white", zorder=4)

    # Arrows between phases
    for i in range(4):
        a1, a2 = angles[i], angles[(i + 1) % 4]
        x1, y1 = np.cos(a1) * 0.95, np.sin(a1) * 0.95
        x2, y2 = np.cos(a2) * 0.95, np.sin(a2) * 0.95
        ax1.annotate("", xy=(x2, y2), xytext=(x1, y1),
                     arrowprops=dict(arrowstyle="-|>", color=FG, lw=1.5))

    ax1.set_xlim(-1.2, 1.2)
    ax1.set_ylim(-1.2, 1.2)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_title("PDCA Cycle – Continuous Improvement", fontsize=12, color=FG, fontweight="bold", pad=10)

    # Before/After bar chart
    stages = ["Before Q09", "After Q09"]
    defects = [67, 18]
    bars = ax2.bar(stages, defects, color=[C1, C3], width=0.4, zorder=3)
    for bar, val in zip(bars, defects):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 f"{val} defects", ha="center", va="bottom", color=FG, fontweight="bold")
    ax2.set_ylabel("Number of Defects", color=FG)
    ax2.set_title("Before vs. After Q09 Implementation\n(73% Defect Reduction)", fontsize=12, color=FG, fontweight="bold", pad=10)
    ax2.set_ylim(0, 80)
    ax2.grid(axis="y", color="#333", linestyle="--", alpha=0.7)

    fig.suptitle("📊  TQM – PDCA Analysis for Q09: Reduce Bugs", fontsize=14, color=FG, fontweight="bold", y=1.01)
    plt.tight_layout()
    path = os.path.join(REPORTS_DIR, "pdca_chart.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()
    return path, "PDCA chart generated."


# ── 5. FMEA Table ─────────────────────────────────────────────────────────────

def generate_fmea_chart():
    """Bar chart of FMEA Risk Priority Numbers."""
    fmea_data = {
        "Failure Mode":  ["Wrong bill total", "Negative quantity", "DB failure", "Invalid phone", "Empty bill generated"],
        "Severity (S)":  [9, 7, 8, 5, 8],
        "Occurrence (O)":[4, 5, 3, 6, 3],
        "Detection (D)": [4, 3, 5, 2, 4],
    }
    df = pd.DataFrame(fmea_data)
    df["RPN"] = df["Severity (S)"] * df["Occurrence (O)"] * df["Detection (D)"]
    df = df.sort_values("RPN", ascending=False)

    fig, ax = plt.subplots(figsize=(11, 6))
    _apply_dark_style(fig, ax)

    clrs = [C1 if r > 100 else C4 if r > 60 else C3 for r in df["RPN"]]
    bars = ax.barh(df["Failure Mode"], df["RPN"], color=clrs, zorder=3)
    for bar, val in zip(bars, df["RPN"]):
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2,
                f"RPN={val}", va="center", color=FG, fontsize=9)

    ax.axvline(100, color="#FF6B6B", linestyle="--", linewidth=1.5, label="Critical threshold (RPN=100)")
    ax.set_xlabel("Risk Priority Number (RPN = S × O × D)", color=FG, fontsize=11)
    ax.set_title("⚠️  FMEA – Risk Priority Analysis\n(Q09: Reduce Bugs)", fontsize=13, color=FG, fontweight="bold", pad=15)
    ax.legend(facecolor="#222", labelcolor=FG)
    ax.grid(axis="x", color="#333", linestyle="--", alpha=0.7)
    ax.invert_yaxis()

    high = mpatches.Patch(color=C1, label="High Risk (RPN > 100)")
    med  = mpatches.Patch(color=C4, label="Medium Risk")
    low  = mpatches.Patch(color=C3, label="Low Risk")
    ax.legend(handles=[high, med, low], facecolor="#222", labelcolor=FG, loc="lower right")

    plt.tight_layout()
    path = os.path.join(REPORTS_DIR, "fmea_chart.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()
    return path, "FMEA chart generated."
