# Introduction to Obstacle Avoidance
import numpy as np

file_points = open("mission.waypoints", "r")
lines_points = np.asarray(file_points.read().split('\n'))
point_number = len(lines_points) - 1
points = np.zeros((point_number, 3))  # point number; lat, long, alt
#
home_point = [39.589000, -74.9507, 1]
#
temp_point_number = 10;
temp_points = np.zeros((point_number, temp_point_number, 3))  # point that vehicle reaches; temp_point number; lat, long, alt
#
file_obstacles = open("obstacles.poly", "r")
lines_obstacles = np.asarray(file_obstacles.read().split('\n'))
obstacle_number = len(lines_obstacles) - 1
obstacles = np.zeros((obstacle_number, 5))  # obstacle number; lat, long, alt, radius, speed


def get_points():
    for i in range(0, point_number):
        values = np.asarray(lines_points[i + 1].split('\t'))
        points[i, 0] = values[8]
        points[i, 1] = values[9]
        points[i, 2] = values[10]
    print(points)


def get_obstacles():
    for i in range(0, obstacle_number):
        values = np.asarray(lines_obstacles[i + 1].split(' '))
        print(values)
        obstacles[i, 0] = values[0]
        obstacles[i, 1] = values[1]
        obstacles[i, 2] = values[2]
        obstacles[i, 3] = values[3]
        obstacles[i, 4] = values[4]
    print(obstacles)


def temp_points(points):
    for i in range(0, obstacle_number):
        for j in range(0, temp_point_number):
            if i == 0:
                temp_points[i, j, 0] += (points[i, 0] - home_point[0]) / temp_point_number * j
                temp_points[i, j, 1] += (points[i, 1] - home_point[1]) / temp_point_number * j
                temp_points[i, j, 2] += (points[i, 2] - home_point[2]) / temp_point_number * j

            temp_points[i, j, 0] += (points[i, 0] - points[i - 1, 0]) / temp_point_number * j
            temp_points[i, j, 1] += (points[i, 1] - points[i - 1, 1]) / temp_point_number * j
            temp_points[i, j, 2] += (points[i, 2] - points[i - 1, 2]) / temp_point_number * j


def det_intersections(points, temp_points, obstacles):

    ### Haversine Formula









#Obstaclelarin hareketli ve hareketsiz olanlari ayiralim
#Hareketsiz olanlari ayirdiktan sonra gecen seneki koda benzer sekilde bi algoritma yazalim
#Waypointler arasinda giderken onundeki tahmini hareket noktalarini belirleyelim
#Waypointler arasinda giderken hangi hareketsiz engellere carptigini belirleyelim


#VEYAA
#Hareketsiz ve hareketli diye ayirmadan direkt olarak onune noktalar koyarak ilerledigi dusunuruz tahmini konumlarla
#Hangi engellere carpacagini belirleriz
#Bundan onceyse kisa bir sure engellerin hareketini izleyerek onlarin yollarinin ogrenebilirsek cok guzel olur!!!!
