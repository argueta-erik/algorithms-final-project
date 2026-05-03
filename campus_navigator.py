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
from tkinter import ttk
from util import COLORS, FONTS, PADDING, configure_window, make_label, make_nav_button
#from enum import IntEnum
from campus_navigation.BFS_solve import solve_bfs
from campus_navigation.DFS_solve import solve_dfs
from campus_navigation.Dijkstra_solve import solve_dijkstra
from campus_navigation.Prim_solve import prim_mst
import campus_navigation.Buildings as B
def reset_edges(canvas, edges):
    for edge in edges.values():
        canvas.itemconfig(edge, fill=COLORS["accent"])

def on_resize(building_nodes, building_node_locations, edges, weights, node_names, canvas, event=None):
    node_size = 25
    if event:
        w, h = event.width, event.height
    else:
        w, h = 800, 508
    #edges
    for edge in edges:
        start = edge[0]
        end = edge[1]
        dirx = (building_node_locations[start][0])*w - (building_node_locations[end][0])*w
        diry = (building_node_locations[start][1])*h - (building_node_locations[end][1])*h
        unit_dir = pow(dirx**2 + diry**2, 0.5)
        weight_offset_x = (diry/unit_dir)*15
        weight_offset_y = (dirx/unit_dir)*15
        canvas.coords(edges[edge], ((building_node_locations[start][0])*w, (building_node_locations[start][1])*h, (building_node_locations[end][0])*w, (building_node_locations[end][1])*h))
        canvas.coords(weights[edges[edge]], building_node_locations[start][0]*w - (dirx)/2 + weight_offset_x, building_node_locations[start][1]*h - (diry)/2 - weight_offset_y)
    #nodes and text
    for i in range(0, len(building_nodes)):
        building = building_node_locations[i]
        node = building_nodes[i]
        text = node_names[i]
        canvas.coords(node, (building[0])*(w)-node_size, (building[1])*(h)-node_size, (building[0])*(w)+node_size, (building[1])*(h)+node_size)
        canvas.coords(text, building[0]*w, building[1]*h)

def oval_on_left_click(node, building_nodes, start_and_end, canvas):
    canvas.itemconfig(building_nodes[start_and_end[0]], fill=COLORS["accent"])
    start_and_end[0] = building_nodes.index(node)
    canvas.itemconfig(node, fill=COLORS["accent_dark"])

def oval_on_right_click(node, building_nodes, start_and_end, canvas):
    canvas.itemconfig(building_nodes[start_and_end[1]], fill=COLORS["accent"])
    start_and_end[1] = building_nodes.index(node)
    canvas.itemconfig(node, fill=COLORS["accent_dark"])

def edge_on_enter(edge, show_weights, canvas):
    if show_weights.get():
        return None
    canvas.itemconfig(edge, state='normal')

def edge_on_leave(edge, show_weights, canvas):
    if show_weights.get():
        return None
    canvas.itemconfig(edge, state='hidden')

def toggle_weights(weights, show_weights, canvas):
    print(show_weights.get())
    if show_weights.get():
        for weight in weights.values():
            canvas.itemconfig(weight, state='normal')
    else:
        for weight in weights.values():
            canvas.itemconfig(weight, state='hidden')

def BFS(canvas, edges, start_and_end):
    path = solve_bfs(*start_and_end)[0]
    reset_edges(canvas, edges)
    #recolor lines on path
    for nodes in zip(path[0::1], path[1::1]):
        #try to get edge both ways because only one actually exists
        try:
            edge = edges[nodes]
        except KeyError:
            edge = edges[(nodes[1],nodes[0])]
        canvas.itemconfig(edge, fill="orange")
        
def Prim(canvas, edges, start_and_end):
    path = prim_mst(start_and_end[0])[0]
    reset_edges(canvas, edges)
    #recolor lines on path
    for start, end, _ in path:
        nodes = (start,end)
        #try to get edge both ways because only one actually exists
        try:
            edge = edges[nodes]
        except KeyError:
            edge = edges[(nodes[1],nodes[0])]

        canvas.itemconfig(edge, fill="orange")

