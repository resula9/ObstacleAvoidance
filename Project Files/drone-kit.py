# Introduction to DroneKit Python
import math
import numpy as np
import json
import dronekit_sitl
from dronekit import connect
import argparse


'''
Waypoint verisi kullanilarak mission olusturulacak ve otonom ucus icin bu veri araca yollanacak

Drone-kit ten aracin konum bilgisi alinarak vehicle_point degiskenine atanacak

temp point sayisi aradaki mesafeye gore belirlenecek

Obtsacle lar moving ve stationary olarak ayrilacak

stationary olanlar en bastan rotada waypoint eklenerek halledilecek
boylece islem yuku olmaktan cikacaklar ve dict kullanimi kolaylasacak

bunun icin programin basinda stationary ler icin bi fonksiyon yazmak gerekiyor
movingler icinse eski temp_point sistemiyle devam ediyoruz simdilik

Home point verisini otopilottan aldiktan sonra home un alt ini degistirebiliyoruz ancak 
lat ve long u degistirmede sorun var nedense araca yuklenmiyo bu veriler


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
obstacledata = str(obstacledata).replace('altitude_msl', 'altitude')
obstacledata = str(obstacledata).replace('sphere_radius', 'radius')
obstacledata = str(obstacledata).replace('cylinder_height', 'altitude')
obstacledata = str(obstacledata).replace('cylinder_radius', 'radius')
obstacle = Obstacle(obstacledata)
#


def connect_vehicle(connection_string):
    if connection_string == "sitl":
        sitl = dronekit_sitl.start_default()
        print("Connecting to vehicle on: %s" % connection_string)
        connection_string = sitl.connection_string()
        _vehicle = connect(connection_string, wait_ready=True)

    else:
        try:
            print("Connecting to vehicle on: %s" % connection_string)
            _vehicle = connect(connection_string, wait_ready=True)
        except:
            print "Vehicle is not connected!!"
    return _vehicle


def set_home():
    pass


def write_mission():
    parser = argparse.ArgumentParser(description='Demonstrates mission import/export from a file.')
    parser.add_argument('--connect',
                        help="Vehicle connection target string. If not specified, SITL automatically started and used.")
    args = parser.parse_args()

    connection_string = args.connect
    #sitl = None

    # Start SITL if no connection string specified
    if not connection_string:
        import dronekit_sitl
        sitl = dronekit_sitl.start_default()
        connection_string = sitl.connection_string()

    # Connect to the Vehicle
    print 'Connecting to vehicle on: %s' % connection_string
    vehicle = connect(connection_string, wait_ready=True)

    # Check that vehicle is armable.
    # This ensures home_location is set (needed when saving WP file)


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


vehicle = connect_vehicle('sitl')
while not vehicle.home_location:  # Get Vehicle Home location - will be `None` until first set by autopilot
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()
    if not vehicle.home_location:
        print " Waiting for home location ..."
# We have a home location, so print it!
print "\n Home location: %s" % vehicle.home_location

my_location = vehicle.location.global_frame
my_location.alt = vehicle.location.global_frame.alt
vehicle.home_location = my_location

cmds = vehicle.commands
cmds.download()
cmds.wait_ready()

print "\n New Home location: %s" % vehicle.home_location
