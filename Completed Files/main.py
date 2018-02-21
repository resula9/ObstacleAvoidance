# MAIN CODE
import os
from dronekit import Vehicle, VehicleMode
import numpy as np
import time
# Importing Local Python Files
import mavlink
import interop
import sda
import airdrop
import odlc
import off_axis

interop.start()

vehicle = mavlink.connect_vehicle('sitl')

mavlink.set_home()

mavlink.clear_mission()

commands = mavlink.write_mission(mission=interop.mission)
mavlink.send_mission(commands)

#vehicle = VehicleMode('AUTO')

mavlink.vehicle.armed = True
time.sleep(5)



#mavlink.vehicle.simple_takeoff(30)
#print vehicle.mode####ATTRIBUTE LISTENER

