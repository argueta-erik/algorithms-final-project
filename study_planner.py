# study_planner.py
# ---------------------------------------------------------------------------
# CAMPUS APP – Study Planner Module
# ---------------------------------------------------------------------------
# Algorithms used:
#   1. Greedy Scheduler  – sorts tasks by value/time ratio, picks greedily
#   2. DP 0/1 Knapsack   – finds the optimal subset maximising total value
# ---------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox
from util import COLORS, FONTS, PADDING, configure_window, make_label


# ---------------------------------------------------------------------------
# algorithm 1 – Greedy Task Scheduler
# strategy: makes locally optimal choices, picking the best value/time ratio task that fits
# time complexity: O(n log n)  –  dominated by the sort step
# ---------------------------------------------------------------------------
def greedy_schedule(tasks: list[dict], available_time: int) -> tuple[list[dict], int, int]:
    # parameters: tasks = list of name, time, value. available_time = total minutes
    # returns: chosen tasks, total time used, total value

    # sort by value-per-minute ratio (highest first)
    sorted_tasks = sorted(tasks, key=lambda t: t["value"] / t["time"], reverse=True)

    chosen = []
    time_used = 0

    for task in sorted_tasks:
        if time_used + task["time"] <= available_time:
            chosen.append(task)
            time_used += task["time"]

    total_value = sum(t["value"] for t in chosen)
    return chosen, time_used, total_value


