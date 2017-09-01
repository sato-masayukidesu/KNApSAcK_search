
import networkx as nx
import matplotlib.pylab as plt
from classes import MCS_Finder
import os
import pylab

def temp1(mode=0):
    G = nx.Graph()
    pylab.figure(figsize=(10, 10))
    scoredic = dict()
    f = MCS_Finder("Streptomyces")
    Clist = f.get_Cnlist_from_label2("C(C)-C(C)-C(C-C-C-C-C-C)-C-C-C-C-C-C-C-C-C")
    for Cnumber in Clist:
        filepath = "SIMCOMP/" + Cnumber + ".txt"
        if not os.path.exists(filepath):
            continue
        with open(filepath, "r") as fi:
            scorelist = []
            score = fi.readline().split("\t")
            score[1] = float(score[1][:-1])
            if mode:
                while(score[1] > 0.9):
                    scorelist.append(score)
                    if score[0] in Clist and score[1] < 1:
                        G = nxappend(G, Cnumber, score[0], score[1])
                    score = fi.readline().split("\t")
                    score[1] = float(score[1][:-1])
            else:
                for i in range(3):
                    scorelist.append(score)
                    if score[0] in Clist and score[1] < 1:
                        G = nxappend(G, Cnumber, score[0], score[1])
                    score = fi.readline().split("\t")
                    score[1] = float(score[1][:-1])
            scoredic[Cnumber] = scorelist
    drawnx(G)
    print(str(len(G.nodes())) + "/" + str(len(Clist)))


def nxappend(G, start, end, weight):
    if not start in G.nodes():
        G.add_node(start)
    if not end in G.nodes():
        G.add_node(end)
    if not (start, end) in G.edges() and not (end, start) in G.edges():
        G.add_edge(start, end, weight=weight)
    return G


def drawnx(G):
    pos = nx.spring_layout(G, k=0.3)
    edge_labels = dict()
    for param in G.edges(data=True):
        edge_labels[(param[0], param[1])] = param[2]["weight"]
    nx.draw_networkx_nodes(G, pos, node_size=200, node_color="w")
    edge_width = [ d['weight']*2**2 for (u,v,d) in G.edges(data=True)]
    # nx.draw_networkx_edges(G, pos, width=edge_width)
    nx.draw_networkx_edges(G, pos)
    # nx.draw_networkx_edge_labels(G, pos,edge_labels)
    nx.draw_networkx_labels(G, pos ,font_size=10, font_color="r")
    plt.xticks([])
    plt.yticks([])
    plt.show()


def main():
    temp1(mode=1)


if __name__ == '__main__':
    main()

plt.close()
plt.clf()
