# MAIN CODE
import os
from dronekit import Vehicle, VehicleMode
import numpy as np
import time
# Importing Local Python Files
import mavlink
import interop
import sda
import odlc
import antennatracker

interop.start()

mavlink.connect_vehicle('sitl')

mavlink.set_home()

mavlink.clear_mission()
a
#commands = mavlink.write_mission(mission=interop.mission)
commands = mavlink.wp_file_read('mission.txt')
mavlink.send_mission(commands)

mavlink.arm_vehicle()

mavlink.vehicle = VehicleMode('AUTO')

time.sleep(15)



#mavlink.vehicle.simple_takeoff(30)
#print vehicle.mode####ATTRIBUTE LISTENER

