
import networkx as nx
import matplotlib.pylab as plt
from classes import MCS_Finder
import os
import pylab

def get_simcomp(Clist, filename="SIMCOMP2/test.txt"):
    import urllib
    i = 0
    url = "http://rest.genome.jp/simcomp2/"
    urlC = ""
    for Cnumber in Clist:
        urlC += Cnumber + "+"
    else:
        urlC = urlC[:-1]
    url += urlC + "/" + urlC + "/cutoff=0.1"
    urllib.request.urlretrieve(url, filename)
    return True


def make_graph(Clist, mode=0, filepath="SIMCOMP2/test.txt", lim=0.9):
    G = nx.Graph()
    pylab.figure(figsize=(10, 10))
    scoredic = dict()
    if not os.path.exists(filepath):
        print("input correct filepath")
        return False
    with open(filepath, "r") as fi:

        score = fi.readline().split("\t")
        score[2] = float(score[2][:-1])
        for Cnumber in Clist:
            scorelist = []
            while(True):
                if score[0] == Cnumber:
                    break
                score = fi.readline().split("\t")
                score[2] = float(score[2][:-1])
            if mode == 1:
                while(True):
                    if score[0] == Cnumber:
                        break
                    score = fi.readline().split("\t")
                    score[2] = float(score[2][:-1])
                while(score[2] > lim and score[0] == Cnumber):
                    scorelist.append(score)
                    if score[0] in Clist and score[2] < 1:
                        G = nxappend(G, Cnumber, score[1], score[2])
                    score = fi.readline().split("\t")
                    score[2] = float(score[2][:-1])
            elif mode == 2:
                try:
                    while(True):
                        scorelist.append(score)
                        if score[0] in Clist and score[2] < 1:
                            G = nxappend(G, Cnumber, score[1], score[2])
                        score = fi.readline().split("\t")
                        score[2] = float(score[2][:-1])
                except IndexError:
                    pass
            else:
                for i in range(3):
                    while(True):
                        if score[0] == Cnumber:
                            break
                        score = fi.readline().split("\t")
                        score[2] = float(score[2][:-1])
                    scorelist.append(score)
                    if score[0] in Clist and score[2] < 1:
                        G = nxappend(G, Cnumber, score[1], score[2])
                    score = fi.readline().split("\t")
                    score[2] = float(score[2][:-1])
            scoredic[Cnumber] = scorelist
    print(str(len(G.nodes())) + "/" + str(len(Clist)))
    print("edge:" + str(len(G.edges())))
    # for g in nx.connected_component_subgraphs(G):
    drawnx(G)
    # nx.draw_networkx(G)
    # plt.xticks([])
    # plt.yticks([])
    # plt.show()
    # return scoredic


def nxappend(G, start, end, weight):
    if not start in G.nodes():
        G.add_node(start)
    if not end in G.nodes():
        G.add_node(end)
    if not (start, end) in G.edges() and not (end, start) in G.edges():
        G.add_edge(start, end, weight=weight)
    else:
        G.edges()
    return G


def drawnx(G):
    pos = nx.spring_layout(G)
    edge_labels = dict()
    for param in G.edges(data=True):
        edge_labels[(param[0], param[1])] = param[2]["weight"]
    nx.draw_networkx_nodes(G, pos, node_size=200, node_color="w")
    edge_width = [ d['weight'] for (u,v,d) in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, width=edge_width)
    # nx.draw_networkx_edges(G, pos)
    # nx.draw_networkx_edge_labels(G, pos,edge_labels)
    nx.draw_networkx_labels(G, pos ,font_size=10, font_color="r")
    plt.xticks([])
    plt.yticks([])
    plt.show()


def main():
    make_graph(mode=0)


if __name__ == '__main__':
    main()

plt.close()
plt.clf()
