# MAIN CODE
import numpy as np
# Importing Local Python Files
import mavlink
import interop
import sda

vehicle = mavlink.connect_vehicle('sitl')
