from plotter import Plotter
from geometry_classes import *
import sys
import os

def user():
    # input your file path of the polygon, the points into the main function
    file_list = os.listdir()
    while True:
        """
        This error handling ensures that the file contains .csv and that it is exists in relative path
        Original Adapted from:
        stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
        Stack Overflow User: Kevin, 2017 
        """
        try:
            input_polygon = input('Type the filename of your polygon (include .csv):')
            if ".csv" not in input_polygon:
                raise (ValueError)
            if input_polygon not in file_list:
                raise (FileNotFoundError)
        except ValueError:
            print('Name must end with .csv')
        except FileNotFoundError:
            print('This file is not in the folder.')
            continue
        else:
            break

    while True:
        try:
            input_points = input('Type the filename of your testing points (include .csv):')
            if ".csv" not in input_points:
                raise ValueError
            if input_points not in file_list:
                raise FileNotFoundError
        except ValueError:
            print('Name must end with .csv')
        except FileNotFoundError:
            print('This file is not in the folder.')
            continue
        else:
            break

    while True:
        try:
            out_path = input('Type the name of your output file (include .csv):')
            if ".csv" not in out_path:
                raise ValueError
            if out_path in file_list:
                raise FileExistsError
        except ValueError:
            print('Name must end with .csv')
        except FileExistsError:
            print('File already exists')
            continue
        else:
            break

    while True:
        try:
            fig_path = input('Type the name of your output plot (include .png):')
            if ".png" not in fig_path:
                raise ValueError
            if out_path in file_list:
                raise FileExistsError
        except ValueError:
            print('Name must end with .png')
        except FileExistsError:
            print('File already exists')
            continue
        else:
            break

    return input_polygon, input_points, out_path, fig_path


def import_csv(path):
    """
    Imports a CSV from chosen file path, then outputs an ID, X, Y list
    :param path is a directory to the csv file containing polygon points
    :return A tuple with the points' > [0]= IDs, [1] = Xs [2] = Ys:
    """
    points_all, x_, y_, id_ = [], [], [], []
    with open(path, 'r') as f:
        points = f.readlines()
        for row in points:
            row_stripped = row.strip("\n")
            row_split = row_stripped.split(',')
            points_all.append(row_split)

    for i in points_all:
        id_.append(i[0])
        x_.append(i[1])
        y_.append(i[2])

    del id_[0], x_[0], y_[0]
    x = [float(i) for i in x_]
    y = [float(i) for i in y_]

    return id_, x, y, points_all


def export_csv(output_path, identification, classification):

    identification.insert(0, 'id')
    classification.insert(0, 'classification')
    out_file = [identification, classification]

    with open(output_path, 'w') as f:
        for i in range(len(out_file[0])):
            f.write(out_file[0][i])
            f.write(',')
            f.write(out_file[1][i])
            f.write('\n')


def main():
    plotter = Plotter()
    errors = user()

    input_polygon = errors[0]
    input_points = errors[1]
    out_path = errors[2]
    fig_path = errors[3]

    # calculate and plot the MBR polygon
    polygon_points = import_csv(input_polygon)
    poly = list(zip(polygon_points[1], polygon_points[2]))
    MBR_values = MBR(polygon_points)
    mbr = MBR_values.mbr_coordinates()
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
    coord_inside_mbr, coord_outside_mbr = mbr_[0], mbr_[1]

    # return the points on the vertex of the geometry
    test = Boundary(coord_inside_mbr, poly)
    vertex_points = test.on_vertex()
    res = test.points_on_line()
    coord_boundary, not_classified = res[0], res[1]

    # Enter the non classified points into the RCA
    final_round = RayCasting(not_classified, poly)
    rca = final_round.rca()
    rca_inside, rca_outside = rca[0], rca[1]

    # plot and append all points to individual classified lists
    outside_points, boundary_points, inside_points = [], [], []
    for i in range(len(vertex_points)):
        plotter.add_point(vertex_points[i][0], vertex_points[i][1], 'boundary')
        boundary_points.append(vertex_points[i])
    for i in range(len(coord_outside_mbr)):
        plotter.add_point(coord_outside_mbr[i][0], coord_outside_mbr[i][1], 'outside')
        outside_points.append(coord_outside_mbr[i])
    for i in range(len(coord_boundary)):
        plotter.add_point(coord_boundary[i][0], coord_boundary[i][1], 'boundary')
        boundary_points.append(coord_boundary[i])
    for i in range(len(rca_outside)):
        plotter.add_point(rca_outside[i][0], rca_outside[i][1], 'outside')
        outside_points.append(rca_outside[i])
    for i in range(len(rca_inside)):
        plotter.add_point(rca_inside[i][0], rca_inside[i][1], 'inside')
        inside_points.append(rca_inside[i])

    # this provides a third list with the points classification
    boundary = [boundary_points, ['boundary'] * len(boundary_points)]
    inside = inside_points, ['inside'] * len(inside_points)
    outside = outside_points, ['outside'] * len(outside_points)

    # join all the points together in one list
    boundary[0].extend(inside[0])
    boundary[1].extend(inside[1])
    boundary[0].extend(outside[0])
    boundary[1].extend(outside[1])

    # Combining the original ID, X and Y, with the classification list.
    original_points = [(y, x) for x, y in zip(original_points[0], original_points[1])]
    id, classification = [], []
    for point, flag in original_points:
        index = boundary[0].index(point)
        id.append(flag)
        classification.append(boundary[1][index]) # returns the classification with the same coordinates as ID

    # for point, flag in final_points
    # plot all of the rays
    # every point
    # max_x_in_points = max(raw_points[1]) # highest x value in input points
    # rca_rays = [raw_points[1], raw_points[2], [max_x_in_points] * 100, raw_points[2]]
    # print(rca_rays[0])
    # print(rca_rays[1])
    # print(rca_rays[2])
    # print(rca_rays[3])
    #
    # for i in range(len(rca_rays)):
    #     plotter.add_line(rca_rays[0][i], rca_rays[1][i], rca_rays[2][i], rca_rays[3][i])

    # Export points with classification
    export_csv(out_path, id, classification)

    plotter.show(fig_path)


if __name__ == "__main__":
    main()
