import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def drawActivity(agraph, act):
    grp = nx.MultiDiGraph()
    nodeind = 0
    nodedict = {}
    print("  ")
    for key in act.nodes:
        nodeind = nodeind + 1
        nodedict[key] = nodeind
        print("Node #"+str(nodeind))
        print("  IP:"+str(agraph.nodes[key].ip))

    print("  ")
    edgeind = 0
    for key in act.edges:
        edgeind = edgeind + 1
        grp.add_edges_from([(nodedict[act.edges[key].sourceid],
                             nodedict[act.edges[key].destid])])
        print("Edge #"+str(edgeind))
        print("  Source Port:"+str(agraph.edges[key].sourcePort))
        print("  Dest Port  :"+str(agraph.edges[key].destPort).strip())
        print("  Time       :"+str(agraph.edges[key].timesig))
        print("  ")

    pos = nx.spring_layout(grp)
    nx.draw_networkx_nodes(grp, pos)
    nx.draw_networkx_edges(grp, pos)
    plt.show()
    
