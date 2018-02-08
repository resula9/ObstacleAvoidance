import dronekit_sitl
from dronekit import connect, Command, Vehicle
import time
from pymavlink import mavutil


def connect_vehicle(connection_string):

    vehicle = Vehicle

    if connection_string == "sitl":
        sitl = dronekit_sitl.start_default()
        print("Connecting to vehicle on: %s" % connection_string)
        connection_string = sitl.connection_string()
        vehicle = connect(connection_string, wait_ready=True)

    else:
        try:
            print("Connecting to vehicle on: %s" % connection_string)
            vehicle = connect(connection_string, wait_ready=True)
        except Exception as e:
            print 'Couldn`t connected to the vehicle Error: %s', e
    return vehicle


def set_home(vehicle):

    cmds = vehicle.commands

    while not vehicle.home_location:  # Get Vehicle Home location - will be `None` until first set by autopilot
        cmds.download()
        cmds.wait_ready()
        if not vehicle.home_location:
            print " Waiting for home location ..."
    # We have a home location, so print it!
    print "\n Home location: %s" % vehicle.home_location

    my_location = vehicle.location.global_frame
    my_location.alt = vehicle.location.global_frame.alt
    vehicle.home_location = my_location

    cmds.download()
    cmds.wait_ready()

    print "\n New Home location: %s" % vehicle.home_location
    return my_location


def clear_mission(vehicle):
    try:
        cmds = vehicle.commands
        cmds.clear()
        cmds.upload()
    except Exception as e:
        print 'Mission couldn`t be deleted Error: %s', e
    else:
        print 'Mission is successfully deleted from vehicle'


def write_mission(vehicle, mission):

    cmd = list()

    # ADD TAKEOFF POINT
    cmd.append(Command(0, 0, 0, vehicle.location.global_relative_frame, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0,
                       0, 0, 0, 0, 0,
                       mission.home_pos['latitude'],
                       mission.home_pos['longitude'],
                       mission.home_pos['altitude']))

    # ADD WAYPOINTS
    for i in range(len(mission.mission_waypoints)):
        cmd.append(Command(0, 0, 0, vehicle.location.global_relative_frame, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0,
                           0, 0, 0, 0, 0,
                           mission.mission_waypoints[i]['latitude'],
                           mission.mission_waypoints[i]['longitude'],
                           mission.mission_waypoints[i]['altitude']))
    # ADD LANDING POINT
    cmd.append(Command(0, 0, 0, vehicle.location.global_relative_frame, mavutil.mavlink.MAV_CMD_NAV_LAND, 0,
                       0, 0, 0, 0, 0,
                       mission.home_pos['latitude'],
                       mission.home_pos['longitude'],
                       mission.home_pos['altitude']))
    return cmd


def send_mission(vehicle, missionlist):

    cmds = vehicle.commands

    # This ensures home_location is set (needed when saving WP file)
    if not vehicle.home_location:
        print " Home location is not set. Pls set home first!"
        return
    try:
        # Add new mission to vehicle
        for command in missionlist:
            cmds.add(command)
        print ' Upload mission'
        vehicle.commands.upload()

    except Exception as e:
        print 'Couldn`t send the mission. Vehicle is not ready!! Error: %s', e


connect_vehicle('sitl')
