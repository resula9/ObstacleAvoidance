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
        for i in range (0, len(self.__dict__['stationary_obstacles'])):
            real_height = self.stationary_obstacles[i].get('altitude')
            cylinder_radius = self.stationary_obstacles[i].get('radius')
            estimated_altitude = int(real_height) - int(cylinder_radius)
            self.__dict__['stationary_obstacles'][i]['altitude'] = str(estimated_altitude)


file1 = open("obstacles.json", "r")
data = file1.read()
data = str(data).replace('altitude_msl', 'altitude')
data = str(data).replace('sphere_radius', 'radius')
data = str(data).replace('cylinder_height', 'altitude')
data = str(data).replace('cylinder_radius', 'radius')
file2 = open("missions.json", "r")
data2 = file2.read()
obstacle = Obstacle(data)
mission = Mission(data2)
#print obstacle.stationary_obstacles[0].get('altitude')
print mission.fly_zones[0]['boundary_pts'][0]['latitude']
#print mission.home_pos['latitude']
print mission['mission_waypoints']

