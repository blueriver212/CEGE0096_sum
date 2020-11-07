from plotter import Plotter
import sys

def import_points(path):
    """
    Imports a CSV from chosen file path, then outputs an ID, X, Y list
    :param path is a directory to the csv file containing polygon points
    :return A tuple with the points' > [0]= IDs, [1] = Xs [2] = Ys:
    """
    points_all, id_, x_, y_ = [], [], [], []
    # Open file
    with open(path, 'r') as f:
        points = f.readlines()
        for row in points:
            row_stripped = row.strip("\n")
            row_split = row_stripped.split(',')
            points_all.append(row_split)

    # append to new lists
    for i in points_all:
        id_.append(i[0])
        x_.append(i[1])
        y_.append(i[2])

    # remove headers, convert to float
    del x_[0]
    del y_[0]
    del id_[0]
    del points_all[0]
    x = [float(i) for i in x_]
    y = [float(i) for i in y_]
    return id_, x, y


class MBR:
    """
    A class that takes a list of x and y coordinates of a polygon and then returns a Minimum Bounding Rectangle
    """

    def __init__(self, xs, ys):
        self.__xs = xs
        self.__ys = ys

        self.min_x = min(self.__xs)
        self.max_x = max(self.__xs)
        self.max_y = max(self.__ys)
        self.min_y = min(self.__ys)

    def min_max(self):
        # coordinates of mbr polygon
        mbr_x = [self.min_x, self.max_x, self.max_x, self.min_x]
        mbr_y = [self.min_y, self.min_y, self.max_y, self.max_y]
        return mbr_x, mbr_y


class InsideMBR:
    """
    Takes x and y points, tests them against the polygon's MBR.
    """

    def __init__(self, x_points, y_points, mbr_xs, mbr_ys):
        self.x_points = x_points
        self.y_points = y_points
        self.__mbr_xs = mbr_xs
        self.__mbr_ys = mbr_ys

        # get the min and max of points for the MBR polygon
        self.max_xmbr = max(self.__mbr_xs)
        self.min_xmbr = min(self.__mbr_xs)
        self.max_ymbr = max(self.__mbr_ys)
        self.min_ymbr = min(self.__mbr_ys)

    def is_inside(self):
        """
        Tests whether a random set of points are within the polygon's MBR
        :return: X and Y coordinates, either in or out.
        """
        coord_in_mbr = []
        coord_out_mbr = []
        for i in range(len(self.x_points)):
            if self.min_xmbr <= self.x_points[i] <= self.max_xmbr and self.min_ymbr <= self.y_points[i] <= self.max_ymbr:
                coord_in_mbr.append((self.x_points[i], self.y_points[i]))
            else:
                coord_out_mbr.append((self.x_points[i], self.y_points[i]))
        return coord_in_mbr, coord_out_mbr


class Inside:
    """
    This will determine whether a list of points are within a polygon.
    It will also return if it is on a vertex and a boundary.
    """
    def __init__(self, coords, poly):
        self.__coords = coords
        self.__poly = poly

    def on_vertex(self):
        # If x,y pairing is in poly file then it is a vertex of polygon.
        res = [i for i in self.__coords if i in self.__poly]
        return res

    def on_line_func(self, x, x1, x2, y, y1, y2):

        """
        equation to test whether a point is on a line defined by (x1, y1) and (x2, y2)
        :param x: X coordinate of a the chosen point
        :param x1: X coordainte of a polygon points
        :param x2: X coordainte of the other polygon point
        :param y: Y coordainte of the chosen point
        :param y1: X coordainte of a polygon points
        :param y2: Y coordainte of the other polygon point
        :return: True if the point is on the line, False if it is not.
        """

        if (x2-x1) == 0:
            if x == x1 or x == x2:
                return True  # This this stops the function returning a math error
        else:
            y_temp = ((x - x1) / (x2 - x1)) * (y2 - y1) + y1  # equation for if point is on the line
            if y == y_temp:
                return True
            else:
                return False

    def points_on_line(self):
        # find values for on_line_func
        on_line = []
        # not_classified = []
        # remove the vertex points for calculation, as already on boundary
        vertex_points = self.on_vertex()
        print(vertex_points)
        points_to_test = [i for i in self.__coords if i not in vertex_points]

        for i in range(len(points_to_test)):

            x = points_to_test[i][0]
            y = points_to_test[i][1]

            for j in range(1, len(self.__poly)):

                one_coord = self.__poly[j-1] # as range starts at 1, this will look at the first point in the list
                two_coord = self.__poly[j]
                x1 = one_coord[0]
                y1 = one_coord[1]
                x2 = two_coord[0]
                y2 = two_coord[1]

                #use above on_line() to calculate if point is on the line but also within the two points
                if self.on_line_func(x, x1, x2, y, y1, y2) == True:
                    if y >= min(y1, y2) and y <= max(y1, y2) and x >= min(x1, x2) and x <= max(x1,x2):  # little mbr algorithm
                         on_line.append((x, y))
                    # else:
                    #     not_classified.append((x,y)) #not classified points

        not_classified = [i for i in points_to_test if i not in on_line]
        return on_line, not_classified

