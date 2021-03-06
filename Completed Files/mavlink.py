import dronekit_sitl
from dronekit import connect, Command, Vehicle, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import math

# Importing Local Python Files
import sda
import json


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


# Classes
vehicle = Vehicle

mission = Mission
obstacle = Obstacle


def antenna_tracker():

    global vehicle

    tracking = True
    # GERCEK KONUMLARI KULLAN

    home = {}
    home.lat = mission.home_pos['latitude']
    home.lon = mission.home_pos['latitude']
    home.alt = 0

    target = {}
    target.lat = vehicle.location.global_relative_frame.lat
    target.lon = vehicle.location.global_relative_frame.lon
    target.alt = vehicle.location.global_relative_frame.alt

    while tracking:

        dif_lat = sda.get_distance(home.lat, home.lon, home.lat, target.lon)
        dif_lon = sda.get_distance(home.lat, home.lon, target.lat, home.lon)

        hor_angle = math.atan2(dif_lon, dif_lat)

        dif_alt = target.alt - home.alt
        hor_distance = sda.get_distance(home.lat, home.lon, target.lat, target.lon)

        ver_angle = math.atan2(dif_alt, hor_distance)

        print 'AT Horizontal Angle: %f', hor_angle
        print 'AT Vertical Angle: %f', ver_angle


def start_interop():
    #
    global mission
    mission_file = open("missions.json", "r")
    missiondata = mission_file.read()
    mission = Mission(missiondata)
    #
    global obstacle
    obstacle_file = open("obstacles.json", "r")
    obstacledata = obstacle_file.read()
    obstacledata = str(obstacledata).replace('altitude_msl', 'altitude')
    obstacledata = str(obstacledata).replace('sphere_radius', 'radius')
    obstacledata = str(obstacledata).replace('cylinder_height', 'altitude')
    obstacledata = str(obstacledata).replace('cylinder_radius', 'radius')
    obstacle = Obstacle(obstacledata)
    #


def wp_file_read(wp_file_name):

    global vehicle

    print "\nReading mission from file: %s" % wp_file_name
    cmd = []
    with open(wp_file_name) as f:
        for i, line in enumerate(f):
            if i == 0:
                if not line.startswith('QGC WPL 110'):
                    raise Exception('File is not supported WP version')
            else:
                linearray = line.split('\t')
                if linearray[3] == '16':
                    command_type = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
                elif linearray[3] == '206':
                    command_type = mavutil.mavlink.MAV_CMD_DO_SET_CAM_TRIGG_DIST
                elif linearray[3] == '201':
                    command_type = mavutil.mavlink.MAV_CMD_DO_SET_ROI
                elif linearray[3] == '181':
                    command_type = mavutil.mavlink.MAV_CMD_DO_SET_RELAY
                elif linearray[3] == '22':
                    command_type = mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
                elif linearray[3] == '21':
                    command_type = mavutil.mavlink.MAV_CMD_NAV_LAND
                else:
                    print 'Command is undefined!!'
                    raise Exception

                command = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                                  command_type, 0, 0, 0, 0, 0, 0, float(linearray[8]),
                                  float(linearray[9]), float(linearray[10]))
                cmd.append(command)
    return cmd


def connect_vehicle(connection_string):

    global vehicle

    if connection_string == "sitl":
        sitl = dronekit_sitl.start_default()
        print('Connecting to vehicle on: %s' % connection_string)
        connection_string = sitl.connection_string()
        vehicle = connect(connection_string, wait_ready=True)
    else:
        try:
            print('Connecting to vehicle on: %s' % connection_string)
            vehicle = connect(connection_string, wait_ready=True, baud=57600)
        except Exception as e:
            print 'Couldn`t connected to the vehicle Error: %s\n', e
    return vehicle


def set_home():

    global vehicle

    while not vehicle.home_location:  # Get Vehicle Home location - will be `None` until first set by autopilot
        vehicle.commands.download()
        vehicle.commands.wait_ready()
        if not vehicle.home_location:
            print 'Waiting for home location ...'
            time.sleep(1)

    my_location = vehicle.location.global_frame
    my_location.alt = vehicle.location.global_frame.alt
    vehicle.home_location = my_location

    vehicle.commands.download()
    vehicle.commands.wait_ready()

    print '\nNew Home location: %s\n' % vehicle.home_location
    return my_location


def clear_mission():

    global vehicle

    try:
        vehicle.commands.clear()
    except Exception as e:
        print 'Mission couldn`t be deleted Error: %s\n', e
    else:
        print 'Mission is successfully deleted from vehicle\n'


def write_mission(mission):

    global vehicle

    cmd = list()

    # ADD TAKEOFF POINT
    cmd.append(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0,
                       0, 0, 0, 0, 0,
                       mission.home_pos['latitude'],
                       mission.home_pos['longitude'],
                       0))

    # ADD WAYPOINTS
    for i in range(len(mission.mission_waypoints)):
        cmd.append(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0,
                           0, 0, 0, 0, 0,
                           mission.mission_waypoints[i]['latitude'],
                           mission.mission_waypoints[i]['longitude'],
                           mission.mission_waypoints[i]['altitude_msl']))
    # ADD LANDING POINT
    cmd.append(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0,
                       0, 0, 0, 0, 0,
                       mission.home_pos['latitude'],
                       mission.home_pos['longitude'],
                       1))
    return cmd


def send_mission(missionlist):

    global vehicle

    # This ensures home_location is set (needed when saving WP file)
    if not vehicle.home_location:
        print "Home location is not set. Pls set home first!\n"
        return
    try:
        # Add new mission to vehicle
        for command in missionlist:
            vehicle.commands.add(command)
        print 'Uploading mission\n'
        vehicle.commands.upload()
        print 'Successfull!!'
    except Exception as e:
        print 'Couldn`t send the mission. Vehicle is not ready!! Error: %s\n', e


def arm_vehicle():

    global vehicle

    if vehicle.is_armable:
        vehicle.armed = True
    else:
        print 'Vehicle is not armable!!'


def off_axis():

    global vehicle

    off_axis_point = LocationGlobalRelative
    off_axis_point.lat = mission.off_axis_odlc_pos['latitude']
    off_axis_point.lon = mission.off_axis_odlc_pos['longitude']
    off_axis_point.alt = 1

    vehicle.gimbal.target_location(off_axis_point)


def airdrop():# COK SALAKCA BI KISIM GERCEKTEN!!!!!!!!!!

    global vehicle

    airdrop_pos = LocationGlobalRelative
    airdrop_pos.lat = mission.air_drop_pos['latitude']
    airdrop_pos.lon = mission.air_drop_pos['longitude']

    # Callback to print the location in global frame
    def location_callback(self, attr_name):

        if sda.get_distance(vehicle.location.attr_name.lat, vehicle.location.attr_name.lon,
                            airdrop_pos.lat, airdrop_pos.lon) < 10:
            vehicle.commands.add(
                Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0,
                        0, 0, 0, 0, 0,
                        airdrop_pos.lat,
                        airdrop_pos.lon,
                        1))

            vehicle.commands.upload()

    # Add observer for the vehicle's current location
    vehicle.add_attribute_listener('global_relative_frame', location_callback)

