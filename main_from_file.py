from plotter import Plotter
import sys
import os

def import_csv(path):
    """
    Imports a CSV from chosen file path, then outputs an ID, X, Y list
    :param path is a directory to the csv file containing polygon points
    :return A tuple with the points' > [0]= IDs, [1] = Xs [2] = Ys:
    """
    points_all, x_, y_, id_ = [], [], [], []

    with open(path, 'r') as f:
        #check that the input is CSV
        # for each in f:
        #     if len(f.split(',''')) > 2:
        #         raise Exception
        # print('Valid CSV')

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

    # del the first column
    del id_[0], x_[0], y_[0]

    # # convert to float
    x = [float(i) for i in x_]
    y = [float(i) for i in y_]

    return id_, x, y, points_all

class MBR:

    def __init__(self, poly):
        self.__poly = poly

        self.__poly_xs = self.__poly[1]
        self.__poly_ys = self.__poly[2]

        self.min_x = min(self.__poly_xs)
        self.max_x = max(self.__poly_xs)
        self.min_y = min(self.__poly_ys)
        self.max_y = max(self.__poly_ys)

    def mbr_coords(self):
        # coordinates of mbr polygon
        mbr_x = [self.min_x, self.max_x, self.max_x, self.min_x]
        mbr_y = [self.min_y, self.min_y, self.max_y, self.max_y]
        return mbr_x, mbr_y


class InsideMBR:
    """
    Takes x and y points, tests them against the polygon's MBR.
    """
    def __init__(self, points, mbr_xs, mbr_ys):
        self.xpoints = points[0]
        self.ypoints = points[1]
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
        for i in range(len(self.xpoints)):
            if self.min_xmbr <= self.xpoints[i] <= self.max_xmbr and self.min_ymbr <= self.ypoints[i] <= self.max_ymbr:
                coord_in_mbr.append((self.xpoints[i], self.ypoints[i]))
            else:
                coord_out_mbr.append((self.xpoints[i], self.ypoints[i]))
        return coord_in_mbr, coord_out_mbr


class Boundary:
    """
    This will determine whether a list of points are within a polygon.
    It will also return if it is on a vertex and a boundary.
    """

    def __init__(self, coords, poly):
        self.__coords = coords
        self.__poly = poly

    def on_vertex(self):
        # If x,y pairing is in poly file then it is a vertex of polygon.
        points_on_vertex = [i for i in self.__coords if i in self.__poly]
        return points_on_vertex

    @staticmethod
    def on_line_func( x, x1, x2, y, y1, y2):
        """
        equation to test whether a point is on a line defined by (x1, y1) and (x2, y2)
        :param x: X coordinate of a the chosen point
        :param x1: X coordinate of a polygon points
        :param x2: X coordinate of the other polygon point
        :param y: Y coordinate of the chosen point
        :param y1: X coordinate of a polygon points
        :param y2: Y coordinate of the other polygon point
        :return: True if the point is on the line, False if it is not.
        """
        if (x2 - x1) == 0:
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

        # remove the vertex points for calculation, as already on boundary
        vertex_points = self.on_vertex()
        points_to_test = [i for i in self.__coords if i not in vertex_points]

        for i in range(len(points_to_test)):

            x = points_to_test[i][0]
            y = points_to_test[i][1]

            for j in range(1, len(self.__poly)):

                one_coord = self.__poly[j - 1]  # as range starts at 1, this will look at the first point in the list
                two_coord = self.__poly[j]
                x1 = one_coord[0]
                y1 = one_coord[1]
                x2 = two_coord[0]
                y2 = two_coord[1]

                # use above on_line() to calculate if point is on the line but also within the two points
                if self.on_line_func(x, x1, x2, y, y1, y2):
                    if min(y1, y2) <= y <= max(y1, y2) and min(x1, x2) <= x <= max(x1, x2):  # little mbr algorithm
                        on_line.append((x, y))
                    # else:
                    #     not_classified.append((x,y)) #not classified points

        not_classified = [i for i in points_to_test if i not in on_line]
        return on_line, not_classified


class RayCasting:

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
            p2 = self.__poly[(i + 1) % len(self.__poly)]
            self.edge_list.append((p1, p2))

    @staticmethod
    def cross_edge(point_x, point_y, edge):

        _huge = sys.float_info.max  # _huge acts as infinity for ray
        _tiny = 0.0000001  # _tiny is used to make sure the points are not on vertices

        # Ensures that the Y values of A is lower than B
        A, B = edge[0], edge[1]
        if A[1] > B[1]:
            A, B = B, A

        A_x, A_y = A[0], A[1]
        B_x, B_y = B[0], B[1]

        # If point intercepts a vertex, then add a small y increase to move it off the path
        if point_y == A_y or point_y == B_y:
            point_y += _tiny

        # If point intercepts a vertex, then add a small x increase to move it off the path
        if point_x == A_x or point_x == B_x:
            point_x += _tiny
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
            count = 0  # number of times it crosses an edge
            point_x = point[0]
            point_y = point[1]

            for edge in self.edge_list:
                is_inside = self.cross_edge(point_x, point_y, edge)
                if is_inside:
                    count += 1

            if count % 2 == 0:
                outside.append(point)
            else:
                inside.append(point)

        return inside, outside


