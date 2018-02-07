# Introduction to Obstacle Avoidance
import math
import numpy as np

file_points = open("mission.waypoints", "r")
lines_points = np.asarray(file_points.read().split('\n'))
point_number = len(lines_points) - 1
points = np.zeros((point_number, 3))  # point number; lat, long, alt
#
home_point = [39.589000, -74.9507, 1]
#
temp_point_number = 10
temp_points = np.zeros((temp_point_number, 3))  # temp_point number; lat, long, alt
#
file_obstacles = open("obstacles.poly", "r")
lines_obstacles = np.asarray(file_obstacles.read().split('\n'))
obstacle_number = len(lines_obstacles) - 1
obstacles = np.zeros((obstacle_number, 5))  # obstacle number; lat, long, alt, radius, speed
#
global trouble_points
trouble_points = np.zeros((temp_point_number, 5))  # temp_point number; lat, long, alt, control, obstacle number
#
earth_radius = 6371000  # earth`s radius in meter


def get_points():
    for i in range(0, point_number):
        values = np.asarray(lines_points[i + 1].split('\t'))
        points[i, 0] = values[8]
        points[i, 1] = values[9]
        points[i, 2] = values[10]
    print(points)
    return points


def get_obstacles():
    for i in range(0, obstacle_number):
        values = np.asarray(lines_obstacles[i + 1].split(' '))
        print(values)
        obstacles[i, 0] = values[0]
        obstacles[i, 1] = values[1]
        obstacles[i, 2] = values[2]
        obstacles[i, 3] = values[3]
        #######
        obstacles[i, 4] = values[4]
        #######
    print(obstacles)
    return obstacles


def get_temp_points(vehicle_position, reaching_point):
    for i in range(0, temp_point_number):
        temp_points[i, 0] = vehicle_position + (reaching_point[0] - vehicle_position[0]) / temp_point_number * i
        temp_points[i, 1] = vehicle_position + (reaching_point[1] - vehicle_position[1]) / temp_point_number * i
        temp_points[i, 2] = vehicle_position + (reaching_point[2] - vehicle_position[2]) / temp_point_number * i
    return temp_points


def get_distance(first_point, second_point):
    lat1 = first_point[0] / 180 * math.pi  # coordinate to radian
    lng1 = first_point[1] / 180 * math.pi  # coordinate to radian
    lat2 = second_point[0] / 180 * math.pi  # coordinate to radian
    lng2 = second_point[1] / 180 * math.pi  # coordinate to radian
    dlat = lat2 - lat1  # latitute difference in radian
    dlong = lng2 - lng1  # longitute difference in radian

    a = math.pow(math.sin(dlat / 2), 2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(dlong / 2), 2)  # Haversine Formula
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))  # Haversine Formula
    distance = earth_radius * c
    return distance


def get_intersections(temp_points, obstacles):
    for i in range(0, temp_point_number):
        for j in range(0, obstacle_number):
            if get_distance(temp_points[i], obstacles[j]) < obstacles[j, 2] * 1.2:
                global trouble_points
                trouble_points[i, 0] = temp_points[i, 0]
                trouble_points[i, 1] = temp_points[i, 1]
                trouble_points[i, 2] = temp_points[i, 2]
                trouble_points[i, 3] = 1
                trouble_points[i, 4] = j

#  temp point sayisini aradaki mesafeye gore belirlemek lazim
#  temp waypoint konumalarini aracin  hizina ve gore tahmini yerlere atamak
#  ustteki olayi obstacle lar icin de yapmak