import os 
import random
import math

ARMOR = {'无装甲':0, '一般装甲':1, '中等装甲':2, '厚装甲':3}
EQUIP = {'子弹':0, '榴弹':1, '穿甲弹':2, '炮射导弹':3}
COMMAND = {'士兵':0, '营长':1, '团长':2, '师长':3}
WEIGHT = {'equip_level':5,'armor_level':3,'command_level':8, 'distance':2}
ENTITY = {'坦克':0, '步兵':1, '反坦克步兵':2, '装甲车':3, '自行火炮':4, '直升机':5, '永备防御工事':6}

distance_ratio = 500

class Entity:
    entityID = 0
    name = ''

class Equipment(Entity):
    entity_type = 0
    state = 0
    health_value = 0
    volumes = (10, 10)
    position = (0, 0)
    equip_level = 0
    armor_level = 0
    command_level = 0

    def __init__(self, name, entityID, position=(0, 0), command_level=0) -> None:
        self.name = name
        self.entityID = entityID
        self.position = position
        self.command_level = command_level

class Tank(Equipment) : 
    name = '坦克'
    entity_type = ENTITY["坦克"]
    volumes = (8, 3)
    equip_level = EQUIP['穿甲弹']
    armor_level = ARMOR['厚装甲']

class Infantry(Equipment) : 
    name = '步兵'
    entity_type = ENTITY["步兵"]
    volumes = (1, 2)
    equip_level = EQUIP['子弹']
    armor_level = ARMOR['无装甲']

class AT_Infantry(Equipment) : 
    name = '反坦克步兵'
    entity_type = ENTITY["反坦克步兵"]
    volumes = (1, 2)
    equip_level = EQUIP['穿甲弹']
    armor_level = ARMOR['无装甲']

class Armored_Car(Equipment) : 
    name = '装甲车'
    entity_type = ENTITY["装甲车"]
    volumes = (7, 3)
    equip_level = EQUIP['子弹']
    armor_level = ARMOR['一般装甲']

class Gun(Equipment) : 
    name = '自行火炮'
    entity_type = ENTITY["自行火炮"]
    volumes = (8, 3)
    equip_level = EQUIP['炮射导弹']
    armor_level = ARMOR['中等装甲']

class Helicopter(Equipment) : 
    name = '直升机'
    entity_type = ENTITY["直升机"]
    volumes = (7, 4)
    equip_level = EQUIP['炮射导弹']
    armor_level = ARMOR['中等装甲']

class Fortification(Equipment) : 
    name = '永备防御工事'
    entity_type = ENTITY["永备防御工事"]
    volumes = (10, 10)
    equip_level = EQUIP['穿甲弹']
    armor_level = ARMOR['厚装甲']

class Ammo(Entity):
    range = (0, 0)
    optional_target = ()
    priority = 255
    hurt = 0
    number = 0
    shoot_number = 0
    shoot_speed = 0
    BF_value = 5
    BG_value = 5
    initial_speed = 0

    def __init__(self, optional_target, priority, number) -> None:
        self.optional_target = optional_target
        self.priority = priority
        self.number = number

    def shoot(self):
        self.number -= self.shoot_number

class CJD(Ammo):
    name = '穿甲弹'
    range = (0, 2000)
    hurt = 100
    number = 10
    shoot_number = 1
    shoot_speed = 5 #秒/发
    initial_speed = 1500
    BF_value = 4
    BG_value = 4

class PJD(Ammo):
    name = '破甲弹'
    range = (0, 2000)
    hurt = 100
    number = 10
    shoot_number = 1
    shoot_speed = 6 #秒/发
    initial_speed = 1400
    BF_value = 4
    BG_value = 4

class SJD(Ammo):
    name = '碎甲弹'
    range = (0, 2000)
    hurt =100
    number = 10
    shoot_number = 1
    shoot_speed = 7 #秒/发
    initial_speed = 1300
    BF_value = 4
    BG_value = 4

class LD(Ammo):
    name = '榴弹'
    range = (0, 1000)
    hurt = 100
    number = 10
    shoot_number = 1
    shoot_speed = 4 #秒/发
    initial_speed = 800
    BF_value = 5
    BG_value = 5

class PSDD(Ammo):
    name = '炮射导弹'
    range = (0, 3000)
    hurt = 100
    number = 5
    shoot_number = 1
    shoot_speed = 10 #秒/发
    initial_speed = 1200
    BF_value = 1
    BG_value = 1

class XKJD(Ammo):
    name = '7.62mm弹'
    range = (0, 800)
    hurt = 50
    number = 1000
    shoot_number = 1
    shoot_speed = 0.1 #秒/发
    initial_speed = 800
    BF_value = 1
    BG_value = 2

