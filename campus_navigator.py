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
#from enum import IntEnum
from campus_navigation.BFS_solve import solve_bfs
from campus_navigation.DFS_solve import solve_dfs
from campus_navigation.Dijkstra_solve import solve_dijkstra
from campus_navigation.Prim_solve import prim_mst
import campus_navigation.Buildings as B

def on_resize(event, building_nodes, building_node_locations, edges, edge_coords, edges_by_coord, node_names, canvas):
    node_size = 25
    edges_by_coord.clear()
    w, h = event.width, event.height
    for i, edge_coord in enumerate(edge_coords):
        edge = edges[i]
        edge_coords[edge_coord] = ((building_node_locations[edge_coord[0]][0])*w/800, (building_node_locations[edge_coord[0]][1])*h/508, (building_node_locations[edge_coord[1]][0])*w/800, (building_node_locations[edge_coord[1]][1])*h/508)
        edge_coord = edge_coords[edge_coord]
        print(i, edge_coord)
        edges_by_coord[edge_coord] = edge
        canvas.coords(edge, edge_coord[0], edge_coord[1], edge_coord[2], edge_coord[3])#(building_node_locations[edge_coord[0]][0])*w/800, (building_node_locations[edge_coord[0]][1])*h/508, (building_node_locations[edge_coord[1]][0])*w/800, (building_node_locations[edge_coord[1]][1])*h/508)
        #canvas.coords(edge, 50, 50, 100, 100)
    for i in range(0, len(building_nodes)):
        building = building_node_locations[i]
        node = building_nodes[i]
        text = node_names[i]
        canvas.coords(node, (building[0])*(w/800)-node_size, (building[1])*(h/508)-node_size, (building[0])*(w/800)+node_size, (building[1])*(h/508)+node_size)
        canvas.coords(text, building[0]*w/800, building[1]*h/508)
        canvas.itemconfig(text, text=B.Buildings(i+1).name)

def oval_on_left_click(event, node, building_nodes, start_and_end):
    print(building_nodes.index(node))
    print(building_nodes)
    start_and_end[0] = building_nodes.index(node)
def oval_on_right_click(event, node, building_nodes, start_and_end):
    print(building_nodes.index(node))
    start_and_end[1] = building_nodes.index(node)

def on_start(building_nodes, building_node_locations, edges, edge_coords, edges_by_coord, node_names, canvas):
    node_size = 25
    w, h = 800, 508
    edges_by_coord.clear()
    for i, edge_coord in enumerate(edge_coords):
        edge = edges[i]
        edge_coords[edge_coord] = ((building_node_locations[edge_coord[0]][0])*w/800, (building_node_locations[edge_coord[0]][1])*h/508, (building_node_locations[edge_coord[1]][0])*w/800, (building_node_locations[edge_coord[1]][1])*h/508)
        edge_coord = edge_coords[edge_coord]
        print(i, edge_coord)
        edges_by_coord[edge_coord] = canvas.coords(edge, edge_coord[0], edge_coord[1], edge_coord[2], edge_coord[3])#(building_node_locations[edge_coord[0]][0])*w/800, (building_node_locations[edge_coord[0]][1])*h/508, (building_node_locations[edge_coord[1]][0])*w/800, (building_node_locations[edge_coord[1]][1])*h/508)
        #canvas.coords(edge, 50, 50, 100, 100)
    for i in range(0, len(building_nodes)):
        building = building_node_locations[i]
        node = building_nodes[i]
        text = node_names[i]
        canvas.coords(node, (building[0])*(w/800)-node_size, (building[1])*(h/508)-node_size, (building[0])*(w/800)+node_size, (building[1])*(h/508)+node_size)
        canvas.coords(text, building[0]*w/800, building[1]*h/508)
        canvas.itemconfig(text, text=B.Buildings(i+1).name)
        
def BFS(canvas, edge_coords, edges_by_coord, start_and_end):
    print(start_and_end)
    path_info = solve_bfs(start_and_end[0]+1, start_and_end[1]+1)
    print(path_info)
    path = path_info[0]
    for nodes in zip(path[0::1], path[1::1]):
        print(path_info[0])
        print(nodes)
        try:
            edge = edges_by_coord[edge_coords[nodes]]
        except KeyError:
            edge = edges_by_coord[edge_coords[(nodes[1],nodes[0])]]
        #canvas.create_line(edge[0], edge[1], edge[2], edge[3], fill="orange")
        canvas.itemconfig(edge, fill="orange")
        
def Prim(canvas, edge_coords, edges_by_coord, start_and_end):
    path_info = prim_mst(start_and_end[0]+1)
    path = path_info[0]
    for start, end, _ in path:
        nodes = (start,end)
        print(path_info[0])
        print(nodes)
        try:
            edge = edges_by_coord[edge_coords[nodes]]
        except KeyError:
            edge = edges_by_coord[edge_coords[(nodes[1],nodes[0])]]
        #canvas.create_line(edge[0], edge[1], edge[2], edge[3], fill="orange")
        canvas.itemconfig(edge, fill="orange")

def open_campus_navigator(master: tk.Tk) -> None:

    """Open this module in a new Toplevel window."""
    building_node_locations = [(400,150), (350,50), (450,50),(650,100), (750, 100), (550, 150), (550, 250), (550, 350), (550,450), (400, 450), (400, 350), (300, 250), (250, 150), (100, 150), (150, 50)]
    building_nodes = []
    node_names = []
    edge_coords = {}
    edges = []
    start_and_end = [0, 0]
    edges_by_coord = {}
    node_size = 25
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
    content.pack(fill="both", expand=True)#, padx=PADDING["window"], pady=PADDING["window"])

    canvas = tk.Canvas(content, bg=COLORS["bg_dark"], borderwidth=0, highlightthickness=0)
    canvas.pack(expand=True, fill='both')

    for startpoint in range(0, len(B.buildings_list)):
        start_list = B.buildings_list[startpoint]
        for endpoint, _ in start_list:
            if not (endpoint, startpoint) in edge_coords:
                edge_coords[(startpoint, endpoint)] = None
    
    for edge in edge_coords:
        edges.append(canvas.create_line(0,0,0,0, fill=COLORS["accent"]))

    for node in building_node_locations:
        building_nodes.append(canvas.create_oval(0,0,0,0,fill=COLORS["accent"], activefill=COLORS["accent_dark"]))#node[0]-node_size, node[1]-node_size, node[0]+node_size, node[1]+node_size, fill=COLORS["accent"]))
        node_names.append(canvas.create_text(0,0))
    
    for node in building_nodes:
        canvas.tag_bind(node, "<Button-1>", lambda event, id=node: oval_on_left_click(event, id, building_nodes, start_and_end))
        canvas.tag_bind(node, "<Button-3>", lambda event, id=node: oval_on_right_click(event, id, building_nodes, start_and_end))
    on_start(building_nodes, building_node_locations, edges, edge_coords, edges_by_coord, node_names, canvas)
    canvas.bind("<Configure>", lambda event: on_resize(event, building_nodes, building_node_locations, edges, edge_coords, edges_by_coord, node_names, canvas))
    buttonPrim = tk.Button(header, text="Prim", command= lambda: Prim(canvas, edge_coords, edges_by_coord, start_and_end))
    buttonBFS = tk.Button(header, text="BFS", command= lambda: BFS(canvas, edge_coords, edges_by_coord, start_and_end))

    buttonPrim.pack()
    buttonBFS.pack()
if __name__ == "__main__":
    root = tk.Tk()
    configure_window(root, title="CampusNavigator", width=800, height=560)
    open_campus_navigator(root)
    root.mainloop()


    