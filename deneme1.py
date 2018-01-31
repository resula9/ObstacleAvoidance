# Json Exapmle for Obstacle Avoidance
import math
import numpy as np
import json
from collections import namedtuple


class Obstacle(object):
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


def object_decoder(obj):
    if '_moving_obstacles' in obj and obj['moving_obstacles'] == 'Obstacle':
        return Obstacle(obj['latitude'], obj['longitude'])
    return obj


obstacles = '{"moving_obstacles": { "latitude": 38.141826869853645, "longitude": -76.43199876559223}}'

data = json.loads(obstacles)
#data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123.56}}'
#x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
x = json.loads(data, object_hook=object_decoder)

print(x.moving_obstacles.latitude)
