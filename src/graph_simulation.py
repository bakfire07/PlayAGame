"""
Author: Deepak Gujraniya
email: deepakgujraniya@gmail.com
"""


import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class GenerateGraph(object):
    def __init__(self, n, p, D):
        self.graph = nx.Graph()
        nodes = self.generate_nodes(n, D)
        self.graph.add_nodes_from(nodes)
        G = nx.gnp_random_graph(n, p)
        edges = list()
        for edge in G.edges_iter():
            a, b = edge
            edges.append((nodes[a], nodes[b]))
        self.graph.add_edges_from(edges)

    def generate_nodes(self, n, D):
        nodes = list()
        visibility = np.abs(np.random.normal(5, 5, size=n))
        visibility = visibility/max(visibility)
        opr = np.abs(np.random.normal(0, 1, size=n))
        opr = opr / max(opr)
        true_val = np.abs(np.random.normal(0, 1, size=n))
        true_val = true_val / max(true_val)
        for i in range(n):
            d = True if i in D else False
            nodes.append(Node(i, visibility[i], opr[i], d, true_val[i]))
        return nodes

    def centrality(self):
        # print "sending centrality"
        return nx.degree_centrality(self.graph)

    def get_node(self, index):
        return [x for x in self.graph.nodes() if x.index == index][0]

    def draw_graph(self):
        nx.draw(self.graph)
        plt.show()

class Node(object):
    def __init__(self, index, v, opr, D, value):
        self.index = index
        self.visibility = v
        self.operability = opr
        self.isDeception = D
        self.TrueValue = value


if __name__ == "__main__":
    G = GenerateGraph(10, 0.6, [2, 4])
    print G.graph.nodes()
    print G.graph.edges()
    print "neighbors", G.graph.neighbors(G.get_node(1))
    # print s
    degree = nx.degree_centrality(G.graph)
    print degree
    nx.draw(G.graph)
    plt.show()