def main(input_polygon, input_points):
    plotter = Plotter()

    # calculate and plot the MBR polygon
    polygon_points = import_csv(input_polygon)
    poly = list(zip(polygon_points[1], polygon_points[2]))
    MBR_values = MBR(polygon_points)
    mbr = MBR_values.mbr_coords()
    plotter.add_polygon(polygon_points[1], polygon_points[2])
    plotter.add_poly_outline(mbr[0], mbr[1])

    # import the individual points
    raw_points = import_csv(input_points)
    points_id, points = raw_points[0], [raw_points[1], raw_points[2]]
    points_tuple = list(zip(raw_points[1], raw_points[2]))
    original_points = [points_id, points_tuple]

    # Test whether these points are within the Polygon's MBR
    poly_mbr = InsideMBR(points, mbr[0], mbr[1])
    mbr_ = poly_mbr.is_inside()
    coord_inside_mbr = mbr_[0]
    coord_outside_mbr = mbr_[1]

    # return the points on the vertex of the geometry
    test = Boundary(coord_inside_mbr, poly)
    vertex_points = test.on_vertex()
    res = test.points_on_line()
    coord_boundary = res[0]
    not_classified = res[1]

    # Enter the non classified points into the RCA
    final_round = RayCasting(not_classified, poly)
    rca = final_round.rca()
    rca_inside = rca[0]
    rca_outside = rca[1]


    # plot and append all points
    outside_pnts = []
    boundary_pnts = []
    inside_pnts = []
    for i in range(len(vertex_points)):
        plotter.add_point(vertex_points[i][0], vertex_points[i][1], 'boundary')
        boundary_pnts.append(vertex_points[i])
    # for i in range(len(not_classified)):
    #     plotter.add_point(not_classified[i][0], not_classified[i][1])
    for i in range(len(coord_outside_mbr)):
        plotter.add_point(coord_outside_mbr[i][0], coord_outside_mbr[i][1], 'outside')
        outside_pnts.append(coord_outside_mbr[i])
    # for i in range(len(coord_inside_mbr)):
    #     plotter.add_point(coord_inside_mbr[i][0], coord_inside_mbr[i][1], 'inside')
    for i in range(len(coord_boundary)):
        plotter.add_point(coord_boundary[i][0], coord_boundary[i][1], 'boundary')
        boundary_pnts.append(coord_boundary[i])
    for i in range(len(rca_outside)):
        plotter.add_point(rca_outside[i][0], rca_outside[i][1], 'outside')
        outside_pnts.append(rca_outside[i])
    for i in range(len(rca_inside)):
        plotter.add_point(rca_inside[i][0], rca_inside[i][1], 'inside')
        inside_pnts.append(rca_inside[i])


    # this provides a third list with the points classification
    boundary = [boundary_pnts, ['boundary'] * len(boundary_pnts)]
    inside = inside_pnts, ['inside'] * len(inside_pnts)
    outside = outside_pnts, ['outside'] * len(outside_pnts)

    # join all the points together in one list
    boundary[0].extend(inside[0])
    boundary[1].extend(inside[1])
    boundary[0].extend(outside[0])
    boundary[1].extend(outside[1])

    # Finding the classification for each point and ID in original list
    original_points = [(y, x) for x, y in zip(original_points[0], original_points[1])]
    out_list = []
    for point, flag in original_points:
        index = boundary[0].index(point)
        x, y = point
        out_list.append((flag, x, y, boundary[1][index]))

    #for point, flag in final_points
    #plot all of the rays
    #every point
    # max_x_in_points = max(raw_points[1])
    # rca_rays = [raw_points[1], raw_points[2], [max_x_in_points] * 100, raw_points[2]]
    # print(rca_rays)
    # for i in range(len(rca_rays)):
    #     plotter.add_point(rca_rays[i][2], rca_rays[i][3], 'outside')#, (rca_rays[i][2], rca_rays[i][3]))




    #need to create a list

    plotter.show()

if __name__ == "__main__":
    # To Do
    # > Need to add a function that you can also add the output file path at the terminal

    # input your file path of the polygon, the points into the main function
    file_list = os.listdir()
    print(file_list)
    while True:
        try:
            # Note: Python 2.x users should us raw_input, the equivalent of 3.x's input
            input_polygon = input('Type the filename of your polygon (include .csv):')
            if ".csv" not in input_polygon:
                raise(ValueError)
            if input_polygon not in file_list:
                raise(FileNotFoundError)
        except ValueError:
            print('Name must end with .csv')
        except FileNotFoundError:
            print('This file is not in the folder.')
            continue
        else:
            break
    while True:
        try:
            # Note: Python 2.x users should us raw_input, the equivalent of 3.x's input
            input_points = input('Type the filename of your testing points (include .csv):')
            if ".csv" not in input_points:
                    raise (ValueError)
            if input_points not in file_list:
                raise(FileNotFoundError)
        except ValueError:
            print('Name must end with .csv')
        except FileNotFoundError:
            print('This file is not in the folder.')
            continue
        else:
            break

    main(input_polygon, input_points)
