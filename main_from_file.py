from plotter import Plotter


def import_points(path):
    """
    Imports a CSV from chosen file path, then outputs an ID, X, Y list
    :param path is a directory to the csv file containing polygon points:
    :return A tuple with the points' > [0]= IDs, [1] = Xs [2] = Ys:
    """
    points_all = []
    id = []
    x_ = []
    y_ = []
    # Open file
    with open(path, 'r') as f:
        points = f.readlines()
        for row in points:
            row_stripped = row.strip("\n")
            row_split = row_stripped.split(',')
            points_all.append(row_split)


    # append to new lists
    for i in points_all:
        id.append(i[0])
        x_.append(i[1])
        y_.append(i[2])

    # remove headers, convert to float
    del x_[0]
    del y_[0]
    del id[0]
    del points_all[0]
    x = [float(i) for i in x_]
    y = [float(i) for i in y_]
    return(id, x, y)


class MinBR:

    def __init__(self, xs, ys):
        self.__xs = xs
        self.__ys = ys

        self.min_x = min(self.__xs)
        self.max_x = max(self.__xs)
        self.max_y = max(self.__ys)
        self.min_y = min(self.__ys)

    def min_max(self):
        #coordinates of mbr polygon
        mbr_x = [self.min_x, self.max_x, self.max_x, self.min_x]
        mbr_y = [self.min_y, self.min_y, self.max_y, self.max_y]
        return mbr_x, mbr_y

class InsideMBR:

    def __init__(self, x_points, y_points, mbr_xs, mbr_ys):
        self.x_points = x_points
        self.y_points = y_points
        self.__mbr_xs = mbr_xs
        self.__mbr_ys = mbr_ys

        #get the min and max of the MBR polygon
        self.max_xmbr = max(self.__mbr_xs)
        self.min_xmbr = min(self.__mbr_xs)
        self.max_ymbr = max(self.__mbr_ys)
        self.min_ymbr = min(self.__mbr_ys)

    def is_inside(self):
        kind = []
        for i in range(len(self.x_points)):
            if self.min_xmbr <= self.x_points[i] <= self.max_xmbr and self.min_ymbr <= self.y_points[i] <= self.max_ymbr:
                kind.append('inside')
            else:
                kind.append('outside')
        return self.x_points, self.y_points, kind

class RCA(MinBR):

    def __init__(self, xs, ys, poly):
        self.___xs = xs
        self.__ys = ys
        self.__poly = poly




def main():
    # print("read polygon.csv")
    # print("read input.csv")
    # print("categorize points")
    # print("write output.csv")
    # print("plot polygon and points")
    plotter = Plotter()

    #Import the points and add to individual lists
    polygon_points = import_points('polygon.csv')
    x_poly = polygon_points[1]
    y_poly = polygon_points[2]

    #plot the Polygon
    plotter.add_polygon(x_poly, y_poly)

    #calculate and plot the MBR polygon
    imp = MinBR(x_poly, y_poly)
    mbr = imp.min_max()
    print(mbr)
    plotter.add_poly_outline(mbr[0], mbr[1])


    # import the individual points
    points = import_points('input.csv')
    x = points[1]
    y = points[2]

    #Test whether these points are within the Polygon's MBR
    pmbr = InsideMBR(x, y, mbr[0], mbr[1])
    mbr_ = pmbr.is_inside()
    MinBR_x = mbr_[0]
    MinBR_y = mbr_[1]
    MinBR_kind = mbr_[2]


    for i in range(len(MinBR_x)):
        plotter.add_point(MinBR_x[i], MinBR_y[i], MinBR_kind[i])

    #plotter.show()

if __name__ == "__main__":
    main()
