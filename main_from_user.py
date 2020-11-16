import os
from plotter import Plotter
from main_from_file import *
from geometry_classes import *


def user():

    avail_files = os.listdir()
    while True:
        try:
            path = input("Input the name of the relative path of your polygon (include .csv): ")
            if ".csv" not in path:
                raise ValueError
            if path not in avail_files:
                raise FileNotFoundError
            break
        except ValueError:
            print('Must end with .csv')
        except FileNotFoundError:
            print('This file is not in the folder.')

    point = []
    while True:
        try:
            input_points = input('Enter your coordinates (x,y format):')
            to_float = [float(input_points.split(',')[0]), float((input_points.split(',')[1]))]
            break
        except ValueError:
            print('Please check the format of your points!')
    point.append(to_float)

    return point, path


def main():
    plotter = Plotter()

    user_inputs = user()
    points = user_inputs[0]
    path = user_inputs[1]

    res = import_csv(path)
    poly_x, poly_y, poly = res[1], res[2], list(zip(res[1], res[2]))
    plotter.add_polygon(res[1], res[2])

    # first create the mbr from the polygon
    mbr = MBR(res)
    poly_mbr = mbr.mbr_coordinates()
    plotter.add_poly_outline(poly_mbr[0], poly_mbr[1])

    # print("Insert point information")
    x = points[0][0]
    y = points[0][1]
    point = [(x, y)]

    # calculate if the point is inside the MBR
    mbr_test = InsideMBR(([x], [y]), poly_mbr[0], poly_mbr[1])
    mbr_output = mbr_test.is_inside()
    is_inside_mbr, is_outside_mbr = mbr_output[0], mbr_output[1]

    # plot the point if outside Minimum Boundary Rectangle
    if len(is_inside_mbr) == 0:
        plotter.add_point(is_outside_mbr[0][0], is_outside_mbr[0][1], 'outside')

    # If inside MBR check if a vertex or on boundary
    inside_mbr_points = Boundary(is_inside_mbr, poly)
    on_vertex = inside_mbr_points.on_vertex()

    classification = []
    # First check and plot the point if on vertex
    if len(on_vertex) != 0:
        plotter.add_point(on_vertex[0][0], on_vertex[0][1], 'boundary')
        classification.append('boundary')
    else:
        point_on_line = inside_mbr_points.points_on_line()

        # Then if the point is on boundary
        if len(point_on_line[0]) != 0:
            plotter.add_point(point_on_line[0][0][0], point_on_line[0][0][1], 'boundary')
            classification.append('boundary')

        else:
            not_classified = RayCasting(point, poly)
            final_round = not_classified.rca()
            inside_poly = final_round[0]
            outside_poly = final_round[1]

            # Plot if inside or outside polygon
            if len(inside_poly) != 0:
                plotter.add_point(inside_poly[0][0], inside_poly[0][1], 'inside')
                classification.append('inside')
            else:
                plotter.add_point(outside_poly[0][0], outside_poly[0][1], 'outside')
                classification.append('outside')

    if classification[0] == 'boundary':
        print(f'Your chosen point is on the {classification[0]} of the polygon')
    else:
        print(f'Your chosen point is {classification[0]} the polygon')

    # Plot and save the file to your relative path
    fig_path = 'User Points Plot.png'
    plotter.show(fig_path)


if __name__ == "__main__":
    main()
