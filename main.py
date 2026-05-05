import tkinter as tk
from util import (
    COLORS, FONTS, PADDING,
    configure_window, make_label, make_nav_button, make_separator,
)

import campus_navigator as campus_navigator
from study_planner import open_study_planner
from notes_search import open_notes_search
from algo_info import open_algo_info


class MainMenu(tk.Frame):
    """Root frame that renders the main menu."""

    def __init__(self, master: tk.Tk):
        super().__init__(master, bg=COLORS["bg_dark"])
        self.master = master
        self._build()

    def _build(self):
        self.pack(fill="both", expand=True)

        top_bar = tk.Frame(self, bg=COLORS["bg_panel"], height=56)
        top_bar.pack(fill="x", side="top")
        top_bar.pack_propagate(False)

        hero = tk.Frame(self, bg=COLORS["bg_dark"])
        hero.pack(pady=(52, 0))

        make_label(
            hero,
            text="Welcome to TitanCampus Assistant",
            style="title",
            fg=COLORS["text_primary"],
        ).pack()

        make_label(
            hero,
            text="Select a module to get started",
            style="subtitle",
            fg=COLORS["text_secondary"],
        ).pack(pady=(6, 0))

        sep = make_separator(self)
        sep.pack(fill="x", padx=PADDING["window"] * 3, pady=36)

        nav_frame = tk.Frame(self, bg=COLORS["bg_dark"])
        nav_frame.pack()

        buttons = [
            ("Campus Navigator", lambda: campus_navigator.open_campus_navigator(self.master)),
            ("Study Planner",    lambda: open_study_planner(self.master)),
            ("Notes Search",     lambda: open_notes_search(self.master)),
            ("Algorithm Info",   lambda: open_algo_info(self.master)),
        ]

        for label, cmd in buttons:
            btn = make_nav_button(nav_frame, text=label, command=cmd, width=26)
            btn.pack(pady=10)


def main():
    root = tk.Tk()
    configure_window(root, title="CampusApp", width=720, height=520)
    MainMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
