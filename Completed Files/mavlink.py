import dronekit_sitl
from dronekit import connect, Command, Vehicle
from pymavlink import mavutil
import time


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
            vehicle = connect(connection_string, wait_ready=True)
        except Exception as e:
            print 'Couldn`t connected to the vehicle Error: %s\n', e
    return vehicle


def set_home():

    global vehicle

    cmds = vehicle.commands

    while not vehicle.home_location:  # Get Vehicle Home location - will be `None` until first set by autopilot
        cmds.download()
        cmds.wait_ready()
        if not vehicle.home_location:
            print 'Waiting for home location ...'
            time.sleep(1)

    my_location = vehicle.location.global_frame
    my_location.alt = vehicle.location.global_frame.alt
    vehicle.home_location = my_location

    cmds.download()
    cmds.wait_ready()

    print '\nNew Home location: %s\n' % vehicle.home_location
    return my_location


def clear_mission():

    global vehicle

    try:
        cmds = vehicle.commands
        cmds.clear()
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

    cmds = vehicle.commands

    # This ensures home_location is set (needed when saving WP file)
    if not vehicle.home_location:
        print "Home location is not set. Pls set home first!\n"
        return
    try:
        # Add new mission to vehicle
        for command in missionlist:
            cmds.add(command)
        print 'Uploading mission\n'
        vehicle.commands.upload()
        print 'Successfull!!'

    except Exception as e:
        print 'Couldn`t send the mission. Vehicle is not ready!! Error: %s\n', e
