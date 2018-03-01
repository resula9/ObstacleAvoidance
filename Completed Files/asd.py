# MAIN CODE
from dronekit import VehicleMode
import time
# Importing Local Python Files
import mavlink

#import antennatracker

mavlink.start_interop()

mavlink.connect_vehicle('sitl')

mavlink.set_home()

mavlink.clear_mission()

#commands = mavlink.write_mission(mission=interop.mission)
commands = mavlink.wp_file_read('mission.txt')
mavlink.send_mission(commands)



mavlink.vehicle.mode = VehicleMode('GUIDED')

mavlink.arm_vehicle()

mavlink.vehicle.simple_takeoff(10)


mavlink.vehicle.mode = VehicleMode('AUTO')

time.sleep(15)

print mavlink.vehicle.mode

#mavlink.vehicle.simple_takeoff(30)
#print vehicle.mode####ATTRIBUTE LISTENER

