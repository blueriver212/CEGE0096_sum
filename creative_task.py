from plotter import Plotter
from geometry_classes import *
from main_from_file import *
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import contextily as ctx


def exportcsv(output_path, identification, classification, x, y):

    xs = [str(i) for i in x]
    ys = [str(i) for i in y]
    print(xs)
    print(ys)
    identification.insert(0, 'id')
    classification.insert(0, 'classification')
    xs.insert(0, 'x')
    ys.insert(0, 'y')
    out_file = [identification, xs, ys, classification]

    with open(output_path, 'w') as f:
        for i in range(len(out_file[0])):
            f.write(out_file[0][i])
            f.write(',')
            f.write(out_file[1][i])
            f.write(',')
            f.write(out_file[2][i])
            f.write(',')
            f.write(out_file[3][i])
            f.write('\n')


def main():
    london = 'london.csv'
    points = 'england_points.csv'

    plotter = Plotter()

    # calculate and plot the MBR polygon
    polygon_points = import_csv(london)
    poly = list(zip(polygon_points[1], polygon_points[2]))
    MBR_values = MBR(polygon_points)
    mbr = MBR_values.mbr_coordinates()
    plotter.add_polygon(polygon_points[1], polygon_points[2])
    plotter.add_poly_outline(mbr[0], mbr[1])

    # import the individual points
    raw_points = import_csv(points)
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
    id_, classification, xs, ys = [], [], [], []
    for point, flag in original_points:
        index = boundary[0].index(point)
        x, y = point
        id_.append(flag)
        classification.append(boundary[1][index])  # returns the classification with the same coordinates as ID
        xs.append(x)
        ys.append(y)
    out_path = 'classified_london_points.csv'
    exportcsv(out_path, id_, classification, xs, ys)

    plotter.show('London Points.png')

    # opening up the CSV with pandas
    df = pd.read_csv('classified_london_points.csv')

    # turn the POINTS X, Y coordinates into point classes
    london_points = df.apply(lambda row: Point(row.x, row.y), axis=1)
    london_points.crs = {'init': 'epsg:27700'}

    # Plots the points with geopandas and matplotlib
    points = gpd.GeoDataFrame(df, geometry=london_points)
    temp = points.to_crs(epsg=3857)
    ax = temp.plot(column=points.classification, categorical=True, markersize=100, legend=True, cmap='tab20')
    ctx.add_basemap(ax)

    plt.ylabel('Northing')
    plt.xlabel('Easting')
    plt.title('Are your points inside or outside London?')

    plt.show()


if __name__ == "__main__":
    main()