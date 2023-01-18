import time
import random
import struct

from base import middleware
import entity as en
import agent
import agent_b

class Bot():
    myCamp = 0
    scenarioId = 0
    favorableTime = 0
    weather = 0
    time = 10
    agent = None

    self_entities = []
    enemy_entities = []
    myScenario = []

    isConnect = False
    isRun = False

    def __init__(self, localHost, host, port, equipDatas):
        self.localHost = localHost

        self.com = middleware.Communication(localHost, host, port)
        self.com.init()
        
        self.com.registerFun(14038, self.recvConnectSuccess)
        self.com.registerFun(14031, self.recvGameInfo)
        self.com.registerFun(14032, self.recvStartGame)
        self.com.registerFun(14035, self.recvStartDeploy)
        self.com.registerFun(14219, self.recvResetGame)
        self.com.registerFun(14801, self.recvGameOver)

        self.com.registerFun(14201, self.recvEquipSyn)
        self.com.registerFun(14203, self.recvTimeSyn)
        self.com.registerFun(14303, self.recvEquipDamage)
        self.com.registerFun(14301, self.recvEquipLose)

        self.equipDatas = equipDatas

    # 运行主循环
    def run(self, frequency):
        self.com.start()

        while(True):
            while(not self.isConnect):
                try:
                    self.com.sendConnect(self.localHost)
                except:
                    print('服务端未启动,等待连接...')
                
                time.sleep(5)

            print('等待比赛...')
            time.sleep(5)

            if self.isRun:
                # self.agent = agent.Agent(self.scenarioId, self.favorableTime, self.weather, self.myCamp) # 智能体对象
                self.agent_b = agent_b.Agent(self.scenarioId, self.favorableTime, self.weather, self.myCamp, self.com) # 智能体b对象

            while(self.isRun): 
                # self.agent.operation(self.self_entities, self.enemy_entities)  # 智能体操作
                self.agent_b.operation(self.self_entities, self.enemy_entities, self.time)  # 智能体b操作
                
                time.sleep(frequency)

    # 接收连接成功            
    def recvConnectSuccess(self, data):
        format = '=i%dsi' % int.from_bytes(data[0:4], byteorder="little")
        info = struct.unpack(format, data)
        if info[1] == bytes(self.localHost, encoding='utf-8'):
            self.baseOrder = info[2]
            self.isConnect = True
            print('连接成功')

    # 接收比赛信息
    def recvGameInfo(self, data):
        format = '=i%ds4bi' % int.from_bytes(data[0:4],byteorder="little")
        info = struct.unpack(format, data)

        self.scenarioId = str(info[1], 'utf-8')
        self.favorableTime = info[2]
        self.weather = info[3]
        self.myCamp = info[4]
        
        print('想定ID：%s，天时：%s，天气：%s，阵营：%s' % 
            (self.scenarioId, self.favorableTime, self.weather, self.myCamp))

        self.com.sendLoadComplete(self.localHost)

    # 接收开始部署
    def recvStartDeploy(self, data):
        print('部署开始')
        self.com.sendDeployComplete(self.localHost)

    # 接收开始推演
    def recvStartGame(self, data):
        self.com.reset(self.baseOrder)
        self.isRun = True
        print('推演开始')

    # 接收时间同步
    def recvTimeSyn(self, data):
        info = struct.unpack('=f', data)
        self.time = info[0]

    # 接收比赛结束,得分
    def recvGameOver(self, data):
        self.isRun = False

        scores = []
        b = 0
        for i in range(6):
            score = str(data[b+4:b+4+int.from_bytes(data[b:4+b],byteorder="little")], 'utf-8')
            scores.append(score)
            b += (4 + int.from_bytes(data[b:b + 4],byteorder="little"))

        scoreDict = {}
        scoreDict['totalScore'] = float(scores[0])          # 总分
        scoreDict['groupScore'] = float(scores[1])          # 编组分
        scoreDict['scoutScore'] = float(scores[2])          # 侦察分
        scoreDict['attackScore'] = float(scores[3])         # 打击分
        scoreDict['damageScore'] = float(scores[4])         # 毁伤分
        scoreDict['timeScore'] = float(scores[5])           # 时间分
        scoreDict['isSuccesed'] = int.from_bytes(data[b:b + 4],byteorder="little")      #是否完成任务
        
        print('推演结束，得分：%s' % scoreDict)

    # 接收重置比赛
    def recvResetGame(self, data):
        print('重置比赛')
        self.com.reset(self.baseOrder)
        self.self_entities.clear()
        self.enemy_entities.clear()
        self.com.sendResetComplete(self.localHost)

    # 同步状态数据
    def EquipSyn(self, entities, uid, type, camp, code, px, py, pz, rx, ry, rz, speed):
        isExist = False

        for entity in entities:
            if entity.uid == uid:
                entity.update(px, py, pz, rx, ry, rz, speed)
                isExist = True
                break

        if not isExist:
            maxOfficer = 0
            weaveScore = 0
            scoutScore = 0
            attackScore = 0
            damageScore = 0

            for equipData in self.equipDatas:
                if code == equipData['code']:
                    maxOfficer = equipData['max_officer']
                    weaveScore = int(equipData['weave_score'].split(',')[int(self.scenarioId) - 1])
                    scoutScore = int(equipData['scout_score'].split(',')[int(self.scenarioId) - 1])
                    attackScore = int(equipData['attack_score'].split(',')[int(self.scenarioId) - 1])
                    damageScore = int(equipData['damage_score'].split(',')[int(self.scenarioId) - 1])

            entity = en.Entity(uid, type, code, camp, maxOfficer, weaveScore, scoutScore, attackScore, damageScore, px, py, pz, rx, ry, rz, speed, self.com)
            entities.append(entity)
            print('实体列表添加：uid：%s，camp：%s' % (uid, camp))
            # print('%s,%s,%s,%s,%s,%s,%s,%s,%s' % (entity.uid,entity.type,entity.code,entity.camp,entity.maxOfficer,entity.weaveScore,entity.scoutScore,entity.attackScore,entity.damageScore))

    # 接收同步状态数据
    def recvEquipSyn(self, data):
        if self.myCamp == 0:
            return

        info = struct.unpack('=HQb7f', data)

        eData = {}
        eData['uid'] = info[1] # 装备uid
        eData['type'] = int.from_bytes(data[2:3],byteorder="little") # 装备类型
        eData['camp'] = int.from_bytes(data[3:4],byteorder="little") # 装备阵营
        eData['code'] = int.from_bytes(data[4:6],byteorder="little") # 装备编号
        eData['px'] = info[3] # 装备x轴坐标
        eData['py'] = info[4] # 装备y轴坐标
        eData['pz'] = info[5] # 装备z轴坐标
        eData['rx'] = info[6] # 装备x轴朝向
        eData['ry'] = info[7] # 装备y轴朝向
        eData['rz'] = info[8] # 装备z轴朝向
        eData['speed'] = info[9] # 装备速度

        if eData['camp'] == self.myCamp:
            self.EquipSyn(self.self_entities, eData['uid'], eData['type'], eData['camp'], eData['code'], info[3], info[4], info[5], info[6], info[7], info[8], info[9])
        else:
            self.EquipSyn(self.enemy_entities, eData['uid'], eData['type'], eData['camp'], eData['code'], info[3], info[4], info[5], info[6], info[7], info[8], info[9])

    # 接收毁伤信息
    def recvEquipDamage(self, data):
        if self.myCamp == 0:
            return

        damagRate = int.from_bytes(data[25:26],byteorder="little") # 毁伤率大于等于3为销毁
        uid = int.from_bytes(data[8:16],byteorder="little") # 装备uid
        camp = int.from_bytes(data[9:10],byteorder="little") # 装备阵营

        if damagRate >= 3:
            if camp == self.myCamp:
                for entity in self.self_entities:
                    if entity.uid == uid:
                        self.self_entities.remove(entity)
                        break
            else:
                for entity in self.enemy_entities:
                    if entity.uid == uid:
                        self.enemy_entities.remove(entity)
                        break

            print('camp:%s, uid:%s 被击毁' % (camp, uid))

    # 接收侦察丢失
    def recvEquipLose(self, data):
        if self.myCamp == 0:
            return

        uid = int.from_bytes(data[8:16],byteorder="little") # 装备uid
        camp = int.from_bytes(data[9:10],byteorder="little") # 装备阵营
        state = int.from_bytes(data[16:17],byteorder="little") # 侦察状态，0为未侦察到，也就是目标丢失

        if state == 0:
            for entity in self.enemy_entities:
                if entity.uid == uid:
                    self.enemy_entities.remove(entity)
                    print('camp:%s,  uid:%s 目标位置丢失' % (camp, uid))
                    break

                    