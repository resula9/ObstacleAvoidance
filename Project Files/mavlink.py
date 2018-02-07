import dronekit_sitl
from dronekit import connect
import argparse


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
        except:
            print "Vehicle is not connected!!"
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




