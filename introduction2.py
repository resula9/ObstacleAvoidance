# Introduction to Obstacle Avoidance
import numpy as np


def get_points():
    file_points = open("mission.waypoints", "r")
    lines = np.asarray(file_points.read().split('\n'))
    point_number = len(lines) - 1
    points = np.zeros((point_number, 3))

    for i in range(0, point_number):
        values = np.asarray(lines[i + 1].split('\t'))
        points[i, 0] = values[8]
        points[i, 1] = values[9]
        points[i, 2] = values[10]
    print(points)


get_points()
