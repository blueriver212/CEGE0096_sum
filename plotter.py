from collections import OrderedDict

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


class Plotter:

    def __init__(self):
        plt.figure()

    def add_polygon(self, xs, ys):
        plt.fill(xs, ys, 'lightblue', label='Polygon')

    def add_poly_outline(self, xs, ys):
        plt.fill(xs, ys, 'red', fill=None, label='MBR') #need to make the outline red

    def add_point(self, x, y, kind=None):
        if kind == "outside":
            plt.plot(x, y, "ro", label='Outside')
        elif kind == "boundary":
            plt.plot(x, y, "bo", label='Boundary')
        elif kind == "inside":
            plt.plot(x, y, "go", label='Inside')
        else:
            plt.plot(x, y, "ko", label='Unclassified')

    def add_line(self, p1, p2):
        plt.plot(p1, p2, "ro-")

    def show(self):
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        # Taken from Trenton McKinney (2018)
        # Source: https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
        plt.legend(by_label.values(), by_label.keys(),loc='upper center',
                   bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Classification of whether a point is Inside, \n Outside or on the Boundary of a Polygon')
        plt.show()
