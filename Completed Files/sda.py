import math
import numpy as np


#
temp_point_number = 10
temp_points = np.zeros((temp_point_number, 3))  # temp_point number; lat, long, alt
#
global trouble_points
trouble_points = np.zeros((temp_point_number, 5))  # temp_point number; lat, long, alt, control, obstacle number
#
earth_radius = 6371000  # earth`s radius in meter
#


def get_temp_points(vehicle_position, reaching_point):
    for i in range(0, temp_point_number):
        temp_points[i, 0] = vehicle_position + (reaching_point[0] - vehicle_position[0]) / temp_point_number * i
        temp_points[i, 1] = vehicle_position + (reaching_point[1] - vehicle_position[1]) / temp_point_number * i
        temp_points[i, 2] = vehicle_position + (reaching_point[2] - vehicle_position[2]) / temp_point_number * i
    return temp_points


def get_distance(first_lat, first_lon, second_lat, second_lon):
    lat1 = first_lat / 180 * math.pi  # coordinate to radian
    lon1 = first_lon / 180 * math.pi  # coordinate to radian
    lat2 = second_lat / 180 * math.pi  # coordinate to radian
    lon2 = second_lon / 180 * math.pi  # coordinate to radian
    dlat = lat2 - lat1  # latitute difference in radian
    dlong = lon2 - lon1  # longitute difference in radian

    a = math.pow(math.sin(dlat / 2), 2) + math.cos(lat1) * math.cos(lat2) * \
        math.pow(math.sin(dlong / 2), 2)  # Haversine Formula
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))  # Haversine Formula
    distance = earth_radius * c
    return distance


def get_intersections(temp_points, obstacle):
    for i in range(0, temp_point_number):
        for j in range(0, len(obstacle.moving_obstacles)):
            if get_distance(temp_points[i, 0], temp_points[i, 1], obstacle.moving_obstacles[j].latitude,
                            obstacle.moving_obstacles[j].longitude) < obstacle.moving_obstacles[j].radius * 1.2:
                global trouble_points
                trouble_points[i, 0] = temp_points[i, 0]
                trouble_points[i, 1] = temp_points[i, 1]
                trouble_points[i, 2] = temp_points[i, 2]
                trouble_points[i, 3] = 1
                trouble_points[i, 4] = j
                print('obtacle is trouble')
