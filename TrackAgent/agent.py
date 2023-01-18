from configparser import ConfigParser
import os
import json

import random

from base import bot
from base import middleware
import entity as en

class Agent():
    def __init__(self, scenarioId, favorableTime, weather, myCamp):
        self.scenarioId = scenarioId
        self.favorableTime = favorableTime
        self.weather = weather
        self.myCamp = myCamp

        self.readConfig('config.ini')
        self.scenarioData = self.readJson('scenario.json')

        self.points = self.scenarioData[int(self.scenarioId) - 1][self.myCamp - 1]

    def operation(self, self_entities, enemy_entities):
        for entity in self_entities:
            self.randomCommand(entity, self_entities, enemy_entities)

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
        targetPoints = self.points['targetPoints']

        minDis = 9999
        targetPoint = None
        for tp in targetPoints:
            dis = entity.distance(tp[0], tp[2])
            if dis < minDis:
                minDis = dis
                targetPoint = tp

        if targetPoint is None:
            return []

        return targetPoint

    # 随机下达指令
    def randomCommand(self, entity, self_entities, enemy_entities):
        print('randomCommand')
        r = random.randint(1,100)

        if entity.type == 5 and not entity.issued:
            points = self.points['targetPoints'] + self.points['attackPoints']
            entity.startCruise(self.maxSpeed, points)
            return

        if entity.type == 5 and entity.issued:
            entity.stopCruise()
            return

        if entity.maxOfficer > 0:
            uuids = []
            for se in self_entities:
                if se.type == 6:
                    uuids.append(se.uid)
            entity.load(uuids)
 
        speed = random.randint(self.minSpeed, self.maxSpeed)

        lon = random.uniform(-self.moveDistance, self.moveDistance)
        lat = random.uniform(-self.moveDistance, self.moveDistance)

        targetPos = []
        targetPos = self.getTargetPos(entity)

        entity.move(speed, targetPos, lon, lat)

        if entity.maxOfficer > 0:
            entity.Unload()

        if r <= (self.moveProbability + self.scoutProbability):
            entity.scout(self.startAngle, self.endAngle)
        elif r <= (self.moveProbability + self.scoutProbability + self.attackProbability):
            if len(enemy_entities) == 0:
                return

            for enemy in enemy_entities:
                entity.attack(enemy.px, enemy.pz)
        else:
            return
