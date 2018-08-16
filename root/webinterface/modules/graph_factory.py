import collections
import os
from os.path import dirname

from modules import datahandler as dth
import pydotplus
import matplotlib.pyplot as plt

path = dth.Path.path
file_name = 'graph'
file_type = '.png'


# TODO add functionality for multiple images being created without overwriting existing ones
# TODO stop programming python like it's Java
def generate_graph(x_data, y_data, x_label, y_label, title):
    file = '%s%s%s%s' % (dirname(dirname(path)), '/webinterface/static/img/', file_name, file_type)
    if os.path.isfile(file):
        os.remove(file)

    plt.scatter(x_data, y_data, color='#b23000')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(file)
    plt.clf()

    if os.path.isfile(file):
        return True
    else:
        return False


def generate_line_plot_confidence_intervals(x_data, y_data, x_label, y_label, title):
    _, ax = plt.subplots()
    ax.plot(x_data, y_data, lw=2, color='#b23000', alpha=1)

    # Label the axes and provide a title
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    plt.savefig(ax)
    plt.clf()  # Clears figure
