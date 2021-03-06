
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
            if mode == 1:
                #特定のスコア値以上のエッジを作る
                while(score[1] > 0.9):
                    scorelist.append(score)
                    if score[0] in Clist and score[1] < 1:
                        G = nxappend(G, Cnumber, score[0], score[1])
                    score = fi.readline().split("\t")
                    score[1] = float(score[1][:-1])
            elif mode == 2:
                # 全部のエッジを作る。
                try:
                    while(True):
                        scorelist.append(score)
                        if score[0] in Clist and score[1] < 1:
                            G = nxappend(G, Cnumber, score[0], score[1])
                        score = fi.readline().split("\t")
                        score[1] = float(score[1][:-1])
                except IndexError:
                    pass
            elif mode == 3:
                # スコア値の高い順に二つ取ってくる 物によっては一つになっている。
                for i in range(3):
                    scorelist.append(score)
                    if score[0] in Clist and score[1] < 1:
                        G = nxappend(G, Cnumber, score[0], score[1])
                    score = fi.readline().split("\t")
                    score[1] = float(score[1][:-1])
            else:
                # エッジが二つになるように取ってくる
                i = 0
                try:
                    while(True):
                        scorelist.append(score)
                        if score[0] in Clist and score[1] < 1:
                            G = nxappend(G, Cnumber, score[0], score[1])
                            i += 1
                        score = fi.readline().split("\t")
                        score[1] = float(score[1][:-1])
                        if i >= 2:
                            break
                except IndexError:
                    pass
            scoredic[Cnumber] = scorelist
    print(str(len(G.nodes())) + "/" + str(len(Clist)))
    print("edge:" + str(len(G.edges())))
    # for g in nx.connected_component_subgraphs(G):
    drawnx(G)
    # nx.draw_networkx(G)
    # plt.xticks([])
    # plt.yticks([])
    # plt.show()


def nxappend(G, start, end, weight):
    if not start in G.nodes():
        G.add_node(start)
    if not end in G.nodes():
        G.add_node(end)
    if not (start, end) in G.edges() and not (end, start) in G.edges():
        G.add_edge(start, end, weight=weight)
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
    temp1(mode=0)


if __name__ == '__main__':
    main()

plt.close()
plt.clf()
