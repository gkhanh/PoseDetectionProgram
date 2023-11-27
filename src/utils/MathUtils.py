import math
import numpy as np


# This class is for calculating angles and distances between landmark coordinates


class MathUtils:
    def __init__(self) -> None:
        pass

    def calculateAngle(self, a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360.0 - angle

        return angle

    def calculateAngleWithXAxis(self, a, b):
        x_diff = a[0] - b[0]
        y_diff = a[1] - b[1]
        return math.degrees(math.atan2(y_diff, x_diff))

    def calculateDistance(self, coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance
