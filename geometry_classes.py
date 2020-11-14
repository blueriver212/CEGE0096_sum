import sys

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

    def __init__(self, points, mbr_xs, mbr_ys):
        """
        Finds the Minimum and Maximum of the MBR polygon.
        :param points: A list of X and Y coordinates
        :param mbr_xs:
        :param mbr_ys:
        """

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
        """
        This idea was taken from Philip Mons, 2017 (Source = philliplemons.com/posts/ray-casting-algorithm)
        :param point_x: X value of a point
        :param point_y: Y value of a point
        :param edge: Two coordinates that make up an edge
        :return: TRUE or FALSE depending on if ray from point intersects with edge
        """

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
        """
        This will take a list of points, and a list of edges, using the cross_edge() function will check
        if a given point crosses any of the edges. If true, the count will increase. Even = Outside, Odd = Inside.

        This is adapted from Rosseta Code (Source: rosettacode.org/wiki/Ray-casting_algorithm#Python)
        :return: Two lists of points, ones that are inside the polygon, ones that are outside.
        """
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
