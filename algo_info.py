# algo_info.py
# ─────────────────────────────────────────────────────────────────────────────
# CAMPUS APP – Algorithm Info Module
# Displays time/space complexity tables for each campus app module.
# ─────────────────────────────────────────────────────────────────────────────

import tkinter as tk
from util import COLORS, FONTS, PADDING, configure_window, make_label


# ══════════════════════════════════════════════════════════════════════════════
#  DATA: algorithm complexity tables per module
# ══════════════════════════════════════════════════════════════════════════════

MODULE_DATA = {
    "Campus Navigator": {
        "description": "Graph traversal and pathfinding algorithms used to navigate campus locations.",
        "columns": ["Algorithm", "Best Case", "Average Case", "Worst Case", "Space"],
        "rows": [
            ["BFS",                   "O(1)",        "O(V + E)",    "O(V + E)",    "O(V)"],
            ["DFS",                   "O(1)",        "O(V + E)",    "O(V + E)",    "O(V)"],
            ["Dijkstra Shortest Path","O((V+E) log V)","O((V+E) log V)","O((V+E) log V)","O(V)"],
            ["Prim's MST",            "O(E log V)",  "O(E log V)",  "O(E log V)",  "O(V)"],
        ],
        "notes": [
            "V = number of vertices (locations),  E = number of edges (paths).",
            "BFS guarantees shortest path on unweighted graphs.",
            "Dijkstra requires non-negative edge weights.",
            "Prim's MST builds a minimum spanning tree, not a shortest path.",
        ],
    },
    "Study Planner": {
        "description": "Scheduling and optimization algorithms for managing tasks and time.",
        "columns": ["Algorithm", "Best Case", "Average Case", "Worst Case", "Space"],
        "rows": [
            ["Greedy Scheduling", "O(n log n)", "O(n log n)", "O(n log n)", "O(n)"],
            ["DP 0/1 Knapsack",   "O(n·W)",     "O(n·W)",     "O(n·W)",     "O(n·W)"],
        ],
        "notes": [
            "n = number of tasks/items,  W = capacity (weight/time budget).",
            "Greedy Scheduling sorts tasks by deadline or finish time.",
            "DP Knapsack finds the optimal subset but requires pseudo-polynomial time.",
            "Greedy does NOT always yield the global optimum; DP does.",
        ],
    },
    "Notes Search": {
        "description": "String searching algorithms that scan document content for a pattern.",
        "columns": ["Algorithm", "Best Case", "Average Case", "Worst Case", "Space"],
        "rows": [
            ["Naive String Search", "O(n)",     "O(n·m)",  "O(n·m)",  "O(1)"],
            ["KMP",                 "O(n)",     "O(n + m)","O(n + m)","O(m)"],
            ["Rabin-Karp",          "O(n + m)", "O(n + m)","O(n·m)",  "O(1)"],
        ],
        "notes": [
            "n = length of text,  m = length of pattern.",
            "Naive worst case occurs with highly repetitive patterns (e.g. 'aaa…ab' in 'aaa…a').",
            "KMP preprocesses the pattern into an LPS table to skip redundant comparisons.",
            "Rabin-Karp worst case occurs when many hash collisions happen (spurious hits).",
        ],
    },
}


# ══════════════════════════════════════════════════════════════════════════════
#  COLOURS & STYLE CONSTANTS (extended from util theme)
# ══════════════════════════════════════════════════════════════════════════════

# Column header background per module (accent tints)
MODULE_ACCENT = {
    "Campus Navigator": "#1a6b8a",
    "Study Planner":    "#5a3e8a",
    "Notes Search":     "#8a5a1a",
}

ROW_EVEN = "#1e2329"
ROW_ODD  = "#242a32"
HEADER_FG = "#ffffff"
CELL_FG   = "#d0d8e8"
NOTE_FG   = "#7a8899"

FONT_TABLE_HEADER = ("TkFixedFont", 9, "bold")
FONT_TABLE_CELL   = ("TkFixedFont", 9)
FONT_NOTE         = ("TkDefaultFont", 8)


