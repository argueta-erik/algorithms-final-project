# main.py
# Entry point for the Campus App.
# Run:  python main.py
#
# The three nav buttons are intentionally non-functional stubs.
# Each team member should create their module file and import + wire it here.
#
# Module wiring guide (search for "TEAM HOOK" comments):
#   Campus Navigator  →  campus_navigator.py   →  open_campus_navigator()
#   Study Planner     →  study_planner.py       →  open_study_planner()
#   Notes Search      →  notes_search.py        →  open_notes_search()

import tkinter as tk
from util import (
    COLORS, FONTS, PADDING,
    configure_window, make_label, make_nav_button, make_separator,
)


# ---------------------------------------------------------------------------
# TEAM HOOK – Campus Navigator
# Uncomment and adjust once campus_navigator.py is ready.
# ---------------------------------------------------------------------------
# from campus_navigator import open_campus_navigator


# ---------------------------------------------------------------------------
# TEAM HOOK – Study Planner
# Uncomment and adjust once study_planner.py is ready.
# ---------------------------------------------------------------------------
from study_planner import open_study_planner


# ---------------------------------------------------------------------------
# TEAM HOOK – Notes Search
# Uncomment and adjust once notes_search.py is ready.
# ---------------------------------------------------------------------------
from notes_search import open_notes_search


# ---------------------------------------------------------------------------
# Stub callbacks (delete these once the real modules are connected)
# ---------------------------------------------------------------------------
def _stub(name: str):
    """Temporary no-op used while a module is not yet implemented."""
    # Replace with the real call once the module is wired in.
    pass


# ---------------------------------------------------------------------------
# Main menu view
# ---------------------------------------------------------------------------
class MainMenu(tk.Frame):
    """Root frame that renders the main menu."""

    def __init__(self, master: tk.Tk):
        super().__init__(master, bg=COLORS["bg_dark"])
        self.master = master
        self._build()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    def _build(self):
        self.pack(fill="both", expand=True)

        # ── top bar ────────────────────────────────────────────────────
        top_bar = tk.Frame(self, bg=COLORS["bg_panel"], height=56)
        top_bar.pack(fill="x", side="top")
        top_bar.pack_propagate(False)


        # ── hero section ───────────────────────────────────────────────
        hero = tk.Frame(self, bg=COLORS["bg_dark"])
        hero.pack(pady=(52, 0))

        make_label(
            hero,
            text="Welcome to CampusApp",
            style="title",
            fg=COLORS["text_primary"],
        ).pack()

        make_label(
            hero,
            text="Select a module to get started",
            style="subtitle",
            fg=COLORS["text_secondary"],
        ).pack(pady=(6, 0))

        # ── separator ──────────────────────────────────────────────────
        sep = make_separator(self)
        sep.pack(fill="x", padx=PADDING["window"] * 3, pady=36)

        # ── navigation buttons ─────────────────────────────────────────
        nav_frame = tk.Frame(self, bg=COLORS["bg_dark"])
        nav_frame.pack()

        buttons = [
            ("Campus Navigator",  lambda: _stub("campus_navigator")),
            ("Study Planner",      lambda: open_study_planner(self.master)),
            ("Notes Search",       lambda: open_notes_search(self.master)),
        ]

        for label, cmd in buttons:
            btn = make_nav_button(nav_frame, text=label, command=cmd, width=26)
            btn.pack(pady=10)

       


# ---------------------------------------------------------------------------
# App entry point
# ---------------------------------------------------------------------------
def main():
    root = tk.Tk()
    configure_window(root, title="CampusApp", width=720, height=520)
    MainMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
