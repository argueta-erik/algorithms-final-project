# module_template.py
# ─────────────────────────────────────────────────────────────────────────────
# CAMPUS APP – Module Template
# ─────────────────────────────────────────────────────────────────────────────
# Instructions for your team:
#
#  1. Copy this file and rename it to match your module, e.g.:
#       campus_navigator.py  /  study_planner.py  /  notes_search.py
#
#  2. Implement your UI inside the open_<module>() function below.
#     It receives the root Tk window as `master` so you can open a
#     Toplevel window, replace the current frame, or do whatever fits best.
#
#  3. In main.py:
#       a. Uncomment the matching import line  (search "TEAM HOOK")
#       b. Replace the matching lambda: _stub(...) with your function call
#
#  4. All colours, fonts, and helpers live in util.py – use them!
# ─────────────────────────────────────────────────────────────────────────────

import tkinter as tk
from util import COLORS, FONTS, PADDING, configure_window, make_label, make_nav_button


def open_campus_navigator(master: tk.Tk) -> None:
    """Open this module in a new Toplevel window."""

    win = tk.Toplevel(master)
    configure_window(win, title="Module Name", width=800, height=560)

    # ── header bar ────────────────────────────────────────────────────────────
    header = tk.Frame(win, bg=COLORS["bg_panel"], height=52)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="  Campus Navigator",
        font=FONTS["subtitle"],
        bg=COLORS["bg_panel"],
        fg=COLORS["accent"],
        anchor="w",
    ).pack(side="left", padx=PADDING["section"], fill="y")

    back_btn = tk.Button(
        header,
        text="← Back",
        font=FONTS["caption"],
        bg=COLORS["bg_panel"],
        fg=COLORS["text_secondary"],
        activebackground=COLORS["bg_panel"],
        activeforeground=COLORS["accent"],
        relief="flat",
        bd=0,
        cursor="hand2",
        command=win.destroy,
    )
    back_btn.pack(side="right", padx=PADDING["section"])

    # ── content area ──────────────────────────────────────────────────────────
    content = tk.Frame(win, bg=COLORS["bg_dark"])
    content.pack(fill="both", expand=True, padx=PADDING["window"], pady=PADDING["window"])

    make_label(
        content,
        text="Your module UI goes here",
        style="title",
        fg=COLORS["text_secondary"],
    ).pack(expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    configure_window(root, title="CampusNavigator", width=720, height=520)
    open_campus_navigator(root)
    root.mainloop()