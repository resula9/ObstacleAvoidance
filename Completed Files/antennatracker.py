import math
import mavlink
import sda

#tracking = True
# GERCEK KONUMLARI KULLAN

home = {}
home.lat = 1
home.lon = 1
home.alt = 1

target = {}
target.lat = 2
target.lon = 2
target.alt = 2


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


while True:

    h_angle = hor_angle()
    v_angle = ver_angle()
