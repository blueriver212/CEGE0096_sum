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


def main():
    plotter = Plotter()

    #Plot the points from a csv
    test = import_csv('input.csv')
    print(test)
    x = test[1]
    y = test[2]
    for i in range(len(x)):
        plotter.add_point(x[i], y[i])
    plotter.show()


    print("read polygon.csv")
    print("read input.csv")
    print("categorize points")
    print("write output.csv")
    print("plot polygon and points")


if __name__ == "__main__":
    main()
