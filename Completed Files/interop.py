import json


class Mission(object):

    def __init__(self, json_content):
        data = json.loads(json_content)
        for key, value in data.items():
            self.__dict__[key] = value


class Obstacle(object):

    def __init__(self, json_content):
        data = json.loads(json_content)
        for key, value in data.items():
            self.__dict__[key] = value
        for i in range (0, len(self.__dict__['stationary_obstacles'])):
            real_height = self.stationary_obstacles[i].get('altitude')
            cylinder_radius = self.stationary_obstacles[i].get('radius')
            estimated_altitude = int(real_height) - int(cylinder_radius)
            self.__dict__['stationary_obstacles'][i]['altitude'] = str(estimated_altitude)


#
mission_file = open("missions.json", "r")
missiondata = mission_file.read()
mission = Mission(missiondata)
#
obstacle_file = open("obstacles.json", "r")
obstacledata = obstacle_file.read()
obstacledata = str(obstacledata).replace('altitude_msl', 'altitude')
obstacledata = str(obstacledata).replace('sphere_radius', 'radius')
obstacledata = str(obstacledata).replace('cylinder_height', 'altitude')
obstacledata = str(obstacledata).replace('cylinder_radius', 'radius')
obstacle = Obstacle(obstacledata)
#


