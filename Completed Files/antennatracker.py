import math
import mavlink
import sda
import interop

tracking = True
# GERCEK KONUMLARI KULLAN

home = {}
home.lat = interop.mission.home_pos['latitude']
home.lon = interop.mission.home_pos['latitude']
home.alt = 0

target = {}
target.lat = mavlink.vehicle.location.global_relative_frame.lat
target.lon = mavlink.vehicle.location.global_relative_frame.lon
target.alt = mavlink.vehicle.location.global_relative_frame.alt


def hor_angle():

    dif_lat = sda.get_distance(home.lat, home.lon, home.lat, target.lon)
    dif_lon = sda.get_distance(home.lat, home.lon, target.lat, home.lon)

    angle = math.atan2(dif_lon, dif_lat)

    return angle


def ver_angle():

    dif_alt = target.alt - home.alt
    hor_distance = sda.get_distance(home.lat, home.lon, target.lat, target.lon)

    angle = math.atan2(dif_alt, hor_distance)

    return angle


while tracking:

    h_angle = hor_angle()
    v_angle = ver_angle()

    print 'AT Horizontal Angle: %f', hor_angle()
    print 'AT Vertical Angle: %f', ver_angle()