class Polygon:


    def __init__(self, points, poly):
        """
        points: a list of points in clockwise order
        """
        self.__points = points
        self.__poly = poly
        self.edge_list = []

        # Create an edge list from the polygon file
        for i, p in enumerate(self.__poly):
            p1 = p
            p2 = self.__poly[(i+1) % len(self.__poly)]
            self.edge_list.append((p1, p2))

    def cross_edge(self, point_x, point_y, edge):

        _huge = sys.float_info.max  # _huge acts as infinity for ray
        _tiny = 0.0000001  # _tiny is used to make sure the points are not on verticies

        A, B = edge[0], edge[1]
        if A[1] > B[1]:
            A, B = B, A

        A_x, A_y = A[0], A[1]
        B_x, B_y = B[0], B[1]

        # make sure that point does not intercept a vertex
        if point_y == A_y or point_y == B_y:
            point_y += _tiny  # add the small value

        if point_x == A_x or point_x == B_x:
            point_x += _tiny  # add the small value

        intersect = False

        if (point_y > B_y or point_y < A_y) or (point_x > max(A_x, B_x)):
            # the ray does not intersect with the edge
            return intersect

        if point_x < min(A_x, B_x):
            intersect = True
            return intersect


        try:
            m_edge = (B_y - A_y) / (B_x - A_x)
        except ZeroDivisionError:
            m_edge = _huge

        try:
            m_point = (point_y - B_y) / (point_x - B_x)
        except ZeroDivisionError:
            m_point = _huge

        if m_point < m_edge:
            # The ray intersects with the edge
            # count += 1
            intersect = True

        return intersect

    def rca(self):

        inside = []
        outside = []
        for point in self.__points:
            count = 0 #number of times it crosses an edge
            point_x = point[0]
            point_y = point[1]

            for edge in self.edge_list:
                is_inside = self.cross_edge(point_x, point_y, edge)
                if is_inside == True:
                    count += 1

            if count % 2 == 0:
                outside.append(point)
            else:
                inside.append(point)
            print(point)
            print(count)
        return inside, outside


class RCA:
    """
    This takes all of the points that have not already been classified and conducts the RCA analysis.
    """
    def __init__(self, points, poly):
        # self.__xs = xs
        # self.__ys = ys
        self.__points = points
        self.__poly = poly

        #self.__points = zip(self.__xs, self.__ys) # make list of coordinate tuples
        max_x = max(x for x, y in self.__poly) + 1 # Gives you 1 more x point in the x direction

    def lines(self):
        pass

    def slope(self, x1, x2, y1, y2):
        #return the slope of two points
        m = (y2-y1)/(x2-x1)
        return m

    def y_intercept(self):
        b1 = self.y1 - (self.x1 * self.m1)
        return b1

    def intersection(self, x1, x2, y1, y2, x3, x4, y3, y4):
        m1 = self.slope(x1, x2, y1, y2) # slope of the first line
        m2 = self.slope(x3, x4, y3, y4) # slope of the second line

        # calculate the point at which they intercept
        x = (self.b2 -self.b1)/(self.m1 - self.m2)
        y = ((self.b2 * self.m1) - (self.b1*self.m2))/(self.m1 - self.m2)
        return x, y

    def do_intersect(self):
        """
        tests whether two points intersect
        :return:
        """

    def get_intersection(self):
        intersection_points = []

        if self.do_intersect() == True:
            for i in range(1, len(self.__poly)):
                x1_ = self.__poly[i-1][0]
                y1_ = self.__poly[i-1][1]

                x2_ = self.__poly[i][0]
                y2_ = self.__poly[i][1]

                for j in range(len(self.__points)):
                    x3_ = self.__points([j][0]) #error seems to be here, list not callable
                    y3_ = self.__points([j][1])

                    x4_ = self.max_x  #Always tends to the same x value
                    y4_ = y3_ #Always on the same horizontal plane, so same as y4

                    test_intersection = self.intersection(x1_, x2_, y1_, y2_, x3_, x4_, y3_, y4_)
                    intersection_points.append(test_intersection)

        return intersection_points


