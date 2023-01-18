from configparser import ConfigParser
import os
import json

import random

from base import bot
from base import middleware
import entity as en

class Agent():
    time = 10

    def __init__(self, scenarioId, favorableTime, weather, myCamp, com):
        self.scenarioId = scenarioId
        self.favorableTime = favorableTime
        self.weather = weather
        self.myCamp = myCamp
        self.com = com

        self.readConfig('config.ini')
        self.scenarioData = self.readJson('scenario.json')

        self.points = self.scenarioData[int(self.scenarioId) - 1][self.myCamp - 1]

    def operation(self, self_entities, enemy_entities, time):
        self.time = time

        uids = []
        r = random.randint(1,10)
        for entity in self_entities:
            if entity.uid % r == 0:
                uids.append(entity.uid)

            if len(uids) == 9:
                break

        self.randomCommand(uids, self_entities, enemy_entities)

    def readConfig(self, fileName):
        conn = ConfigParser()
        filePath = os.path.dirname(os.path.realpath(__file__)) + '\\data\\' + fileName

        if not os.path.exists(filePath):
            raise FileNotFoundError('文件不存在')
            return 

        conn.read(filePath)

        self.minSpeed = int(conn.get('ai', 'minSpeed'))
        self.maxSpeed = int(conn.get('ai', 'maxSpeed'))
        self.moveDistance = float(conn.get('ai', 'moveDistance'))
        self.startAngle = int(conn.get('ai', 'startAngle'))
        self.endAngle = int(conn.get('ai', 'endAngle'))
        self.moveProbability = int(conn.get('ai', 'moveProbability'))
        self.scoutProbability = int(conn.get('ai', 'scoutProbability'))
        self.attackProbability = int(conn.get('ai', 'attackProbability'))

    def readJson(self, fileName):
        with open(os.path.dirname(os.path.realpath(__file__)) + '\\data\\' + fileName, encoding='utf-8') as file_obj:
            contents = file_obj.read()

            return json.loads(contents)

    # 获取目标点
    def getTargetPos(self, entity):
        posArray = []
        
        if self.myCamp == 1:
            if self.time > 360:
                targetPoints = self.points['attackPoints']
            elif self.time > 180:
                targetPoints = self.points['stationPoints']
            else:
                targetPoints = self.points['meetPoints']
        else:
            if self.time > 540:
                targetPoints = self.points['stationPoints']
            elif self.time > 480:
                targetPoints = self.points['attackPoints']
            else:
                targetPoints = self.points['targetPoints']

        # minDis = 99999
        # targetPoint = None
        # for tp in targetPoints:
        #     dis = entity.distance(tp[0], tp[2])
        #     if dis < minDis:
        #         minDis = dis
        #         targetPoint = tp

        targetPoint = targetPoints[random.randint(0,len(targetPoints)-1)]

        if targetPoint is None:
            return []

        return targetPoint

    # 随机下达指令
    def randomCommand(self, uids, self_entities, enemy_entities):
        if len(uids) == 0:
            return

        r = random.randint(1,100)
 
        speed = random.randint(self.minSpeed, self.maxSpeed)

        lon = random.uniform(-self.moveDistance, self.moveDistance)
        lat = random.uniform(-self.moveDistance, self.moveDistance)

        targetPos = []
        targetPos = self.getTargetPos(self_entities[random.randint(0,len(self_entities)-1)])

        if r <= self.moveProbability:
            self.com.sendMove(uids, speed, targetPos[0], targetPos[2])
        elif r <= (self.moveProbability + self.scoutProbability):
            self.com.sendScout(uids, self.startAngle, self.endAngle)
        elif r <= (self.moveProbability + self.scoutProbability + self.attackProbability):
            if len(enemy_entities) == 0:
                return

            enemy = enemy_entities[random.randint(0,len(enemy_entities)-1)]
                
            self.com.sendAttack(uids, enemy.px, enemy.pz)
        else:
            return
