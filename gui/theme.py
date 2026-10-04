# gui/theme.py – Shared design tokens for the entire GUI

# Colour palette
BG_DARK    = "#0D1117"
BG_CARD    = "#161B22"
BG_SIDEBAR = "#0D1117"
ACCENT     = "#F97316"   # Orange
ACCENT2    = "#3B82F6"   # Blue
SUCCESS    = "#22C55E"
WARNING    = "#EAB308"
DANGER     = "#EF4444"
TEXT_PRI   = "#F0F6FC"
TEXT_SEC   = "#8B949E"
BORDER     = "#30363D"

# Font sizes
FONT_H1    = ("Segoe UI", 22, "bold")
FONT_H2    = ("Segoe UI", 16, "bold")
FONT_H3    = ("Segoe UI", 13, "bold")
FONT_BODY  = ("Segoe UI", 12)
FONT_SMALL = ("Segoe UI", 10)
FONT_MONO  = ("Consolas", 11)

# CTk widget colours
ENTRY_FG   = "#1C2128"
ENTRY_BORDER = "#3B82F6"
BTN_PRIMARY  = "#F97316"
BTN_HOVER    = "#EA580C"

# Sidebar nav items: (label, icon, page_key)
NAV_ITEMS = [
    ("Dashboard",     "📊", "dashboard"),
    ("Menu",          "🍽", "menu"),
    ("Customers",     "👥", "customers"),
    ("Orders",        "📋", "orders"),
    ("Billing",       "🧾", "billing"),
    ("Bug Tracker",   "🐛", "bugs"),
    ("TQM Reports",   "📈", "reports"),
    ("Error Logs",    "📄", "logs"),
]