class DKJD(Ammo):
    name = '12.7mm弹'
    range = (0, 1600)
    hurt = 50
    number = 500
    shoot_number = 1
    shoot_speed = 0.1 #秒/发
    initial_speed = 1000
    BF_value = 1
    BG_value = 2

class Own_Entity(Entity):
    name = '我方坦克'
    position = (0, 0)
    rotation = 0
    angular_speed = 0
    optional_ammo = []
    

    def __init__(self, position, rotation, angular_speed) -> None:
        super().__init__()
        self.init_ammo()
        self.position = position
        self.rotation = rotation
        self.angular_speed = angular_speed

    def init_ammo(self):
        ammo = CJD((ENTITY['坦克'], ENTITY['自行火炮'], ENTITY["永备防御工事"]), 0, 10)
        self.optional_ammo.append(ammo)
        ammo = SJD((ENTITY['坦克'], ENTITY['自行火炮'], ENTITY["永备防御工事"]), 1, 10)
        self.optional_ammo.append(ammo)
        ammo = PJD((ENTITY['坦克'], ENTITY['自行火炮'], ENTITY["永备防御工事"]), 2, 10)
        self.optional_ammo.append(ammo)
        ammo = LD((ENTITY['坦克'], ENTITY['自行火炮'], ENTITY["永备防御工事"]), 3, 10)
        self.optional_ammo.append(ammo)
        ammo = PSDD((ENTITY['坦克'], ENTITY['自行火炮'], ENTITY['装甲车'], ENTITY['直升机']), 4, 5)
        self.optional_ammo.append(ammo)
        ammo = XKJD((ENTITY['步兵'], ENTITY['反坦克步兵']), 0, 1000)
        self.optional_ammo.append(ammo)
        ammo = DKJD((ENTITY['步兵'], ENTITY['反坦克步兵'], ENTITY['装甲车'], ENTITY['直升机']), 1, 500)
        self.optional_ammo.append(ammo)

    def shoot(self, ammo):
        for ammoself in self.optional_ammo:
            if ammoself == ammo:
                ammoself.shoot()

    def print(self):
        print("装备名称：%s" % self.name)
        print("装备位置：(%s,%s)" % (self.position[0], self.position[1]))
        print("装备朝向：%s" % self.rotation)
        print("调炮速度：%s" % self.angular_speed)
        for ammo in self.optional_ammo:
            print("弹种：%s，剩余数量：%s" % (ammo.name, ammo.number))

class War_Report:
    target_id = 0
    target_name = ''
    target_state = ''
    priority = 0
    target_position = (0, 0)
    target_distance = 0
    target_size = (0,0)
    hurt_time = {}
    hurt_situation = []
    remarks = ''

    def reset(self):
        self.target_id = 0
        self.target_name = ''
        self.target_state = ''
        self.priority = 0
        self.target_position = (0, 0)
        self.target_distance = 0
        self.target_size = (0,0)
        self.hurt_time = {}
        self.hurt_situation = []
        self.remarks = ''

    def print_report(self):
        print("目标编号：%s" % self.target_id)
        print("目标名称：%s" % self.target_name)
        print("目标状态：%s" % self.target_state)
        print("打击优先级：%s" %self.priority)
        print("目标位置：(%s, %s)" % (self.target_position[0], self.target_position[1]))
        print("目标距离：%s" % self.target_distance)
        print("目标大小：(%s, %s)" % (self.target_size[0], self.target_size[1]))

        print("打击用时：%s" % self.hurt_time)
        print("打击状况：%s" % self.hurt_situation)

        if self.remarks != '':
            print('备注：%s' % self.remarks)

def get_distance(position, position_own):
    return math.sqrt(
            math.pow(position[0] - position_own[0], 2) +
            math.pow(position[1] - position_own[1], 2)
        )

def get_angle(position, position_own):
    return math.degrees(math.atan((position[0] - position_own[0])/(position[1] - position_own[1])))

def angle_diff(unit1, unit2):
    phi = abs(unit2 - unit1) % 360
    sign = 1
    # used to calculate sign
    if not ((unit1-unit2 >= 0 and unit1-unit2 <= 180) or (
            unit1-unit2 <= -180 and unit1-unit2 >= -360)):
        sign = -1
    if phi > 180:
        result = 360-phi
    else:
        result = phi

    return abs(result*sign)

def Spread(Bf, Bg):
    R1 = random.random()
    R2 = random.random()

    x = Bf * math.cos(2*math.pi*R2) * math.sqrt(-math.log(R1)/0.2274768)
    y = Bg * math.sin(2*math.pi*R2) * math.sqrt(-math.log(R1)/0.2274768)

    return (x, y)

