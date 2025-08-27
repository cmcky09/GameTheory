import networkx as nx
from networkx_viewer import Viewer
from numpy import log2
import random
import tkinter as tk
from networkx_viewer import NodeToken, GraphCanvas


G = nx.DiGraph()
#node string variables to help avoid typos:
start = "start"

#Russia Options:
military_escalation = 'Military Escalation (Aggressive)'
attrition_strategy = 'Attrition Strategy (Passive-Aggressive)'
negotiation_deescalation = 'Negotiation and De-escalation (Passive)'
proxy_warfare = 'Proxy Warfare (Indirect)'

#West Response:
sanctions = 'Sanctions (Aggressive)'
military_aid = 'Military Aid to Ukraine (Supportive)'
diplomatic_pressure = 'Diplomatic Pressure (Negotiation)'
containment = 'Containment Strategy (Passive)'




#ending type
complete_quick_cheap = 'Take Ukraine Completely, Quickly, and Cheaply'
partial_quick_cheap = 'Take Ukraine Partially, Quickly, and Cheaply'
lose_quick_cheap = 'Lose, Quickly, and Cheaply'
complete_quick_expensive = 'Take Ukraine Completely, Quickly, and Expensively'
complete_slow_expensive = 'Take Ukraine Completely, Slowly, and Expensively'
partial_slow_expensive = 'Take Ukraine Partially, Slowly, and Expensively'
lose_slow_expensive = 'Lose, Slowly, and Expensively'

end = 'end'

ukraine_chance = lambda :1-random.random()/5 #random double from (0-1]/5

''''''
#all edges should have weight W with 0<W<=1
#initial moves should all have `weight` =1 and `u_of_edge` = 'start' as a formality
#Multiply by *ukraine_chance() wherever relevant.
#Note: Ukraine chance is always a negative modifier on every weight

G.add_edge(start,military_escalation,weight=1 *ukraine_chance() )
G.add_edge(start,attrition_strategy,weight=1 *ukraine_chance() )
G.add_edge(start,negotiation_deescalation,weight=1 *ukraine_chance() )
G.add_edge(start,proxy_warfare,weight=1 *ukraine_chance() )


''''''
#From Russian First move to Western Response:

#from russian military escalation
G.add_edge(military_escalation,sanctions,weight=.99)
G.add_edge(military_escalation,military_aid,weight=.99)
G.add_edge(military_escalation,diplomatic_pressure,weight=.99)
G.add_edge(military_escalation,containment,weight=.99)

#from russian attrition strat
G.add_edge(attrition_strategy,sanctions,weight=.99)
G.add_edge(attrition_strategy,military_aid,weight=.99)
G.add_edge(attrition_strategy,diplomatic_pressure,weight=.99)
G.add_edge(attrition_strategy,containment,weight=.99)

#from russian negotiation and de-escalation
G.add_edge(negotiation_deescalation,sanctions,weight=.99)
G.add_edge(negotiation_deescalation,military_aid,weight=.99)
G.add_edge(negotiation_deescalation,diplomatic_pressure,weight=.99)
G.add_edge(negotiation_deescalation,containment,weight=.99)

#from russian proxy warfare
G.add_edge(proxy_warfare,sanctions,weight=.99)
G.add_edge(proxy_warfare,military_aid,weight=.99)
G.add_edge(proxy_warfare,diplomatic_pressure,weight=.99)
G.add_edge(proxy_warfare,containment,weight=.99)

''''''
#From Western Moves to Payout nodes:

#From sanctions:

G.add_edge(sanctions,complete_quick_cheap,weight=.99)
G.add_edge(sanctions,complete_quick_expensive,weight=.99)
G.add_edge(sanctions,complete_slow_expensive,weight=.99)
G.add_edge(sanctions,lose_quick_cheap,weight=.99)

#From military aid:
G.add_edge(military_aid,complete_quick_cheap,weight=.99)
G.add_edge(military_aid,complete_quick_expensive,weight=.99)
G.add_edge(military_aid,complete_slow_expensive,weight=.99)
G.add_edge(military_aid,lose_quick_cheap,weight=.99)


'''^Fill in the rest as relevant^'''


''''''
'''payout:'''
#Payout nodes all have parameter `v_of_edge` = 'end' as a formality

G.add_edge(complete_quick_cheap,end,weight=1)
#G.add_edge(partial_quick_cheap,'end',weight=.7)
G.add_edge(complete_quick_expensive,end,weight=.5)
G.add_edge(complete_slow_expensive,end,weight=.2)#
#G.add_edge(partial_slow_expensive,end,weight=.1)
G.add_edge(lose_quick_cheap,end,weight=.01)#
#G.add_edge(lose_slow_expensive,end,weight=.001)



'''For Dijkstra's transformations:'''
#Transform edge weights for Dijkstra's
for u,v,edge in G.edges(data=True):
    edge['weight'] = -log2(edge['weight'])


dijkstra_nodes_list = nx.dijkstra_path(G,'start','end')
for i in range(len(dijkstra_nodes_list)-1):
    node = dijkstra_nodes_list[i]
    node2 = dijkstra_nodes_list[i+1]
    #G.nodes[node]['circle'] = True
    G.nodes[node]['fill'] = 'blue'
    G.nodes[node2]['fill'] = 'blue'
    G.edges[(node,node2)]['width'] = 5

print(dijkstra_nodes_list)
#print(G.edges)
#print(G.nodes)


#Start the visualization:
#app = Viewer(G)
#app.mainloop()




#pos = nx.bfs_layout(G,start)
app = Viewer(G)

app.mainloop()
