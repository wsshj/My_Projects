from configparser import ConfigParser
import os
import sys

class ReadConfig():
    def __init__(self, fileName):
        self.conn = ConfigParser()
        self.filePath = os.path.dirname(os.path.realpath(sys.executable)) + '\\' + fileName

        if not os.path.exists(self.filePath):
            raise FileNotFoundError('文件不存在')

        self.conn.read(self.filePath)

        self.localHost = self.conn.get('network', 'localHost')
        self.host = self.conn.get('network', 'host')
        self.port = int(self.conn.get('network', 'port'))
        self.frequency = int(self.conn.get('network', 'frequency'))

        self.minSpeed = int(self.conn.get('ai', 'minSpeed'))
        self.maxSpeed = int(self.conn.get('ai', 'maxSpeed'))
        self.moveDistance = float(self.conn.get('ai', 'moveDistance'))
        self.targetPoint = []
        if self.conn.get('ai', 'targetLon') != '' and self.conn.get('ai', 'targetLat') != '':
            self.targetPoint.append(float(self.conn.get('ai', 'targetLon')))
            self.targetPoint.append(float(self.conn.get('ai', 'targetLat')))
        self.startAngle = float(self.conn.get('ai', 'startAngle'))
        self.endAngle = float(self.conn.get('ai', 'endAngle'))
        self.moveProbability = int(self.conn.get('ai', 'moveProbability'))
        self.scoutProbability = int(self.conn.get('ai', 'scoutProbability'))
        self.attackProbability = int(self.conn.get('ai', 'attackProbability'))
