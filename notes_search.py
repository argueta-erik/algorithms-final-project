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

# =========================================
# SEARCH ALGORITHMS
# ========================================

# DISCLAIMER: The search algorithms provided by Dr. Shah were used. 
# Time was taken to develop a firm understanding before use in the project.

# ========================================
# NAIVE SEARCH
# ========================================
def naive_search(text, pattern):
    # Using Dr. Shah's Lecture Code for reference
    matches = []
    comparisons = 0
    n = len(text)
    m = len(pattern)

    if m == 0 or m > n:
        return matches, comparisons

    for i in range(n - m + 1):
        found = True
        for j in range(m):
            comparisons += 1
            if text[i + j] != pattern[j]:
                found = False
                break
        if found:
            matches.append(i)
    return matches, comparisons


# ========================================
# RABIN-KARP SEARCH
# ========================================

def rabin_karp_search(text, pattern):
    matches = []
    comparisons = 0
    n = len(text)
    m = len(pattern)

    if m == 0 or m > n:
        return matches, comparisons

    d = 256
    q = 101
    pattern_hash = 0
    window_hash = 0

    h = 1

    for _ in range(m - 1):
        h = (h * d) % q
    for i in range(m):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % q
        window_hash  = (d * window_hash  + ord(text[i]))    % q

    for i in range(n - m + 1):
        comparisons += 1
        if pattern_hash == window_hash:
            if text[i:i + m] == pattern:   # verify (spurious-hit guard)
                matches.append(i)
        if i < n - m:
            window_hash = (d * (window_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            if window_hash < 0:
                window_hash += q

    return matches, comparisons

# ========================================
# KMP ALGORITHM
# ========================================

def build_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text: str, pattern: str):
    matches = []
    comparisons = 0
    if not pattern:
        return matches, comparisons

    lps = build_lps(pattern)
    i = 0
    j = 0
    n = len(text)
    m = len(pattern)

    while i < n:
        comparisons += 1
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches, comparisons




def open_module_template(master: tk.Tk) -> None:
    """Open this module in a new Toplevel window."""

    win = tk.Toplevel(master)
    configure_window(win, title="Module Name", width=800, height=560)

    # ── header bar ────────────────────────────────────────────────────────────
    header = tk.Frame(win, bg=COLORS["bg_panel"], height=52)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="  Module Name",
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
