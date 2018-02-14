# MAIN CODE
import os
from dronekit import Vehicle, VehicleMode
import numpy as np
# Importing Local Python Files
import mavlink
import interop
import sda
import airdrop
import odlc
import off_axis

global vehicle
vehicle = Vehicle

interop.start()

vehicle = mavlink.connect_vehicle('sitl')

mavlink.set_home()

mavlink.clear_mission()

commands = mavlink.write_mission(mission=interop.mission)
mavlink.send_mission(commands)

vehicle = VehicleMode('AUTO')

print vehicle.mode####ATTRIBUTE LISTENER
