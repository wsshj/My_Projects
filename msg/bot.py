import time
import random

import middleware
import entity as en
import readConfig

class Bot():
    myCamp = 0

    self_entities = []
    enemy_entities = []

    isRun = False
    isConnect = False

    def __init__(self, localHost, host, port):
        self.localHost = localHost

        self.com = middleware.Communication(localHost, host, port)
        self.com.init()
        
        self.com.registerFun(14038, self.recvConnectSuccess)
        self.com.registerFun(14015, self.recvStartDeploy)
        self.com.registerFun(14016, self.recvStartGame)
        self.com.registerFun(14203, self.recvGameOver)
        self.com.registerFun(14801, self.recvScore)
        self.com.registerFun(14219, self.recvResetGame)

        self.com.registerFun(14306, self.recvEquipSyn)
        self.com.registerFun(14207, self.recvEquipDamage)
    
    def getAIInfo(self, minSpeed, maxSpeed, moveDistance, startAngle, endAngle, targetPoint, moveProbability, scoutProbability, attackProbability):
        self.minSpeed = minSpeed
        self.maxSpeed = maxSpeed
        self.moveDistance = moveDistance
        self.startAngle = startAngle
        self.endAngle = endAngle
        self.targetPoint = targetPoint
        self.moveProbability = moveProbability
        self.scoutProbability = scoutProbability
        self.attackProbability = attackProbability

    def randomCommand(self, entity):
        r = random.randint(1,100)

        if r <= self.moveProbability:
            speed = random.randint(self.minSpeed, self.maxSpeed)

            lon = random.uniform(-self.moveDistance, self.moveDistance)
            lat = random.uniform(-self.moveDistance, self.moveDistance)

            entity.move(speed, self.targetPoint, lon, lat)
        elif r <= (self.moveProbability + self.scoutProbability):
            entity.scout(self.startAngle, self.endAngle)
        elif r <= (self.moveProbability + self.scoutProbability + self.attackProbability):
            if len(self.enemy_entities) == 0:
                return

            enemy = self.enemy_entities[0]
            dis = entity.distance(self.enemy_entities[0].longitude, self.enemy_entities[0].latitude)

            for e in self.enemy_entities:
                d = entity.distance(e.longitude, e.latitude)
                if d < dis:
                    dis = d
                    enemy = e
            
            entity.attack(enemy.longitude, enemy.latitude)
        else:
            return

    # def run(self, frequency):
    #     self.com.start()

    #     try:
    #         self.com.sendConnect(self.localHost)
    #     except:
    #         print('服务端未启动')
    #         return

    #     while(True):
    #         print('等待部署...')
    #         time.sleep(5)
    #         while(self.isRun):
    #             for entity in self.self_entities:
    #                 self.randomCommand(entity)
                
    #             time.sleep(frequency)

    def run(self, frequency):
        self.com.start()

        while(not self.isConnect):
            try:
                self.com.sendConnect(self.localHost)
            except:
                print('等待连接...')
                
            time.sleep(5)

        while(True):
            print('等待部署...')
            time.sleep(5)
            while(self.isRun):
                for entity in self.self_entities:
                    self.randomCommand(entity)
                
                time.sleep(frequency)
            
    # 接收开始部署
    def recvConnectSuccess(self, data):
        print('连接成功')
        self.isConnect = True

    # 接收终端装备加载数据
    def recvBaseInfo(self, data):
        self.myCamp = data['camp']
        print('接收到推演基本信息')

        self.com.sendLoadComplete(self.localHost)  

    # 接收开始部署
    def recvStartDeploy(self, data):
        print('部署开始')
        self.myCamp = data['camp']

        self.com.sendDeployComplete(self.localHost)

    # 接收开始推演
    def recvStartGame(self, data):
        self.isRun = True
        print('推演开始')

    # 接收比赛结束
    def recvGameOver(self, data):
        self.isRun = False
        self.com.reset()
        self.self_entities.clear()
        self.enemy_entities.clear()
        print('推演结束')

    # 接收比赛得分
    def recvScore(self, data):
        print('该场推演的得分为：%s' % (data['score']))

    # 接收重置推演
    def recvResetGame(self, data):
        self.com.sendResetComplete(self.localHost)
        
    # 接收同步状态数据
    def recvEquipSyn(self, data):
        isExist = False

        if self.myCamp == 0:
            return

        if data['camp'] == self.myCamp:
            for entity in self.self_entities:
                if entity.code == data['code'] and entity.id == data['id']:
                    entity.update(data['longi'], data['lat'], data['h'], data['rx'], data['ry'], data['rz'])
                    isExist = True
                    break

            if not isExist:
                entity = en.Entity(data['code'], data['id'], data['camp'], data['longi'], data['lat'], data['h'], data['rx'], data['ry'], data['rz'], self.com)
                self.self_entities.append(entity)
                print('我方列表添加 code:%s, id:%s' % (data['code'], data['id']))
        else:
            for entity in self.enemy_entities:
                if entity.code == data['code'] and entity.id == data['id']:
                    entity.update(data['longi'], data['lat'], data['h'], data['rx'], data['ry'], data['rz'])
                    isExist = True
                    break

            if not isExist:
                entity = en.Entity(data['code'], data['id'], data['camp'], data['longi'], data['lat'], data['h'], data['rx'], data['ry'], data['rz'], self.com)
                self.enemy_entities.append(entity)
                print('敌方列表添加 code:%s, id:%s' % (data['code'], data['id']))

    def recvEquipDamage(self, data):
        if self.myCamp == 0:
            return

        if data['damag_rate'] == 3:
            if data['enemy_camp'] == self.myCamp:
                for entity in self.self_entities:
                    if entity.code == data['enemy_code'] and entity.id == data['enemy_id']:
                        self.self_entities.remove(entity)
                        break
            else:
                for entity in self.enemy_entities:
                    if entity.code == data['enemy_code'] and entity.id == data['enemy_id']:
                        self.enemy_entities.remove(entity)
                        break

            print('camp:%s, code:%s, id:%s 被击毁' % (data['enemy_camp'], data['enemy_code'], data['enemy_id']))
    