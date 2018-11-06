import glob
import os
from os.path import dirname

from modules import datahandler as dth
import matplotlib.pyplot as plt

path = dth.Path.path


# TODO add functionality for multiple images being created without overwriting existing ones
# TODO stop programming python like it's Java
def generate_graph(x_data, y_data, x_label, y_label, title, filename):
    file = '%s%s%s' % (dirname(dirname(path)), '/webinterface/static/img/graphs/', filename)
    if os.path.isfile(file):
        os.remove(file)
    plt.scatter(x_data, y_data, color='#b23000')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(file)
    plt.clf()
    return filename


def generate_line_plot_confidence_intervals(x_data, y_data, x_label, y_label, title):
    _, ax = plt.subplots()
    ax.plot(x_data, y_data, lw=2, color='#b23000', alpha=1)

    # Label the axes and provide a title
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    plt.savefig(ax)
    plt.clf()  # Clears figure


def make_some_graphs():
    data = dth.prune_features(dth.Data.dataframe)
    files = glob.glob(dth.Path.img + '/graphs/*')
    for file in files:
        print(file)
        os.remove(file)
    graphs = []
    count = 1
    for feature in list(data):
        if feature != 'years in vivo':
            graphs.append(generate_graph(data['years in vivo'], data[feature], 'years in vivo', feature,
                                         'Relation between longevity and ' + feature, 'graph' + str(count) + '.png'))
            count += 1

    return graphs