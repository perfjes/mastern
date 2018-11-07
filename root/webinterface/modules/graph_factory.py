import glob
import os
import numpy as np
from statistics import mean
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
    m, b = best_fit_slope_and_intercept(x_data, y_data)
    regression_line = []
    for x in x_data:
        regression_line.append((m*x) + b)

    plt.scatter(x_data, y_data, color='#b23000')
    plt.plot(x_data, regression_line, color='#ba7f04')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(file)
    plt.clf()
    return filename


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
    bins = range(0, 20)
    plt.hist(list_of_results, bins=bins, rwidth=0.8, color='#b23000')
    plt.savefig(path)
    plt.clf()
    return ['histogram.png']


def best_fit_slope_and_intercept(xs, ys):
    m = (((mean(xs) * mean(ys)) - mean(xs * ys)) /
         ((mean(xs) * mean(xs)) - mean(xs * xs)))

    b = mean(ys) - m * mean(xs)
    return m, b
