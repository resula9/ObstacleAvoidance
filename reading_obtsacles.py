import json


class Obstacle(object):

    def __init__(self, moving_obstacles, stationary_obstacles):
        self.moving_obstacles = moving_obstacles
        self.stationary_obstacles = stationary_obstacles


def object_decoder(obj):
    return Obstacle(obj['moving_obstacles'], obj['stationary_obstacles'])


file = open("jsonobstacle.json", "r")
data = file.read()

x = json.loads(data, object_hook=object_decoder)


print(x.moving_obstacles)
