import random
import pylab
from matplotlib.pyplot import pause
import networkx as nx
pylab.ion()

graph = ''
#node_number = 0
#graph.add_node(node_number, Position=(random.randrange(0, 100), random.randrange(0, 100)))
#num_nodes = graph.number_of_nodes()
#labels = dict.fromkeys(range(num_nodes),0)
labels = dict()
print labels

def alter_labels():
    return

def alter_nodes(graph, node_list, color_list):
    return

def alter_edges(edge_pairs,colors):
    return

def initilize (grapher):

    global graph
    pylab.ion()
    graph = grapher
    nx.draw(graph,pos=nx.get_node_attributes(graph, 'Position'))
    pylab.show()
    pause(2)

def is_int(var):
    try:
        k = int(var)
        return True
    except Exception:
        return False

def draw_fig(fig_info):
    global graph
    nx.draw(graph, pos=nx.get_node_attributes(graph, 'Position'))
    for info in fig_info:
        #label = {key: key.index for key in fig_info[1]}
        #color_label = {key:fig_info[1][key] for key in fig_info[1]}
        nx.draw_networkx_nodes(graph,pos=nx.get_node_attributes(graph, 'Position'),node_color=info[1],nodelist=info[0])
def process_fig(action_list):
    global graph
    nx.draw(graph, pos=nx.get_node_attributes(graph, 'Position'))
    count =1
    for action in action_list:
        print count
        count += 1
        draw_fig(action)
        #pylab.draw()
        pause(1)

    pylab.pause(10)
def get_fig():
    global node_number,labels
    node_number += 1
    graph.add_node(node_number, Position=(random.randrange(0, 100), random.randrange(0, 100)))
    labels[node_number] = random.sample('balamurali'.split(),1)[0]
    graph.add_edge(node_number, random.choice(graph.nodes()))

    nx.draw(graph, pos=nx.get_node_attributes(graph,'Position'))
    nx.draw_networkx_labels(graph, pos=nx.get_node_attributes(graph,'Position'),labels=labels)


def before():
    num_plots = 50;
    pylab.show()


    for i in range(num_plots):

        get_fig()
        pylab.draw()
        pause(2)


