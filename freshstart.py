# Fresh Start to Obstacle Avoidance
import math
import numpy as np
import json

'''
Drone-kit ten aracin konum bilgisi alinarak vehicle_point degiskenine atanacak
temp point sayisi aradaki mesafeye gore belirlenecek
Obtsacle lar moving ve stationary olarak ayrilacak
stationary olanlar en bastan rotada waypoint eklenerek halledilecek
boylece islem yuku olmaktan cikacaklar ve dict kullanimi kolaylasacak
bunun icin programin basinda stationary ler icin bi fonksiyon yazmak gerekiyor
movingler icinse eski temp_point sistemiyle devam ediyoruz simdilik

'''


class Mission(object):

    def __init__(self, json_content):
        data = json.loads(json_content)
        for key, value in data.items():
            self.__dict__[key] = value


class Obstacle(object):

    def __init__(self, json_content):
        data = json.loads(json_content)
        for key, value in data.items():
            self.__dict__[key] = value
        for i in range (0, len(self.__dict__['stationary_obstacles'])):
            real_height = self.stationary_obstacles[i].get('altitude')
            cylinder_radius = self.stationary_obstacles[i].get('radius')
            estimated_altitude = int(real_height) - int(cylinder_radius)
            self.__dict__['stationary_obstacles'][i]['altitude'] = str(estimated_altitude)


#
temp_point_number = 10
temp_points = np.zeros((temp_point_number, 3))  # temp_point number; lat, long, alt
#
global trouble_points
trouble_points = np.zeros((temp_point_number, 5))  # temp_point number; lat, long, alt, control, obstacle number
#
earth_radius = 6371000  # earth`s radius in meter
#
mission_file = open("missions.json", "r")
missiondata = mission_file.read()
mission = Mission(missiondata)
#
obstacle_file = open("obstacles.json", "r")
obstacledata = obstacle_file.read()
obstacle = Obstacle(obstacledata)
#


def get_temp_points(vehicle_position, reaching_point):
    for i in range(0, temp_point_number):
        temp_points[i, 0] = vehicle_position + (reaching_point[0] - vehicle_position[0]) / temp_point_number * i
        temp_points[i, 1] = vehicle_position + (reaching_point[1] - vehicle_position[1]) / temp_point_number * i
        temp_points[i, 2] = vehicle_position + (reaching_point[2] - vehicle_position[2]) / temp_point_number * i
    return temp_points


def get_distance(first_lat, first_lng, second_lat, second_lng):
    lat1 = first_lat / 180 * math.pi  # coordinate to radian
    lng1 = first_lng / 180 * math.pi  # coordinate to radian
    lat2 = second_lat / 180 * math.pi  # coordinate to radian
    lng2 = second_lng / 180 * math.pi  # coordinate to radian
    dlat = lat2 - lat1  # latitute difference in radian
    dlong = lng2 - lng1  # longitute difference in radian

    a = math.pow(math.sin(dlat / 2), 2) + math.cos(lat1) * math.cos(lat2) \
        * math.pow(math.sin(dlong / 2), 2)  # Haversine Formula
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
