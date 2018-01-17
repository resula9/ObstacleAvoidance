# Introduction to Obstacle Avoidance
import numpy as np

file_points = open("mission.waypoints", "r")
lines_points = np.asarray(file_points.read().split('\n'))
point_number = len(lines_points) - 1
points = np.zeros((point_number, 3))  # lat, long, alt

file_obstacles = open("obstacles.poly", "r")
lines_obstacles = np.asarray(file_obstacles.read().split('\n'))
obstacle_number = len(lines_obstacles) - 1
obstacles = np.zeros((obstacle_number, 5))  # lat, long, alt, radius, speed


def get_points():
    for i in range(0, point_number):
        values = np.asarray(lines_points[i + 1].split('\t'))
        points[i, 0] = values[8]
        points[i, 1] = values[9]
        points[i, 2] = values[10]


def get_obstacles():
    for i in range(0, obstacle_number):
        values = np.asarray(lines_obstacles[i + 1].split(' '))
        print(values)
        obstacles[i, 0] = values[0]
        obstacles[i, 1] = values[1]
        obstacles[i, 2] = values[2]
        obstacles[i, 3] = values[3]
        obstacles[i, 4] = values[4]

get_points()
get_obstacles()
print(obstacles)
print(points)