data = '''
{
    "moving_obstacles": [
        {
            "altitude_msl": 189.56748784643966,
            "latitude": 38.141826869853645,
            "longitude": -76.43199876559223,
            "sphere_radius": 150.0
        },
        {
            "altitude_msl": 250.0,
            "latitude": 38.14923628783763,
            "longitude": -76.43238529543882,
            "sphere_radius": 150.0
        }
    ],
    "stationary_obstacles": [
        {
            "cylinder_height": 750.0,
            "cylinder_radius": 300.0,
            "latitude": 38.140578,
            "longitude": -76.428997
        },
        {
            "cylinder_height": 400.0,
            "cylinder_radius": 100.0,
            "latitude": 38.149156,
            "longitude": -76.430622
        }
    ]
}'''

import json


class Obstacle(object):

    def __init__(self, altitude_msl, latitude, longitude, sphere_radius):
        self.altitude_msl = altitude_msl
        self.latitude = latitude
        self.longitude = longitude
        self.sphere_radius = sphere_radius


def object_decoder(obj):
    return Obstacle(obj['altitude_msl'], obj['latitude'], obj['longitude'], obj['sphere_radius'])


x = json.loads(data, object_hook=object_decoder)

print(x.altitude_msl)