import dronekit_sitl
from dronekit import connect, Command, Vehicle, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import interop
import sda

vehicle = Vehicle


def wp_file_read(wp_file_name):

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
    off_axis_point.lat = interop.mission.off_axis_odlc_pos['latitude']
    off_axis_point.lon = interop.mission.off_axis_odlc_pos['longitude']
    off_axis_point.alt = 1

    vehicle.gimbal.target_location(off_axis_point)


def airdrop():

    global vehicle

    airdrop_pos = LocationGlobalRelative
    airdrop_pos.lat = interop.mission.air_drop_pos['latitude']
    airdrop_pos.lon = interop.mission.air_drop_pos['longitude']

    if sda.get_distance(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon,
                        airdrop_pos.lat, airdrop_pos.lon) < 5:
        vehicle.commands.add(
            Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0,
                    0, 0, 0, 0, 0,
                    airdrop_pos.lat,
                    airdrop_pos.lon,
                    1))

        vehicle.commands.upload()
