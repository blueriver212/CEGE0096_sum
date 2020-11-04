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


class Inside:

    def __init__(self, coords, poly):
        self.__coords = coords
        self.__poly = poly

    def on_vertex(self):
        #If x,y pairing is in poly file then it is a vertex of polygon.
        res = [i for i in self.__coords if i in self.__poly]
        return res

    def on_line_func(self, x, x1, x2, y, y1, y2):
        # equation to test whether a point is on a line defined by (x1, y1) and (x2, y2)
        if (x2-x1) == 0:
            if x == x1 or x == x2:
                #print("y: {}, y1: {}, y2: {}".format(y,y1,y2))
                return True # if line is x = 0
        else:
            y_temp = ((x - x1) / (x2 - x1)) * (y2 - y1) + y1
            if y == y_temp:
                return True
            else:
                return False

    def points_on_line(self):
        # find values for on_line_func
        coordinate = []
        vertex_points = self.on_vertex()
        points_to_test = [i for i in self.__coords if i not in vertex_points]
        count = 0
        for i in range(len(points_to_test)):

            x = points_to_test[i][0]
            y = points_to_test[i][1]

            for j in range(1, len(self.__poly)):

                one_coord = self.__poly[j-1]
                two_coord = self.__poly[j]
                x1 = one_coord[0]
                y1 = one_coord[1]
                x2 = two_coord[0]
                y2 = two_coord[1]

                if self.on_line_func(x, x1, x2, y, y1, y2) == True: # or self.on_line_func(x, x1, x2, y, y1, y2) == y:
                    if y >= min(y1, y2) and y <= max(y1, y2) and x >= min(x1, x2) and x <= max(x1,x2):  # little mbr algorithm  and
                         coordinate.append((x, y))

        return coordinate

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
        coord_in_mbr = []
        coord_out_mbr = []
        for i in range(len(self.x_points)):
            if self.min_xmbr <= self.x_points[i] <= self.max_xmbr and self.min_ymbr <= self.y_points[i] <= self.max_ymbr:
                coord_in_mbr.append((self.x_points[i], self.y_points[i]))
            else:
                coord_out_mbr.append((self.x_points[i], self.y_points[i]))
        return coord_in_mbr, coord_out_mbr

class RCA(MinBR):

    def __init__(self, xs, ys, poly):
        self.___xs = xs
        self.__ys = ys
        self.__poly = poly


def main():
    # # print("read polygon.csv")
    # # print("read input.csv")
    # # print("categorize points")
    # # print("write output.csv")
    # # print("plot polygon and points")
    plotter = Plotter()
    #
    #Import the points and add to individual lists
    polygon_points = import_points('polygon.csv')
    x_poly = polygon_points[1]
    y_poly = polygon_points[2]
    poly = list(zip(x_poly, y_poly))
    #plot the Polygon
    plotter.add_polygon(x_poly, y_poly)

    #calculate and plot the MBR polygon
    imp = MinBR(x_poly, y_poly)
    mbr = imp.min_max()
    plotter.add_poly_outline(mbr[0], mbr[1])

    # import the individual points
    points = import_points('input.csv')
    x = points[1]
    y = points[2]



    #Test whether these points are within the Polygon's MBR
    pmbr = InsideMBR(x, y, mbr[0], mbr[1])
    mbr_ = pmbr.is_inside()
    coord_inside = mbr_[0]
    coord_outside = mbr_[1]

    test = Inside(coord_inside, poly)
    # return the points on the vertex of the geometry
    vertex_points = test.on_vertex()

    # test whether the you can classify points on polygons

    coord_boundary = test.points_on_line()

    #plotting
    for i in range(len(coord_inside)):
        plotter.add_point(coord_inside[i][0], coord_inside[i][1], 'inside')
    for i in range(len(vertex_points)):
        plotter.add_point(vertex_points[i][0], vertex_points[i][1])
    for i in range(len(coord_outside)):
        plotter.add_point(coord_outside[i][0], coord_outside[i][1], 'outside')
    for i in range(len(coord_boundary)):
        plotter.add_point(coord_boundary[i][0], coord_boundary[i][1], 'boundary')


    plotter.show()
if __name__ == "__main__":
    main()
