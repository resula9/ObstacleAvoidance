import dronekit_sitl
from dronekit import connect
import time


def connect_vehicle(connection_string):
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


def clear_mission(vehicle):
    try:
        cmds = vehicle.commands
        cmds.clear()
        cmds.upload()
    except Exception as e:
        print 'Mission couldn`t be deleted Error: %s', e
    else:
        print 'mission is successfully deleted from vehicle'


def write_mission(vehicle, mission):

    # Add file-format information
    waypoints = 'QGC WPL 110\n'
    home = vehicle.home_location
    # SET HOME POINT
    waypoints += "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (0, 1, 0, 16, 0, 0, 0, 0,
                                                                       mission.home_pos['latitude'],
                                                                       mission.home_pos['longitude'],
                                                                       mission.home_pos['altitude'], 1)
    # ADD TAKEOFF POINT
    waypoints += "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (0, 1, 0, 22, 0, 0, 0, 0,
                                                                       mission.home_pos['latitude'],
                                                                       mission.home_pos['longitude'],
                                                                       mission.home_pos['altitude'], 1)

    # ADD WAYPOINTS
    for i in range(len(mission.mission_waypoints)):
        waypoints += "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (0, 1, 0, 16, 0, 0, 0, 0,
                                                                           mission.mission_waypoints[i]['latitude'],
                                                                           mission.mission_waypoints[i]['longitude'],
                                                                           mission.mission_waypoints[i]['altitude'], 1)
    # ADD LANDING POINT
    waypoints += "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (0, 1, 0, 21, 0, 0, 0, 0,
                                                                       mission.home_pos['latitude'],
                                                                       mission.home_pos['longitude'],
                                                                       mission.home_pos['altitude'], 1)
    return waypoints


def send_mission(vehicle, missionlist):
    cmds = vehicle.commands
    connect_vehicle('sitl')
    # Check that vehicle is armable.-0
    # This ensures home_location is set (needed when saving WP file)
    while not vehicle.is_armable:
         print " Waiting for vehicle to initialise..."
         time.sleep(1)

    # Add new mission to vehicle
    for command in missionlist:
        cmds.add(command)
    print ' Upload mission'
    vehicle.commands.upload()


