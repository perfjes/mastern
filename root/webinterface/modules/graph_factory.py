import glob
import os
from os.path import dirname
from modules import datahandler as dth
import matplotlib.pyplot as plt


def clean_up_graph_folder():
    files = glob.glob(dth.Path.img + '/graphs/*')
    for file in files:
        os.remove(file)


# TODO add functionality for multiple images being created without overwriting existing ones
# TODO stop programming python like it's Java
def generate_graph(x_data, y_data, x_label, y_label, title, filename):
    file = '%s%s' % (dth.Path.img + '/graphs/', filename)
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
    graphs = []
    count = 1
    for feature in list(data):
        if feature != 'years in vivo':
            graphs.append(generate_graph(data['years in vivo'], data[feature], 'years in vivo', feature,
                                         'Relation between longevity and ' + feature, 'graph' + str(count) + '.png'))
            count += 1
    return graphs


def histogram_of_results(list_of_results):
    path = '%s%s' % (dth.Path.img + '/graphs/', 'histogram.png')
    plt.xlabel('Predicted years of longevity')
    plt.ylabel('Number of predictions')
    plt.hist(list_of_results, color='#b23000')
    plt.savefig(path)
    plt.clf()
    return ['histogram.png']
