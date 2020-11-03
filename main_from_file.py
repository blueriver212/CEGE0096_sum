from plotter import Plotter


def import_csv(path):
    point_list = []
    id = []
    x = []
    y = []
    # Open file
    with open(path, 'r') as f:
        points = f.readlines()
        for row in points:
            row_stripped = row.strip("\n")
            row_split = row_stripped.split(',')
            point_list.append(row_split)


    # append to new lists
    for i in point_list:
        id.append(i[0])
        x.append(i[1])
        y.append(i[2])

    # remove the headers
    del x[0]
    del y[0]
    del id[0]

    return(id, x, y)
    # print(point_list)
    # print(id)
    # print(x)
    # print(y)

class MinBR:


    def __init__(self, xs, ys):
        self.__xs = xs
        self.__ys = ys

    def min_max(self):
        min_x = min(self.__xs)
        max_x = max(self.__xs)
        max_y = max(self.__ys)
        min_y = min(self.__ys)

        #coordinates of mbr polygon
        mbr_x = [min_x, max_x, max_x, min_x]
        mbr_y = [min_y, min_y, max_y, max_y]
        return mbr_x, mbr_y


def main():
    plotter = Plotter()

    #Plot the points from a csv
    data = import_csv('input.csv')
    x_ = data[1]
    x = [int(float(i)) for i in x_]
    y_ = data[2]
    y = [int(float(i)) for i in y_]
    for i in range(len(x)):
        plotter.add_point(x[i], y[i])

    # print("read polygon.csv")
    # print("read input.csv")
    # print("categorize points")
    # print("write output.csv")
    # print("plot polygon and points")

    imp = MinBR(x, y)
    mbr = imp.min_max()
    print(mbr)
    plotter.add_polygon(mbr[0], mbr[1])
    plotter.show()

if __name__ == "__main__":
    main()