# ══════════════════════════════════════════════════════════════════════════════
#  UI BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def open_algo_info(master: tk.Tk) -> None:
    """Open the Algorithm Info module in a new Toplevel window."""

    win = tk.Toplevel(master)
    configure_window(win, title="Algorithm Info", width=860, height=620)

    # ── Header bar ────────────────────────────────────────────────────────────
    header = tk.Frame(win, bg=COLORS["bg_panel"], height=52)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header, text="  Algorithm Info",
        font=FONTS["subtitle"], bg=COLORS["bg_panel"],
        fg=COLORS["accent"], anchor="w",
    ).pack(side="left", padx=PADDING["section"], fill="y")

    tk.Button(
        header, text="← Back",
        font=FONTS["caption"], bg=COLORS["bg_panel"],
        fg=COLORS["text_secondary"], activebackground=COLORS["bg_panel"],
        activeforeground=COLORS["accent"], relief="flat", bd=0,
        cursor="hand2", command=win.destroy,
    ).pack(side="right", padx=PADDING["section"])

    # ── Body ──────────────────────────────────────────────────────────────────
    body = tk.Frame(win, bg=COLORS["bg_dark"])
    body.pack(fill="both", expand=True)

    # ── Left: module selector ─────────────────────────────────────────────────
    sidebar = tk.Frame(body, bg=COLORS["bg_panel"], width=220)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    tk.Label(
        sidebar, text="SELECT MODULE",
        font=FONTS["caption"], bg=COLORS["bg_panel"],
        fg=COLORS["text_secondary"], anchor="w",
    ).pack(fill="x", padx=14, pady=(18, 6))

    # ── Right: content area ───────────────────────────────────────────────────
    right = tk.Frame(body, bg=COLORS["bg_dark"])
    right.pack(side="left", fill="both", expand=True)

    # Placeholder shown before a module is selected
    placeholder_frame = tk.Frame(right, bg=COLORS["bg_dark"])
    placeholder_frame.pack(fill="both", expand=True)
    tk.Label(
        placeholder_frame,
        text="← Choose a module to view\nits algorithm complexities.",
        font=FONTS["subtitle"], bg=COLORS["bg_dark"],
        fg=COLORS["text_secondary"], justify="center",
    ).pack(expand=True)

    # Will hold the currently displayed detail frame
    _current = {"frame": placeholder_frame}

    def _show_module(module_name: str, btn_ref):
        """Render the complexity table for the selected module."""
        # Highlight selected sidebar button
        for b in sidebar_buttons:
            b.config(
                bg=COLORS["bg_panel"],
                fg=COLORS["text_primary"],
                relief="flat",
            )
        btn_ref.config(
            bg=COLORS["bg_dark"],
            fg=COLORS["accent"],
            relief="flat",
        )

        # Destroy previous content
        _current["frame"].destroy()

        data = MODULE_DATA[module_name]
        accent = MODULE_ACCENT[module_name]

        detail = tk.Frame(right, bg=COLORS["bg_dark"])
        detail.pack(fill="both", expand=True,
                    padx=PADDING["window"], pady=PADDING["window"])
        _current["frame"] = detail

        # Module title + description
        tk.Label(
            detail, text=module_name,
            font=FONTS["subtitle"], bg=COLORS["bg_dark"],
            fg=COLORS["text_primary"], anchor="w",
        ).pack(fill="x", pady=(0, 2))

        tk.Label(
            detail, text=data["description"],
            font=FONTS["caption"], bg=COLORS["bg_dark"],
            fg=COLORS["text_secondary"], anchor="w", wraplength=580, justify="left",
        ).pack(fill="x", pady=(0, 14))

        # ── Complexity table ──────────────────────────────────────────────────
        table_frame = tk.Frame(detail, bg=COLORS["bg_dark"])
        table_frame.pack(fill="x")

        columns = data["columns"]
        col_widths = [22, 16, 16, 16, 10]  # chars approx

        def _cell(parent, text, row, col, is_header=False):
            bg = accent if is_header else (ROW_EVEN if row % 2 == 0 else ROW_ODD)
            fg = HEADER_FG if is_header else CELL_FG
            font = FONT_TABLE_HEADER if is_header else FONT_TABLE_CELL
            anchor = "w" if col == 0 else "center"

            lbl = tk.Label(
                parent, text=text,
                font=font, bg=bg, fg=fg,
                anchor=anchor, padx=10, pady=7,
                width=col_widths[col],
            )
            lbl.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

        # Header row
        for c, col_name in enumerate(columns):
            _cell(table_frame, col_name, 0, c, is_header=True)

        # Data rows
        for r, row_data in enumerate(data["rows"], start=1):
            for c, cell_val in enumerate(row_data):
                _cell(table_frame, cell_val, r, c)

        # Make first column slightly wider
        table_frame.columnconfigure(0, weight=2)
        for c in range(1, len(columns)):
            table_frame.columnconfigure(c, weight=1)

        # ── Notes ─────────────────────────────────────────────────────────────
        notes_frame = tk.Frame(detail, bg=COLORS["bg_panel"])
        notes_frame.pack(fill="x", pady=(18, 0))

        tk.Label(
            notes_frame, text="  NOTES",
            font=("TkDefaultFont", 8, "bold"), bg=COLORS["bg_panel"],
            fg=COLORS["text_secondary"], anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 2))

        for note in data["notes"]:
            tk.Label(
                notes_frame, text=f"  •  {note}",
                font=FONT_NOTE, bg=COLORS["bg_panel"],
                fg=NOTE_FG, anchor="w", justify="left", wraplength=580,
            ).pack(fill="x", padx=10, pady=1)

        tk.Frame(notes_frame, bg=COLORS["bg_panel"], height=8).pack()

    # ── Build sidebar buttons ─────────────────────────────────────────────────
    sidebar_buttons = []
    for module_name in MODULE_DATA:
        btn = tk.Button(
            sidebar, text=module_name,
            font=FONTS["caption"],
            bg=COLORS["bg_panel"], fg=COLORS["text_primary"],
            activebackground=COLORS["bg_dark"],
            activeforeground=COLORS["accent"],
            relief="flat", bd=0, cursor="hand2",
            anchor="w", padx=16, pady=12,
        )
        btn.pack(fill="x", pady=2)
        sidebar_buttons.append(btn)

    # Bind each button after all are created (so btn_ref closure is correct)
    for btn, module_name in zip(sidebar_buttons, MODULE_DATA):
        btn.config(command=lambda n=module_name, b=btn: _show_module(n, b))

    # ── Divider line between sidebar and content ──────────────────────────────
    tk.Frame(body, bg=COLORS["bg_panel"], width=1).place(
        in_=sidebar, relx=1.0, rely=0, relheight=1.0
    )