# ---------------------------------------------------------------------------
# algorithm 2 – DP 0/1 Knapsack
# strategy: breaks into overlapping subproblems, stores solutions in a table, guarantees optimal solution
# time complexity: O(n × W)  where W = available_time
# ---------------------------------------------------------------------------
def dp_schedule(tasks: list[dict], available_time: int) -> tuple[list[dict], int, int]:
    # parameters: tasks = list of name, time, value. available_time = total minutes
    # returns: chosen tasks, total time used, total value

    n = len(tasks)
    W = available_time

    # build DP table  (n+1) × (W+1), all zeros
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        t = tasks[i - 1]["time"]
        v = tasks[i - 1]["value"]
        for w in range(W + 1):
            # option A: skip this task
            dp[i][w] = dp[i - 1][w]
            # option B: include this task (only if it fits)
            if t <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - t] + v)

    # back-track to find which tasks were chosen
    chosen = []
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(tasks[i - 1])
            w -= tasks[i - 1]["time"]

    chosen.reverse()
    time_used = sum(t["time"] for t in chosen)
    total_value = dp[n][W]
    return chosen, time_used, total_value


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------
def open_study_planner(master: tk.Tk) -> None:
    """Open the Study Planner in a new Toplevel window."""

    win = tk.Toplevel(master)
    configure_window(win, title="Study Planner", width=900, height=780)
    win.minsize(860, 700)

    # ── internal task list (mutable list shared by closures) ──────────────
    task_list: list[dict] = []

    # -----------------------------------------------------------------------
    # header bar
    # -----------------------------------------------------------------------
    header = tk.Frame(win, bg=COLORS["bg_panel"], height=52)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="  📚  Study Planner",
        font=FONTS["subtitle"],
        bg=COLORS["bg_panel"],
        fg=COLORS["accent"],
        anchor="w",
    ).pack(side="left", padx=PADDING["section"], fill="y")

    tk.Button(
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
    ).pack(side="right", padx=PADDING["section"])

    # -----------------------------------------------------------------------
    # main body (entry panel(left) & result panel(right))
    # -----------------------------------------------------------------------
    body = tk.Frame(win, bg=COLORS["bg_dark"])
    body.pack(fill="both", expand=True, padx=PADDING["window"], pady=PADDING["window"])

    body.columnconfigure(0, weight=0, minsize=260)
    body.columnconfigure(1, weight=1)
    body.rowconfigure(0, weight=1)

    # entry panel
    left = tk.Frame(body, bg=COLORS["bg_panel"], bd=0, width=260)
    left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    left.grid_propagate(False)

    make_label(
        left,
        text="Add Task",
        style="subtitle",
        bg=COLORS["bg_panel"],
        fg=COLORS["accent"],
    ).pack(anchor="w", padx=14, pady=(14, 2))

    # helper to create a labelled entry inside entry panel
    def labelled_entry(parent, label_text: str) -> tk.Entry:
        tk.Label(
            parent,
            text=label_text,
            font=FONTS["caption"],
            bg=COLORS["bg_panel"],
            fg=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x", padx=14, pady=(8, 0))
        entry = tk.Entry(
            parent,
            font=FONTS["body"],
            bg=COLORS["bg_dark"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["accent"],
            relief="flat",
            bd=4,
        )
        entry.pack(fill="x", padx=14, ipady=4)
        return entry

    ent_name  = labelled_entry(left, "Task Name")
    ent_time  = labelled_entry(left, "Time Required (minutes)")
    ent_value = labelled_entry(left, "Value / Priority (1–100)")

    # add task button
    def add_task():
        name  = ent_name.get().strip()
        t_str = ent_time.get().strip()
        v_str = ent_value.get().strip()

        if not name:
            messagebox.showerror("Input Error", "Task name cannot be empty.", parent=win)
            return
        try:
            t = int(t_str)
            v = int(v_str)
            if t <= 0 or v <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Time and Value must be positive integers.",
                parent=win,
            )
            return

        task_list.append({"name": name, "time": t, "value": v})
        ent_name.delete(0, tk.END)
        ent_time.delete(0, tk.END)
        ent_value.delete(0, tk.END)
        _refresh_task_listbox()

    tk.Button(
        left,
        text="＋  Add Task",
        font=FONTS["button"],
        bg=COLORS["accent"],
        fg=COLORS["bg_dark"],
        activebackground=COLORS["accent_dark"],
        activeforeground=COLORS["text_primary"],
        relief="flat",
        bd=0,
        cursor="hand2",
        command=add_task,
        pady=8,
    ).pack(fill="x", padx=14, pady=(12, 4))

    # remove selected task button
    def remove_selected():
        sel = task_lb.curselection()
        if not sel:
            return
        idx = sel[0]
        task_list.pop(idx)
        _refresh_task_listbox()

    tk.Button(
        left,
        text="✕  Remove Selected",
        font=FONTS["caption"],
        bg=COLORS["bg_dark"],
        fg=COLORS["text_secondary"],
        activebackground=COLORS["bg_hover"],
        activeforeground=COLORS["text_primary"],
        relief="flat",
        bd=0,
        cursor="hand2",
        command=remove_selected,
        pady=6,
    ).pack(fill="x", padx=14, pady=(0, 10))

    # task listbox
    tk.Label(
        left,
        text="Current Tasks",
        font=FONTS["caption"],
        bg=COLORS["bg_panel"],
        fg=COLORS["text_secondary"],
        anchor="w",
    ).pack(fill="x", padx=14)

    lb_frame = tk.Frame(left, bg=COLORS["bg_panel"])
    lb_frame.pack(fill="both", expand=True, padx=14, pady=(2, 10))

    scrollbar = tk.Scrollbar(lb_frame)
    scrollbar.pack(side="right", fill="y")

    task_lb = tk.Listbox(
        lb_frame,
        font=FONTS["caption"],
        bg=COLORS["bg_dark"],
        fg=COLORS["text_primary"],
        selectbackground=COLORS["accent_dark"],
        relief="flat",
        bd=0,
        yscrollcommand=scrollbar.set,
    )
    task_lb.pack(fill="both", expand=True)
    scrollbar.config(command=task_lb.yview)

    def _refresh_task_listbox():
        task_lb.delete(0, tk.END)
        for task in task_list:
            task_lb.insert(
                tk.END,
                f"{task['name']}  |  {task['time']} min  |  val {task['value']}",
            )

    # available time
    tk.Label(
        left,
        text="Available Study Time (minutes)",
        font=FONTS["caption"],
        bg=COLORS["bg_panel"],
        fg=COLORS["text_secondary"],
        anchor="w",
    ).pack(fill="x", padx=14, pady=(4, 0))

    ent_avail = tk.Entry(
        left,
        font=FONTS["body"],
        bg=COLORS["bg_dark"],
        fg=COLORS["text_primary"],
        insertbackground=COLORS["accent"],
        relief="flat",
        bd=4,
    )
    ent_avail.pack(fill="x", padx=14, ipady=4)

    # run button
    def run_algorithms():
        if not task_list:
            messagebox.showerror("No Tasks", "Please add at least one task.", parent=win)
            return
        try:
            avail = int(ent_avail.get().strip())
            if avail <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Available time must be a positive integer.",
                parent=win,
            )
            return

        g_tasks, g_time, g_val = greedy_schedule(task_list, avail)
        d_tasks, d_time, d_val = dp_schedule(task_list, avail)
        _display_results(g_tasks, g_time, g_val, d_tasks, d_time, d_val, avail)

    tk.Button(
        left,
        text="▶  Run Both Schedulers",
        font=FONTS["button"],
        bg=COLORS["accent"],
        fg=COLORS["bg_dark"],
        activebackground=COLORS["accent_dark"],
        activeforeground=COLORS["text_primary"],
        relief="flat",
        bd=0,
        cursor="hand2",
        command=run_algorithms,
        pady=10,
    ).pack(fill="x", padx=14, pady=12)

    # result panel
    right = tk.Frame(body, bg=COLORS["bg_panel"])
    right.grid(row=0, column=1, sticky="nsew")

    make_label(
        right,
        text="Results",
        style="subtitle",
        bg=COLORS["bg_panel"],
        fg=COLORS["accent"],
    ).pack(anchor="w", padx=14, pady=(14, 6))

    result_text = tk.Text(
        right,
        font=("Courier", 10),
        bg=COLORS["bg_dark"],
        fg=COLORS["text_primary"],
        insertbackground=COLORS["accent"],
        relief="flat",
        bd=0,
        wrap="word",
        state="disabled",
        padx=10,
        pady=10,
    )
    result_text.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    # configure texts for colored output
    result_text.tag_configure("header",  foreground=COLORS["accent"],       font=("Courier", 11, "bold"))
    result_text.tag_configure("subhdr",  foreground=COLORS["accent_light"], font=("Courier", 10, "bold"))
    result_text.tag_configure("task",    foreground=COLORS["text_primary"],  font=("Courier", 10))
    result_text.tag_configure("summary", foreground="#FFD54F",               font=("Courier", 10, "bold"))
    result_text.tag_configure("note",    foreground=COLORS["text_secondary"],font=("Courier", 9, "italic"))
    result_text.tag_configure("divider", foreground=COLORS["border"],        font=("Courier", 10))

    # colored text in the result panel
    def _write(text: str, tag: str = "task"):
        result_text.config(state="normal")
        result_text.insert(tk.END, text, tag)
        result_text.config(state="disabled")

    def _clear():
        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.config(state="disabled")

    # display results
    def _display_results(g_tasks, g_time, g_val, d_tasks, d_time, d_val, avail):
        _clear()

        _write(f"Available Time: {avail} minutes\n\n", "header")

        # greedy result
        _write("━" * 44 + "\n", "divider")
        _write("  GREEDY SCHEDULER\n", "header")
        _write("  Strategy: highest value/time ratio first\n", "note")
        _write("━" * 44 + "\n", "divider")

        if g_tasks:
            _write(f"  {'Task':<22} {'Time':>6}  {'Value':>6}\n", "subhdr")
            _write(f"  {'─'*22} {'─'*6}  {'─'*6}\n", "divider")
            for t in g_tasks:
                _write(f"  {t['name']:<22} {t['time']:>6}  {t['value']:>6}\n", "task")
        else:
            _write("  No tasks fit within the available time.\n", "note")

        _write(f"\n  Total time used : {g_time} / {avail} min\n", "summary")
        _write(f"  Total value     : {g_val}\n\n", "summary")

        # DP result
        _write("━" * 44 + "\n", "divider")
        _write("  DP OPTIMAL SCHEDULER  (0/1 Knapsack)\n", "header")
        _write("  Strategy: maximise total value exactly\n", "note")
        _write("━" * 44 + "\n", "divider")

        if d_tasks:
            _write(f"  {'Task':<22} {'Time':>6}  {'Value':>6}\n", "subhdr")
            _write(f"  {'─'*22} {'─'*6}  {'─'*6}\n", "divider")
            for t in d_tasks:
                _write(f"  {t['name']:<22} {t['time']:>6}  {t['value']:>6}\n", "task")
        else:
            _write("  No tasks fit within the available time.\n", "note")

        _write(f"\n  Total time used : {d_time} / {avail} min\n", "summary")
        _write(f"  Total value     : {d_val}\n\n", "summary")

        # compare
        _write("━" * 44 + "\n", "divider")
        _write("  COMPARISON\n", "header")
        _write("━" * 44 + "\n", "divider")

        diff = d_val - g_val
        if diff == 0:
            _write("  ✔ Both methods found the same total value.\n", "note")
            _write("  Greedy was optimal here!\n", "note")
        else:
            _write(f"  DP found {diff} more value than Greedy.\n", "note")
            _write("  Greedy is fast but not always optimal.\n", "note")
            _write("  DP guarantees the best possible result.\n", "note")

    # placeholder text when textbox is empty
    _write("Add tasks on the left, set your available\n", "note")
    _write("study time, then click  ▶ Run Both Schedulers.\n\n", "note")
    _write("Results will appear here.\n", "note")

# run file without main.py
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # hide the dummy root window
    open_study_planner(root)
    root.mainloop()
