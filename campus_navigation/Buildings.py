from enum import IntEnum
Buildings = IntEnum('Buildings', ['PL', 'KH', 'HC', 'E', 'CS', 'EC', 'H', 'GH', 'LDH', 'DBH', 'MCH', 'CPA', 'TSU', 'TS', 'SRC'])

def add_edge(adj, u, v, w):
    adj[u-1].append((v-1,w))

#building adjacency list
num_of_buildings = Buildings.SRC
buildings_list = [[] for _ in range(num_of_buildings)]

'''manually setting values for list'''

#Pollak Library
add_edge(buildings_list, Buildings.PL, Buildings.TS, 4)
add_edge(buildings_list, Buildings.PL, Buildings.CPA, 1)
add_edge(buildings_list, Buildings.PL, Buildings.MCH, 6)
add_edge(buildings_list, Buildings.PL, Buildings.GH, 7)
add_edge(buildings_list, Buildings.PL, Buildings.H, 4)
add_edge(buildings_list, Buildings.PL, Buildings.EC, 3)
add_edge(buildings_list, Buildings.PL, Buildings.HC, 5)
add_edge(buildings_list, Buildings.PL, Buildings.KH, 3)

#Kinesiology & Health Science
add_edge(buildings_list, Buildings.KH, Buildings.SRC, 2)
add_edge(buildings_list, Buildings.KH, Buildings.TSU, 4)
add_edge(buildings_list, Buildings.KH, Buildings.TS, 3)
add_edge(buildings_list, Buildings.KH, Buildings.PL, 3)
add_edge(buildings_list, Buildings.KH, Buildings.HC, 3)

#Student Health and Counseling Center
add_edge(buildings_list, Buildings.HC, Buildings.KH, 3)
add_edge(buildings_list, Buildings.HC, Buildings.PL, 5)
add_edge(buildings_list, Buildings.HC, Buildings.EC, 6)
add_edge(buildings_list, Buildings.HC, Buildings.E, 3)

#Engineering
add_edge(buildings_list, Buildings.E, Buildings.HC, 3)
add_edge(buildings_list, Buildings.E, Buildings.EC, 4)
add_edge(buildings_list, Buildings.E, Buildings.CS, 1)

#Computer Science
add_edge(buildings_list, Buildings.CS, Buildings.E, 1)

#Education Classrooms
add_edge(buildings_list, Buildings.EC, Buildings.PL, 3)
add_edge(buildings_list, Buildings.EC, Buildings.H, 3)
add_edge(buildings_list, Buildings.EC, Buildings.E, 4)
add_edge(buildings_list, Buildings.EC, Buildings.HC, 6)

#Humanities
add_edge(buildings_list, Buildings.H, Buildings.PL, 4)
add_edge(buildings_list, Buildings.H, Buildings.GH, 3)
add_edge(buildings_list, Buildings.H, Buildings.EC, 3)

#Gordon Hall
add_edge(buildings_list, Buildings.GH, Buildings.PL, 7)
add_edge(buildings_list, Buildings.GH, Buildings.MCH, 2)
add_edge(buildings_list, Buildings.GH, Buildings.LDH, 2)
add_edge(buildings_list, Buildings.GH, Buildings.H, 3)

#Langsdorf Hall
add_edge(buildings_list, Buildings.LDH, Buildings.MCH, 2)
add_edge(buildings_list, Buildings.LDH, Buildings.DBH, 1)
add_edge(buildings_list, Buildings.LDH, Buildings.GH, 2)

#Dan Black Hall
add_edge(buildings_list, Buildings.DBH, Buildings.MCH, 1)
add_edge(buildings_list, Buildings.DBH, Buildings.LDH, 1)

#McCarthy Hall
add_edge(buildings_list, Buildings.MCH, Buildings.CPA, 1)
add_edge(buildings_list, Buildings.MCH, Buildings.DBH, 1)
add_edge(buildings_list, Buildings.MCH, Buildings.LDH, 2)
add_edge(buildings_list, Buildings.MCH, Buildings.GH, 2)
add_edge(buildings_list, Buildings.MCH, Buildings.PL, 6)

#Clayes Performing Arts Center
add_edge(buildings_list, Buildings.CPA, Buildings.TSU, 2)
add_edge(buildings_list, Buildings.CPA, Buildings.MCH, 1)
add_edge(buildings_list, Buildings.CPA, Buildings.PL, 1)
add_edge(buildings_list, Buildings.CPA, Buildings.TS, 3)

#Titan Student Union
add_edge(buildings_list, Buildings.TSU, Buildings.CPA, 2)
add_edge(buildings_list, Buildings.TSU, Buildings.TS, 1)
add_edge(buildings_list, Buildings.TSU, Buildings.KH, 4)
add_edge(buildings_list, Buildings.TSU, Buildings.SRC, 2)

#Titan Shops
add_edge(buildings_list, Buildings.TS, Buildings.TSU, 1)
add_edge(buildings_list, Buildings.TS, Buildings.CPA, 3)
add_edge(buildings_list, Buildings.TS, Buildings.PL, 4)
add_edge(buildings_list, Buildings.TS, Buildings.KH, 3)

#Student Recreation Center
add_edge(buildings_list, Buildings.SRC, Buildings.TSU, 2)
add_edge(buildings_list, Buildings.SRC, Buildings.KH, 2)
