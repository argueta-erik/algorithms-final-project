# util.py
# Shared theme constants and utility helpers for the Campus App.
# All modules should import from here to stay visually consistent.

import tkinter as tk


# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
COLORS = {
    "bg_dark":      "#1E1E1E",   # main window background
    "bg_panel":     "#2A2A2A",   # card / panel background
    "bg_hover":     "#2F3F2F",   # button hover state
    "accent":       "#4CAF50",   # primary green accent
    "accent_dark":  "#388E3C",   # darker green (pressed state)
    "accent_light": "#81C784",   # lighter green (highlights)
    "text_primary": "#F0F0F0",   # main text
    "text_secondary":"#9E9E9E",  # muted / caption text
    "border":       "#3A3A3A",   # subtle borders
    "separator":    "#333333",   # dividers
}

# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
FONTS = {
    "title":    ("Helvetica", 28, "bold"),
    "subtitle": ("Helvetica", 13),
    "button":   ("Helvetica", 12, "bold"),
    "body":     ("Helvetica", 11),
    "caption":  ("Helvetica", 9),
}

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
PADDING = {
    "window":  20,
    "section": 16,
    "element": 8,
}

BUTTON_STYLE = {
    "font":              FONTS["button"],
    "bg":                COLORS["accent"],
    "fg":                COLORS["bg_dark"],
    "activebackground":  COLORS["accent_dark"],
    "activeforeground":  COLORS["text_primary"],
    "relief":            "flat",
    "cursor":            "hand2",
    "bd":                0,
    "padx":              24,
    "pady":              14,
}


# ---------------------------------------------------------------------------
# Helper: apply global window defaults
# ---------------------------------------------------------------------------
def configure_window(root: tk.Tk | tk.Toplevel, title: str,
                     width: int = 900, height: int = 600) -> None:
    """Centre the window on screen and apply theme defaults."""
    root.title(title)
    root.configure(bg=COLORS["bg_dark"])
    root.resizable(True, True)

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.minsize(640, 480)


# ---------------------------------------------------------------------------
# Helper: themed label
# ---------------------------------------------------------------------------
def make_label(parent, text: str, style: str = "body", **kw) -> tk.Label:
    """Return a Label pre-styled with the app theme."""
    defaults = {
        "bg":   COLORS["bg_dark"],
        "fg":   COLORS["text_primary"],
        "font": FONTS.get(style, FONTS["body"]),
    }
    defaults.update(kw)
    return tk.Label(parent, text=text, **defaults)


# ---------------------------------------------------------------------------
# Helper: themed nav button with hover effect
# ---------------------------------------------------------------------------
def make_nav_button(parent, text: str, command=None, **kw) -> tk.Button:
    """Return a large themed navigation button."""
    style = {**BUTTON_STYLE, **kw}
    if command:
        style["command"] = command

    btn = tk.Button(parent, text=text, **style)

    def on_enter(_):
        btn.config(bg=COLORS["bg_hover"], fg=COLORS["accent_light"])

    def on_leave(_):
        btn.config(bg=COLORS["accent"], fg=COLORS["bg_dark"])

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


# ---------------------------------------------------------------------------
# Helper: horizontal separator
# ---------------------------------------------------------------------------
def make_separator(parent) -> tk.Frame:
    return tk.Frame(parent, bg=COLORS["separator"], height=1)