def take_heatlevel(elem):
    return elem['heat_level']

def onFire(entities, own):
    entity_list = []
    reports = []
    for entity in entities:
        entity_dict = {}
        distance = get_distance(entity.position, own.position)

        heat_level = float(entity.equip_level * WEIGHT['equip_level']) - float(entity.armor_level * WEIGHT['armor_level']) + float(entity.command_level * WEIGHT['command_level']) - float(distance/distance_ratio * WEIGHT['distance'])
        
        entity_dict['heat_level'] = heat_level
        entity_dict['entity'] = entity
        entity_list.append(entity_dict)

    entity_list.sort(key=take_heatlevel, reverse=True)
    
    for entity_dict in entity_list: 
        report = War_Report()
        report.reset()
        report.target_id = entity_dict['entity'].entityID
        report.target_name = entity_dict['entity'].name
        report.priority = entity_dict['heat_level']
        report.target_size = entity_dict['entity'].volumes
        report.target_position = entity_dict['entity'].position

        distance = get_distance(entity_dict['entity'].position, own.position)
        report.target_distance = round(distance, 3)

        angle = get_angle(entity_dict['entity'].position, own.position)

        total_time = 0
        rotation_time = angle_diff(angle, own.rotation)/own.angular_speed
        report.hurt_time["调炮用时"] = round(rotation_time, 3)

        own.rotation = angle

        available = True

        while(True):
            fire_ammo = Ammo([],255,0)
            for ammo in own.optional_ammo:
                if entity_dict['entity'].entity_type in ammo.optional_target and ammo.range[1] > distance and ammo.number > 0 and ammo.priority < fire_ammo.priority :
                    fire_ammo = ammo
                    have_ammo = True

            if fire_ammo.initial_speed == 0:
                available = False
                break

            own.shoot(fire_ammo)

            spread = Spread(fire_ammo.BF_value, fire_ammo.BG_value)

            if fire_ammo.number == 0:
                fire_ammo.priority = 255

            if not have_ammo:
                break

            have_ammo = False

            stateDict = {}
            stateDict["弹种"] = fire_ammo.name
            stateDict["弹着点"] = (round(entity_dict['entity'].position[0] + spread[0], 3), round(entity_dict['entity'].position[1] + spread[1], 3))

            if abs(spread[0]) < entity_dict['entity'].volumes[0]/2 and abs(spread[1]) < entity_dict['entity'].volumes[0]/2:
                stateDict['是否击中'] = "击中"
                report.target_state = '损毁'
                report.hurt_situation.append(stateDict)
                total_time += fire_ammo.shoot_speed
                break
            else:
                report.target_state = '完好'
                stateDict['是否击中'] = "未击中"

            report.hurt_situation.append(stateDict)
            total_time += fire_ammo.shoot_speed

        if not available:
            report.remarks = "没有合适的弹药"
            break
        
        # report.hurt_time["装填用时"] = round(total_time, 3)
        total_time += distance/fire_ammo.initial_speed
        report.hurt_time["射击用时"] = round(total_time, 3)
        total_time += rotation_time
        report.hurt_time["总用时"] = round(total_time, 3)
        reports.append(report)

    return reports, own

if __name__ == "__main__":
    own = Own_Entity((0,0), 0, 15)

    entities = [
        Tank('坦克A', 1, (800,800),COMMAND["士兵"]), 
        Infantry('步兵A', 2, (-500,200),COMMAND["士兵"]),
        AT_Infantry('反坦克步兵A', 3, (600,600),COMMAND["士兵"]), 
        Armored_Car('装甲车A', 4, (-500,-200),COMMAND["士兵"]),
        Gun('自行火炮A', 5, (1000,1000),COMMAND["士兵"]), 
        Helicopter('直升机A', 6, (400,700),COMMAND["士兵"]),
        Fortification('永备防御工事A', 7, (800,-800),COMMAND["士兵"]), 
        Tank('坦克B', 8, (500,200),COMMAND["营长"]),
        Tank('坦克C', 9, (-800,-800),COMMAND["团长"]), 
        Tank('坦克D', 10, (1500,2000),COMMAND["师长"]),
        ]

    print("我方装备初始化状态：")
    own.print()

    reports , own = onFire(entities, own)    

    print("\n被打击目标的状态：")
    for report in reports:
        print()
        report.print_report()

    print("\n我方装备现状态：")
    own.print()

    
    for i in range(100):
        R1 = random.random()
        R2 = random.random()
        print(math.cos(2*math.pi*R2) * math.sqrt(-math.log(R1)/0.2274768))

    os.system('pause')