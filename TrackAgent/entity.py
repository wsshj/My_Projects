import random
import math

class Entity:
    issued = False

    def __init__(self, uid, type, code, camp, maxOfficer, weaveScore, scoutScore, attackScore, damageScore, px, py, pz, rx, ry, rz, speed, com):
        self.uid = uid                      # 实体唯一id
        self.type = type                    # 装备类型
        self.code = code                    # 装备型号
        self.camp = camp                    # 装备阵营
        self.maxOfficer = maxOfficer        # 装备最大载员
        self.weaveScore = weaveScore        # 编组得分
        self.scoutScore = scoutScore        # 被侦察到分数
        self.attackScore = attackScore      # 被歼灭分数
        self.damageScore = damageScore      # 战损分数
        self.px = px                        # x轴位置
        self.py = py                        # y轴位置
        self.pz = pz                        # z轴位置
        self.rx = rx                        # x轴朝向
        self.ry = ry                        # y轴朝向
        self.rz = rz                        # z轴朝向
        self.speed = speed                  # 速度
        self.com = com                      # 通信类对象，用于发消息

    # 更新实体状态
    def update(self, px, py, pz, rx, ry, rz, speed):
        self.px = px
        self.py = py
        self.pz = pz
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.speed = speed

    # 实体测距
    def distance(self, px, pz):
        return math.sqrt(pow(self.px-px, 2) + pow(self.pz-pz, 2))

    # 实体机动
    def move(self, speed, targetPoint, px, pz):
        if len(targetPoint) == 3:
            x = targetPoint[0]
            z = targetPoint[2]
        else:
            x = self.px + px
            z = self.pz + pz

        uids = [self.uid]
        self.com.sendMove(uids, speed, x, z)

    # 侦察
    def scout(self, startAngle, endAngle):
        uids = [self.uid]
        self.com.sendScout(uids, startAngle, endAngle)

    # 打击
    def attack(self, px, pz):
        uids = [self.uid]
        self.com.sendAttack(uids, px, pz)

    # 装载
    def load(self, uuids):
        if self.maxOfficer <= 0:
            print('装备无法装载')
            return 

        self.com.sendLoadSoldier(self.uid, uuids)

    # 卸载
    def Unload(self):
        if self.maxOfficer <= 0:
            print('装备无法卸载')
            return 

        self.com.sendUnloadSoldier(self.uid)

    # 巡航
    def startCruise(self, speed, points):
        if self.type != 5:
            print('只有无人机可以巡航')
            return 

        if self.issued:
            print('该无人机已经在巡航')
            return

        uids = [self.uid]
        self.com.sendStartCruise(uids, speed ,points)
        self.issued = True

    # 取消巡航
    def stopCruise(self):
        if self.type != 5:
            print('只有无人机可以巡航')
            return 

        if not self.issued: 
            print('该无人机未在巡航')
            return

        uids = [self.uid]
        self.com.sendStopCruise(uids)
        self.issued = False