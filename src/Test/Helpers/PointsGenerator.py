import math


def PointsGenerator(x, y, z, angleXY, angleZ, distance=1):
    # Convert the angles to radians
    angleXYInRad = math.radians(angleXY)
    angleZInRad = math.radians(angleZ)

    # Calculate the coordinates of the first point
    x1 = x + distance * math.sin(angleZInRad) * math.cos(angleXYInRad)
    y1 = y + distance * math.sin(angleZInRad) * math.sin(angleXYInRad)
    z1 = z + distance * math.cos(angleZInRad)

    # Calculate the coordinates of the second point
    x2 = x + distance * math.sin(math.pi - angleZInRad) * math.cos(math.pi - angleXYInRad)
    y2 = y + distance * math.sin(math.pi - angleZInRad) * math.sin(math.pi - angleXYInRad)
    z2 = z + distance * math.cos(math.pi - angleZInRad)

    return (x1, y1, z1), (x2, y2, z2)


def ThirdPointGenerator(point1, point2, angle, distance):
    # Convert the angle to radians
    angleInRad = math.radians(angle)

    # Define the vector from point1 to point2
    vector12 = [p2 - p1 for p1, p2 in zip(point1, point2)]

    # Calculate the length (magnitude) of the vector
    length = math.sqrt(sum(val ** 2 for val in vector12))

    # Normalize the vector
    vector12 = [val / length for val in vector12]

    # Calculate the coordinates of the third point
    x3 = point1[0] + distance * math.cos(angleInRad) * vector12[0] - distance * math.sin(angleInRad) * vector12[1]
    y3 = point1[1] + distance * math.cos(angleInRad) * vector12[1] + distance * math.sin(angleInRad) * vector12[0]
    z3 = point1[2] + distance * vector12[2]

    return (x3, y3, z3)


# Test the functions with a point and angles
point = (0.43, 0.18, 0.98)  # vertex point of first Angle
targetAngleXY = 20
targetAngleZ = 0.6

point1, point2 = PointsGenerator(*point, targetAngleXY, targetAngleZ)

print("Original point:", point)
print("First new point:", point1)
print("Second new point:", point2)

angle = 77
distance = 1

# point1 is the vertex point of the second Angle
point3 = ThirdPointGenerator(point1, point2, angle, distance)

print("Third new point:", point3)
