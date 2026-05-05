# notes_search.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time
import os

try:
    import fitz  # PyMuPDF
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    from docx import Document as DocxDocument
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False

from util import COLORS, FONTS, PADDING, configure_window, make_label


# ==============================================================================
#  SEARCH ALGORITHMS
# ==============================================================================

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

def kmp_search(text, pattern):
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



# ========================================
#  DOCUMENT READER
# ========================================

def read_document(filepath: str) -> str:
    """Extract plain text from .txt, .pdf, or .docx files."""
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".txt":
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    if ext == ".pdf":
        if not PDF_SUPPORT:
            raise RuntimeError(
                "PDF support requires PyMuPDF.\n"
                "Install it with:  pip install pymupdf"
            )
        doc = fitz.open(filepath)
        return "\n".join(page.get_text() for page in doc)

    if ext in (".docx", ".doc"):
        if not DOCX_SUPPORT:
            raise RuntimeError(
                "DOCX support requires python-docx.\n"
                "Install it with:  pip install python-docx"
            )
        doc = DocxDocument(filepath)
        return "\n".join(p.text for p in doc.paragraphs)

    raise ValueError(f"Unsupported file type: {ext}")


# ========================================
#  MAIN MODULE WINDOW
# ========================================

def open_notes_search(master: tk.Tk) -> None:
    """Open the Notes Search module in a new Toplevel window."""

    win = tk.Toplevel(master)
    configure_window(win, title="Notes Search", width=900, height=660)

    # ── State ─────────────────────────────────────────────────────────────────
    doc_text       = tk.StringVar(value="")
    doc_name_var   = tk.StringVar(value="No document loaded")
    status_var     = tk.StringVar(value="Upload a document to begin.")
    algo_var       = tk.StringVar(value="KMP")
    comparison_var = tk.BooleanVar(value=False)

    # ── Header bar ───────────────────────────────────────────────────────────
    header = tk.Frame(win, bg=COLORS["bg_panel"], height=52)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header, text="  Notes Search",
        font=FONTS["subtitle"], bg=COLORS["bg_panel"],
        fg=COLORS["accent"], anchor="w",
    ).pack(side="top", padx=PADDING["section"], fill="y")

    tk.Button(
        header, text="← Back",
        font=FONTS["caption"], bg=COLORS["bg_panel"],
        fg=COLORS["text_secondary"], activebackground=COLORS["bg_panel"],
        activeforeground=COLORS["accent"], relief="flat", bd=0,
        cursor="hand2", command=win.destroy,
    ).pack(side="left", padx=PADDING["section"])

    # ── Main content ──────────────────────────────────────────────────────────
    content = tk.Frame(win, bg=COLORS["bg_dark"])
    content.pack(fill="both", expand=True,
                 padx=PADDING["window"], pady=PADDING["window"])

    # ── Left panel: upload + controls ────────────────────────────────────────
    left = tk.Frame(content, bg=COLORS["bg_panel"], width=260)
    left.pack(side="left", fill="y", padx=(0, PADDING["section"]))
    left.pack_propagate(False)

    def _section_label(parent, text):
        tk.Label(
            parent, text=text,
            font=FONTS["caption"], bg=COLORS["bg_panel"],
            fg=COLORS["text_secondary"], anchor="w",
        ).pack(fill="x", padx=12, pady=(14, 2))

    # ── Upload area ───────────────────────────────────────────────────────────
    _section_label(left, "DOCUMENT")

    upload_frame = tk.Frame(left, bg=COLORS["bg_dark"], pady=18, padx=12)
    upload_frame.pack(fill="x", padx=12)

    tk.Label(
        upload_frame, text="📄",
        font=("TkDefaultFont", 28), bg=COLORS["bg_dark"],
        fg=COLORS["accent"],
    ).pack()

    tk.Label(
        upload_frame,
        textvariable=doc_name_var,
        font=FONTS["caption"], bg=COLORS["bg_dark"],
        fg=COLORS["text_secondary"], wraplength=200,
    ).pack(pady=(4, 8))

    def _upload_document():
        filetypes = [("Documents", "*.txt *.pdf *.docx"), ("All files", "*.*")]
        path = filedialog.askopenfilename(parent=win, filetypes=filetypes)
        if not path:
            return
        try:
            text = read_document(path)
            doc_text.set(text)
            doc_name_var.set(os.path.basename(path))
            status_var.set(f"Loaded {len(text):,} characters.  Ready to search.")
            _refresh_preview(text)
        except Exception as e:
            messagebox.showerror("Load Error", str(e), parent=win)

    tk.Button(
        upload_frame, text="Upload Document",
        font=FONTS["caption"], bg=COLORS["accent"],
        fg="#ffffff", activebackground=COLORS["accent"],
        relief="flat", bd=0, cursor="hand2", padx=10, pady=6,
        command=_upload_document,
    ).pack()

    # ── Algorithm selector ────────────────────────────────────────────────────
    _section_label(left, "ALGORITHM")

    algo_frame = tk.Frame(left, bg=COLORS["bg_panel"])
    algo_frame.pack(fill="x", padx=12)

    for algo in ("Naive", "KMP", "Rabin-Karp"):
        tk.Radiobutton(
            algo_frame, text=algo, variable=algo_var, value=algo,
            font=FONTS["caption"], bg=COLORS["bg_panel"],
            fg=COLORS["text_primary"], selectcolor=COLORS["bg_dark"],
            activebackground=COLORS["bg_panel"],
            activeforeground=COLORS["accent"],
        ).pack(anchor="w", pady=1)

    # ── Comparison mode ───────────────────────────────────────────────────────
    _section_label(left, "OPTIONS")

    tk.Checkbutton(
        left, text="Algorithm Comparison Mode",
        variable=comparison_var,
        font=FONTS["caption"], bg=COLORS["bg_panel"],
        fg=COLORS["text_primary"], selectcolor=COLORS["bg_dark"],
        activebackground=COLORS["bg_panel"],
        activeforeground=COLORS["accent"],
    ).pack(anchor="w", padx=12, pady=2)

    tk.Label(
        left,
        text="Runs all 3 algorithms and\ncompares speed & matches.",
        font=("TkDefaultFont", 8), bg=COLORS["bg_panel"],
        fg=COLORS["text_secondary"], justify="left",
    ).pack(anchor="w", padx=24)

    # ── Spacer + stats ────────────────────────────────────────────────────────
    tk.Frame(left, bg=COLORS["bg_panel"]).pack(expand=True, fill="both")

    stats_frame = tk.Frame(left, bg=COLORS["bg_dark"])
    stats_frame.pack(fill="x", padx=12, pady=12)

    stats_label = tk.Label(
        stats_frame, text="", font=("TkFixedFont", 8),
        bg=COLORS["bg_dark"], fg=COLORS["text_secondary"],
        justify="left", anchor="w", padx=8, pady=6,
    )
    stats_label.pack(fill="x")

    # ── Right panel: search + results ────────────────────────────────────────
    right = tk.Frame(content, bg=COLORS["bg_dark"])
    right.pack(side="left", fill="both", expand=True)

    # Search bar
    search_bar = tk.Frame(right, bg=COLORS["bg_panel"], pady=8, padx=10)
    search_bar.pack(fill="x")

    search_entry = tk.Entry(
        search_bar, font=FONTS["body"],
        bg=COLORS["bg_dark"], fg=COLORS["text_primary"],
        insertbackground=COLORS["accent"],
        relief="flat", bd=4,
    )
    search_entry.pack(side="left", fill="x", expand=True, ipady=4)
    search_entry.insert(0, "Search pattern…")
    search_entry.bind("<FocusIn>",  lambda e: _clear_placeholder(search_entry, "Search pattern…"))
    search_entry.bind("<FocusOut>", lambda e: _set_placeholder(search_entry, "Search pattern…"))
    search_entry.bind("<Return>",   lambda e: _run_search())

    def _clear_placeholder(widget, placeholder):
        if widget.get() == placeholder:
            widget.delete(0, tk.END)
            widget.config(fg=COLORS["text_primary"])

    def _set_placeholder(widget, placeholder):
        if not widget.get():
            widget.insert(0, placeholder)
            widget.config(fg=COLORS["text_secondary"])

    tk.Button(
        search_bar, text="Search",
        font=FONTS["caption"], bg=COLORS["accent"],
        fg="#ffffff", activebackground=COLORS["accent"],
        relief="flat", bd=0, cursor="hand2", padx=14, pady=5,
        command=lambda: _run_search(),
    ).pack(side="left", padx=(8, 0))

    # ── Document preview pane ─────────────────────────────────────────────────
    preview_label = tk.Label(
        right, text="DOCUMENT PREVIEW",
        font=FONTS["caption"], bg=COLORS["bg_dark"],
        fg=COLORS["text_secondary"], anchor="w",
    )
    preview_label.pack(fill="x", padx=8, pady=(10, 2))

    preview_frame = tk.Frame(right, bg=COLORS["bg_dark"])
    preview_frame.pack(fill="both", expand=True, padx=8)

    preview_scroll = tk.Scrollbar(preview_frame)
    preview_scroll.pack(side="right", fill="y")

    preview_text = tk.Text(
        preview_frame, font=("TkFixedFont", 9),
        bg=COLORS["bg_panel"], fg=COLORS["text_primary"],
        relief="flat", bd=0, wrap="word",
        yscrollcommand=preview_scroll.set,
        state="disabled",
    )
    preview_text.pack(fill="both", expand=True)
    preview_scroll.config(command=preview_text.yview)

    preview_text.tag_config("highlight", background="#f5a623", foreground="#000000")

    # ── Results / comparison pane ────────────────────────────────────────────
    results_label = tk.Label(
        right, text="RESULTS",
        font=FONTS["caption"], bg=COLORS["bg_dark"],
        fg=COLORS["text_secondary"], anchor="w",
    )
    results_label.pack(fill="x", padx=8, pady=(10, 2))

    results_frame = tk.Frame(right, bg=COLORS["bg_dark"], height=180)
    results_frame.pack(fill="x", padx=8, pady=(0, 8))
    results_frame.pack_propagate(False)

    results_scroll = tk.Scrollbar(results_frame)
    results_scroll.pack(side="right", fill="y")

    results_text = tk.Text(
        results_frame, font=("TkFixedFont", 9),
        bg=COLORS["bg_panel"], fg=COLORS["text_primary"],
        relief="flat", bd=0, wrap="word",
        yscrollcommand=results_scroll.set,
        state="disabled",
    )
    results_text.pack(fill="both", expand=True)
    results_scroll.config(command=results_text.yview)

    results_text.tag_config("header",  foreground=COLORS["accent"], font=("TkFixedFont", 9, "bold"))
    results_text.tag_config("winner",  foreground="#4caf50", font=("TkFixedFont", 9, "bold"))
    results_text.tag_config("match",   foreground="#f5a623")
    results_text.tag_config("muted",   foreground=COLORS["text_secondary"])

    # ── Status bar ────────────────────────────────────────────────────────────
    tk.Label(
        win, textvariable=status_var,
        font=("TkDefaultFont", 8), bg=COLORS["bg_panel"],
        fg=COLORS["text_secondary"], anchor="w", padx=10,
    ).pack(fill="x", side="bottom")

    # ── Helper: refresh document preview ─────────────────────────────────────
    def _refresh_preview(text: str):
        preview_text.config(state="normal")
        preview_text.delete("1.0", tk.END)
        preview_text.insert(tk.END, text[:8000])  # cap display for performance
        if len(text) > 8000:
            preview_text.insert(tk.END, "\n… (preview truncated)")
        preview_text.config(state="disabled")

    # ── Helper: write to results pane ────────────────────────────────────────
    def _write_results(segments):
        """segments: list of (text, tag_or_None)"""
        results_text.config(state="normal")
        results_text.delete("1.0", tk.END)
        for text_chunk, tag in segments:
            if tag:
                results_text.insert(tk.END, text_chunk, tag)
            else:
                results_text.insert(tk.END, text_chunk)
        results_text.config(state="disabled")

    # ── Helper: highlight matches in preview ─────────────────────────────────
    def _highlight_matches(text: str, pattern: str, matches: list):
        preview_text.config(state="normal")
        preview_text.tag_remove("highlight", "1.0", tk.END)
        m = len(pattern)
        preview_start = 0  # preview is first 8000 chars
        for idx in matches:
            if idx >= 8000:
                break
            start = f"1.0 + {idx - preview_start}c"
            end   = f"1.0 + {idx - preview_start + m}c"
            preview_text.tag_add("highlight", start, end)
        preview_text.config(state="disabled")

    # ── Core search runner ────────────────────────────────────────────────────
    def _run_search():
        text    = doc_text.get()
        pattern = search_entry.get().strip()

        if not text or text == "":
            messagebox.showwarning("No Document", "Please upload a document first.", parent=win)
            return
        if not pattern or pattern == "Search pattern…":
            messagebox.showwarning("Empty Pattern", "Please enter a search pattern.", parent=win)
            return

        if comparison_var.get():
            _run_comparison(text, pattern)
        else:
            _run_single(text, pattern)

    def _run_single(text: str, pattern: str):
        algo = algo_var.get()

        t0 = time.perf_counter()
        if algo == "Naive":
            matches, comparisons = naive_search(text, pattern)
        elif algo == "KMP":
            matches, comparisons = kmp_search(text, pattern)
        else:
            matches, comparisons = rabin_karp_search(text, pattern)
        elapsed = (time.perf_counter() - t0) * 1000  # ms

        count = len(matches)
        status_var.set(
            f"{algo} → {count} match{'es' if count != 1 else ''} "
            f"in {elapsed:.4f} ms  |  {comparisons:,} comparisons"
        )

        _highlight_matches(text, pattern, matches)

        # Build results output
        segs = [
            (f"Algorithm : {algo}\n", "header"),
            (f"Pattern   : \"{pattern}\"\n", None),
            (f"Matches   : {count}\n", None),
            (f"Time      : {elapsed:.4f} ms\n", None),
            (f"Comparisons: {comparisons:,}\n\n", None),
        ]

        if matches:
            segs.append(("Match indices (first 50):\n", "header"))
            preview_indices = matches[:50]
            for idx in preview_indices:
                ctx_start = max(0, idx - 20)
                ctx_end   = min(len(text), idx + len(pattern) + 20)
                ctx = text[ctx_start:ctx_end].replace("\n", " ")
                segs.append((f"  [{idx}]  …{ctx}…\n", "match"))
            if len(matches) > 50:
                segs.append((f"  … and {len(matches) - 50} more.\n", "muted"))
        else:
            segs.append(("No matches found.\n", "muted"))

        _write_results(segs)
        stats_label.config(
            text=f"Chars: {len(text):,}\nPattern len: {len(pattern)}\nMatches: {count}"
        )

    def _run_comparison(text: str, pattern: str):
        algorithms = [
            ("Naive",      naive_search),
            ("KMP",        kmp_search),
            ("Rabin-Karp", rabin_karp_search),
        ]
        results = []
        for name, fn in algorithms:
            t0 = time.perf_counter()
            matches, comparisons = fn(text, pattern)
            elapsed = (time.perf_counter() - t0) * 1000
            results.append({
                "name":        name,
                "matches":     matches,
                "count":       len(matches),
                "time_ms":     elapsed,
                "comparisons": comparisons,
            })

        fastest = min(results, key=lambda r: r["time_ms"])
        fewest  = min(results, key=lambda r: r["comparisons"])

        # Highlight matches from the fastest algorithm
        _highlight_matches(text, pattern, fastest["matches"])

        status_var.set(
            f"Comparison complete — fastest: {fastest['name']} "
            f"({fastest['time_ms']:.4f} ms)"
        )

        # Build comparison table
        col_w = 18
        segs = [
            ("━" * 62 + "\n", "header"),
            ("  ALGORITHM COMPARISON MODE\n", "header"),
            (f"  Pattern: \"{pattern}\"   |   Text: {len(text):,} chars\n", None),
            ("━" * 62 + "\n", "header"),
            (
                f"  {'Algorithm':<14} {'Matches':>8} {'Time (ms)':>12} {'Comparisons':>14}\n",
                "header"
            ),
            ("─" * 62 + "\n", "muted"),
        ]

        for r in results:
            is_fastest = r["name"] == fastest["name"]
            is_fewest  = r["name"] == fewest["name"]
            tag = "winner" if is_fastest else None
            badge = " ◀ fastest" if is_fastest else ("  ← fewest cmp" if is_fewest and not is_fastest else "")
            line = (
                f"  {r['name']:<14} {r['count']:>8,} "
                f"{r['time_ms']:>12.4f} {r['comparisons']:>14,}{badge}\n"
            )
            segs.append((line, tag))

        segs += [
            ("━" * 62 + "\n", "header"),
            ("\n  NOTES\n", "header"),
            ("  • Naive:      simple O(n·m) brute force\n", "muted"),
            ("  • KMP:        O(n+m), LPS-table preprocessing\n", "muted"),
            ("  • Rabin-Karp: O(n+m) average with rolling hash\n", "muted"),
            ("  Highlights in preview show matches from the fastest algorithm.\n", "muted"),
        ]

        _write_results(segs)

        stats_label.config(
            text=(
                f"Chars : {len(text):,}\n"
                f"Pattern: {len(pattern)}\n"
                f"Fastest: {fastest['name']}"
            )
        )