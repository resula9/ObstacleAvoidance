import dronekit
import dronekit_sitl
from dronekit import connect
import argparse
import time
import mavlink

connection_string = 'sitl'

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




def write_mission(vehicle, mission):

    cmds = vehicle.commands

    mavlink.connect_vehicle(sitl)

    # Check that vehicle is armable.-0
    # This ensures home_location is set (needed when saving WP file)
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)

