cp = [[4,5,6],[7,8,9],['I','O','I']]
out = [[1,2,3],[4,5,6],[7,8,9]]

cp = [((x, y), z) for x, y, z in zip(cp[0], cp[1], cp[2])]
print(cp)
points = [(z, (x, y)) for x, y, z in zip(out[1], out[2], out[0])]
print(points)
output = []
for point, classif in cp:
    x, y = point
    z = classif
    for point, id in points

    output.append(tmp)
print(output)