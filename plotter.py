from collections import OrderedDict
from geometry_classes import *
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


class Plotter:

    def __init__(self):
        plt.figure()

    def add_polygon(self, xs, ys):
        plt.fill(xs, ys, 'lightblue', label='Polygon')

    def add_poly_outline(self, xs, ys):
        plt.fill(xs, ys, 'red', fill=None, label='MBR')

    def add_point(self, x, y, kind=None):
        if kind == "outside":
            plt.plot(x, y, "ro", label='Outside')
        elif kind == "boundary":
            plt.plot(x, y, "bo", label='Boundary')
        elif kind == "inside":
            plt.plot(x, y, "go", label='Inside')
        else:
            plt.plot(x, y, "ko", label='Unclassified')

    def add_line(self, x1, x2, y1, y2):
        plt.plot([x1, x2], [y1, y2], "ro-", linewidth=0.3, markersize=0, alpha=0.3)

    def show(self, fig_path):
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        # Adapted from Trenton McKinney (2018)
        # Source: https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
        plt.legend(by_label.values(), by_label.keys(), loc='upper center',
                   bbox_to_anchor=(0.5, -0.12), fancybox=True, shadow=True, ncol=5)
        plt.subplots_adjust(bottom=0.2)
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Classification of whether a point is Inside, \n Outside or on the Boundary of a Polygon')
        plt.savefig(fig_path)
        plt.show()
