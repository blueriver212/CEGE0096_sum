from plotter import Plotter
import main_from_file as mf
from main_from_file import *

def main():
    plotter = Plotter()

    print("read polygon.csv")
    path = input("Input the name of the relative path of your csv (include .csv): ")
    res = mf.import_csv(path)
    poly_x, poly_y, poly = res[1], res[2], list(zip(res[1], res[2]))
    plotter.add_polygon(res[1], res[2])

    # first create the mbr from the polygon
    mbr = MBR(poly_x, poly_y)
    poly_mbr = mbr.min_max()
    plotter.add_poly_outline(poly_mbr[0], poly_mbr[1])

    # # print("Insert point information")
    x = float(input("x coordinate: "))
    y = float(input("y coordinate: "))

    point = [(x, y)]

    # calculate if the point is inside the MBR
    mbr_test = InsideMBR([x], [y], poly_mbr[0], poly_mbr[1])
    mbr_output = mbr_test.is_inside()
    is_inside_mbr = mbr_output[0]
    is_outside_mbr = mbr_output[1]

    # plot the point if outside Minimum Boundary Rectangle
    if len(is_inside_mbr) == 0:
        plotter.add_point(is_outside_mbr[0][0], is_outside_mbr[0][1], 'outside')

    #Check if it is on a vertex or line
    inside_mbr_points = Inside(is_inside_mbr, poly)
    on_vertex = inside_mbr_points.on_vertex()

    # plot point if on vertex
    if len(on_vertex) != 0:
        plotter.add_point(on_vertex[0][0], on_vertex[0][1], 'boundary')
    else:
        point_on_line = inside_mbr_points.points_on_line()

    # check if the point is on boundary
    if len(point_on_line[0]) != 0:
        plotter.add_point(point_on_line[0][0][0], point_on_line[0][0][1], 'boundary')
    else:
        not_classified = Polygon(point, poly)
        final_round = not_classified.rca()
        inside_poly = final_round[0]
        outside_poly = final_round[1]

        # Plot if inside or outside polygon
        if len(inside_poly) !=0:
            plotter.add_point(inside_poly[0][0], inside_poly[0][1], 'inside')
        else:
            plotter.add_point(outside_poly[0][0], outside_poly[0][1], 'outside')

    # print("categorize point")
    #
    # print("plot polygon and point")
    plotter.show()


if __name__ == "__main__":
    main()