def DFS(canvas, edges, start_and_end):
    path = solve_dfs(*start_and_end)[0]
    reset_edges(canvas, edges)
    #recolor lines on path
    for nodes in zip(path[0::1], path[1::1]):
        #try to get edge both ways because only one actually exists
        try:
            edge = edges[nodes]
        except KeyError:
            edge = edges[(nodes[1],nodes[0])]
        canvas.itemconfig(edge, fill="orange")

def Dijkstra(canvas, edges, start_and_end):
    print(solve_dijkstra(*start_and_end))


def open_campus_navigator(master: tk.Tk) -> None:

    '''relevant variable declarations'''
    building_node_locations = [(400,150), #PL
                               (350,50), #KH
                               (450,50), #HC
                               (650,100), #E
                               (750, 100), #CS
                               (550, 150), #EC
                               (550, 250), #H
                               (550, 350), #GH
                               (550,450), #LDH
                               (400, 450), #DBH
                               (400, 350), #MCH
                               (300, 250), #CPA
                               (100, 150), #TS
                               (250, 150), #TSU
                               (150, 50)] #SRC
    #turning coords to ratios to be multiplied by canvas size when made
    building_node_locations = [(x/800, y/508) for x,y in building_node_locations]
    building_nodes = []
    node_names = []
    edges = {}
    weights = {}
    start_and_end = [0, 0]
    show_weights = tk.BooleanVar()
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
    content.pack(fill="both", expand=True)

    canvas = tk.Canvas(content, bg=COLORS["bg_dark"], borderwidth=0, highlightthickness=0)
    canvas.pack(expand=True, fill='both')

    #finding unique edges
    for start in range(0, len(B.buildings_list)):
        start_list = B.buildings_list[start]
        for end, w in start_list:
            if not (end, start) in edges:
                edges[(start, end)] = canvas.create_line(0,0,0,0, fill=COLORS["accent"])
                print(B.buildings_list[start][1])
                weights[edges[(start,end)]] = canvas.create_text(0,0, text=w, fill=COLORS["text_primary"], state='hidden')

        for edge in edges.values():
            canvas.tag_bind(edge, "<Enter>", lambda event, id=weights[edge]: edge_on_enter(id, show_weights, canvas))
            canvas.tag_bind(edge, "<Leave>", lambda event, id=weights[edge]: edge_on_leave(id, show_weights, canvas))

    #initializing nodes and text
    for i in range(0, len(building_node_locations)):
        building_nodes.append(canvas.create_oval(0,0,0,0,fill=COLORS["accent"], activefill=COLORS["accent_dark"]))
        node_names.append(canvas.create_text(0,0, text=B.Buildings(i+1).name))
    #putting click events on nodes
    for node in building_nodes:
        canvas.tag_bind(node, "<Button-1>", lambda event, id=node: oval_on_left_click(id, building_nodes, start_and_end, canvas))
        canvas.tag_bind(node, "<Button-3>", lambda event, id=node: oval_on_right_click(id, building_nodes, start_and_end, canvas))
    #using make positions and sizes change when window size does
    canvas.bind("<Configure>", lambda event: on_resize(building_nodes, building_node_locations, edges, weights, node_names, canvas, event))
    #function buttons
    buttonPrim = tk.Button(header, text="Prim", command= lambda: Prim(canvas, edges, start_and_end))
    buttonBFS = tk.Button(header, text="BFS", command= lambda: BFS(canvas, edges, start_and_end))
    buttonDFS = tk.Button(header, text="DFS", command= lambda: DFS(canvas, edges, start_and_end))
    buttonDijkstra = tk.Button(header, text="Dijkstra", command= lambda: Dijkstra(canvas, edges, start_and_end))
    buttonDFS.pack(side=tk.LEFT)
    buttonPrim.pack(side=tk.LEFT)
    buttonBFS.pack(side=tk.LEFT)
    buttonDijkstra.pack(side=tk.LEFT)
    toggle_btn = ttk.Checkbutton(canvas, text="show weights", onvalue=True, offvalue=False, variable=show_weights, command= lambda: toggle_weights(weights, show_weights, canvas))
    toggle_btn.pack()
if __name__ == "__main__":
    root = tk.Tk()
    configure_window(root, title="CampusNavigator", width=800, height=560)
    open_campus_navigator(root)
    root.mainloop()


    