def main(polygon, input):
    # # print("read polygon.csv")
    # # print("read input.csv")
    # # print("categorize points")
    # # print("write output.csv")
    # # print("plot polygon and points")
    plotter = Plotter()

    # Import the polygon, export xs and ys, and plot
    polygon_points = import_points(polygon)
    x_poly = polygon_points[1]
    y_poly = polygon_points[2]
    poly = list(zip(x_poly, y_poly))
    plotter.add_polygon(x_poly, y_poly)

    # calculate and plot the MBR polygon
    imp = MBR(x_poly, y_poly)
    mbr = imp.min_max()
    plotter.add_poly_outline(mbr[0], mbr[1])

    # import the individual points
    points = import_points(input)
    x = points[1]
    y = points[2]

    x = [2]
    y = [2]


    # Test whether these points are within the Polygon's MBR
    poly_mbr = InsideMBR(x, y, mbr[0], mbr[1])
    mbr_ = poly_mbr.is_inside()
    coord_inside_mbr = mbr_[0]
    coord_outside_mbr = mbr_[1]
    test = Inside(coord_inside_mbr, poly)

    # return the points on the vertex of the geometry
    vertex_points = test.on_vertex()
    res = test.points_on_line()
    coord_boundary = res[0]
    not_classified = res[1]  # get the not yet classified points

    # There are actually duplicates of points which can be seen here (why there are less points on graph)
    # count = {}
    # for coordinate in not_classified:
    #     count.setdefault(coordinate, 0)
    #     count[coordinate] += 1
    # print(count)
    # input the final points into the RCA

    final_round = Polygon(not_classified, poly)
    rca = final_round.rca()
    rca_inside = rca[0]
    rca_outside = rca[1]




    # Plotting
    # for i in range(len(coord_inside_mbr)):
    #     plotter.add_point(coord_inside_mbr[i][0], coord_inside_mbr[i][1], 'outside')
    # for i in range(len(vertex_points)):
    #     plotter.add_point(vertex_points[i][0], vertex_points[i][1], 'boundary')
    # for i in range(len(coord_outside_mbr)):
    #     plotter.add_point(coord_outside_mbr[i][0], coord_outside_mbr[i][1], 'outside')
    # for i in range(len(coord_boundary)):
    #      plotter.add_point(coord_boundary[i][0], coord_boundary[i][1], 'boundary')
    for i in range(len(rca_outside)):
        plotter.add_point(rca_outside[i][0], rca_outside[i][1], 'outside')
    for i in range(len(rca_inside)):
        plotter.add_point(rca_inside[i][0], rca_inside[i][1], 'inside')
    # for i in range(len(not_classified)):
    #     plotter.add_point(not_classified[i][0], not_classified[i][1], 'inside')
    # for i in range(len(coord_boundary)):
    #     plotter.add_point(coord_boundary[i][0], coord_boundary[i][1])



    plotter.show()


if __name__ == "__main__":
    # To Do
    # > Need to add a function that you can also add the output file path at the terminal

    # input your file path of the polygon, the points into the main function
    polygon = 'polygon.csv' # input('Type the filename of your polygon (include .csv):')
    input = 'input.csv' # input('Type the filename of your testing points (include .csv):')

    main(polygon, input)
