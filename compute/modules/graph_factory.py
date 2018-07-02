import collections
import os
from os.path import dirname

import numpy as np

from compute.modules import datahandler as dth
import pydotplus
import matplotlib.pyplot as plt

path = dth.Path.path
file_name = 'graph'
file_type = '.png'


# TODO add functionality for multiple images being created without overwriting existing ones
# TODO stop programming python like it's Java
def save_regression_scatter_as_png(regressor, data1, data2):
    file = '%s%s%s%s' % (dirname(dirname(path)), '/webinterface/static/img/', file_name, file_type)
    if os.path.isfile(file):
        os.remove(file)
    plt.scatter(data1, data2)
    plt.xlabel('True vivos')
    plt.ylabel('Predictivivos')
    plt.savefig(file)
    plt.clf()

    if os.path.isfile(file):
        return True
    else:
        return False


# DEPRECATED (still want the code for reference though)
def graph_factory(classifier):
    from sklearn import tree

    dot_data = tree.export_graphviz(classifier,
                                    feature_names=list(dth.Data.dataframe.drop('Case', axis=1)),
                                    out_file=None,
                                    filled=True,
                                    rounded=True)
    graph = pydotplus.graph_from_dot_data(dot_data)

    colors = ('turquoise', 'orange')
    edges = collections.defaultdict(list)

    for edge in graph.get_edge_list():
        edges[edge.get_source()].append(int(edge.get_destination()))

    for edge in edges:
        edges[edge].sort()
        for i in range(2):
            dest = graph.get_node(str(edges[edge][i]))[0]
            dest.set_fillcolor(colors[i])
    save_file = '%s%s' % (path, 'tree.png')
    graph.write_png(save_file)
    return graph
