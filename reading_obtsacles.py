import json


class Mission(object):

    def __init__(self, json_content):
        missiondata = json.loads(json_content)
        for key, value in missiondata.items():
            self.__dict__[key] = value


class Obstacle(object):

    def __init__(self, json_content):
        obstacledata = json.loads(json_content)
        for key, value in obstacledata.items():
            self.__dict__[key] = value

        self.__dict__('stationary_obstacles')[i].get('altitude') =


file1 = open("obstacles.json", "r")
data = file1.read()
data = str(data).replace('altitude_msl', 'altitude')
data = str(data).replace('sphere_radius', 'radius')
data = str(data).replace('cylinder_height', 'altitude')
data = str(data).replace('cylinder_radius', 'radius')

obstacle = Obstacle(data)
print obstacle.moving_obstacles[1].get('altitude')


