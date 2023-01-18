import random
import math

class Entity:
    # self.code = ''
    # self.id = -1
    # self.camp = 0
    # self.longitude = 0.0
    # self.latitude = 0.0
    # self.height = 0.0
    # self.rx = 0.0
    # self.ry = 0.0
    # self.rz = 0.0

    def __init__(self, code, id, camp, longitude, latitude, height, rx, ry, rz, com):
        self.code = code
        self.id = id
        self.camp = camp
        self.longitude = longitude
        self.latitude = latitude
        self.height = height
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.com = com

    def update(self, longitude, latitude, height, rx, ry, rz):
        self.longitude = longitude
        self.latitude = latitude
        self.height = height
        self.rx = rx
        self.ry = ry
        self.rz = rz

    def distance(self, longitude, latitude):
        return pow(self.longitude-longitude, 2) + pow(self.latitude-latitude, 2)

    def move(self, speed, targetPoint, lon, lat):
        if len(targetPoint) == 2:
            longitude = targetPoint[0]
            latitude = targetPoint[1]
        else:
            longitude = self.longitude + lon
            latitude = self.latitude + lat

        self.com.sendMove(self.code, self.id, self.camp, speed, 0, longitude, latitude)

    def scout(self, startAngle, endAngle):
        self.com.sendScout(self.code, self.id, self.camp, startAngle, endAngle)

    def attack(self, longitude, latitude):
        self.com.sendAttack(self.code, self.id, self.camp, 0, longitude, latitude)
