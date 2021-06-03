import random
import math

Armor = {'无装甲':0, '一般装甲':1, '中等装甲':2, '厚装甲':3}
Equip = {'子弹':0, '榴弹':1, '穿甲弹':2, '炮射导弹':3}
Command = {'士兵':0, '营长':1, '团长':2, '师长':3}
weight = {'equip_level':5,'armor_level':3,'command_level':8, 'distance':2}
entity = {'坦克':0, '步兵':1, '反坦克步兵':2, '装甲车':3, '自行火炮':4, '直升机':5, '永备防御工事':6}
distance_ratio = 500

class Entity:
    entityID = 0
    name = ''

class Equipment(Entity):
    entity_type = 0
    state = 0
    health_value = 0
    volumes = (1, 1)
    position = (0, 0)
    equip_level = 0
    armor_level = 0
    command_level = 0

    def __init__(self, entityID, position=(0, 0), command_level=0) -> None:
        self.entityID = entityID
        self.position = position
        self.command_level = command_level

class Tank(Equipment) : 
    name = '坦克'
    entity_type = entity["坦克"]
    equip_level = Equip['穿甲弹']
    armor_level = Armor['厚装甲']

class Infantry(Equipment) : 
    name = '步兵'
    entity_type = entity["步兵"]
    equip_level = Equip['穿甲弹']
    armor_level = Armor['无装甲']

class AT_Infantry(Equipment) : 
    name = '反坦克步兵'
    entity_type = entity["反坦克步兵"]
    equip_level = Equip['穿甲弹']
    armor_level = Armor['无装甲']

class Armored_Car(Equipment) : 
    name = '装甲车'
    entity_type = entity["装甲车"]
    equip_level = Equip['子弹']
    armor_level = Armor['一般装甲']

class Gun(Equipment) : 
    name = '自行火炮'
    entity_type = entity["自行火炮"]
    equip_level = Equip['炮射导弹']
    armor_level = Armor['中等装甲']

class Helicopter(Equipment) : 
    name = '直升机'
    entity_type = entity["直升机"]
    equip_level = Equip['炮射导弹']
    armor_level = Armor['中等装甲']

class Fortification(Equipment) : 
    name = '永备防御工事'
    entity_type = entity["永备防御工事"]
    equip_level = Equip['穿甲弹']
    armor_level = Armor['厚装甲']

class Ammo(Entity):
    range = (0, 0)
    optional_target = ()
    priority = 255
    hurt = 0
    number = 0
    shoot_number = 0

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

class PJD(Ammo):
    name = '破甲弹'
    range = (0, 2000)
    hurt = 100
    number = 10
    shoot_number = 1

class SJD(Ammo):
    name = '碎甲弹'
    range = (0, 2000)
    hurt =100
    number = 10
    shoot_number = 1

class LD(Ammo):
    name = '榴弹'
    range = (0, 1000)
    hurt = 100
    number = 10
    shoot_number = 1

class PSDD(Ammo):
    name = '炮射导弹'
    range = (0, 3000)
    hurt = 100
    number = 5
    shoot_number = 1

class XKJD(Ammo):
    name = '7.62mm弹'
    range = (0, 800)
    hurt = 50
    number = 1000
    shoot_number = 10

class DKJD(Ammo):
    name = '12.7mm弹'
    range = (0, 1600)
    hurt = 50
    number = 500
    shoot_number = 10

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
        ammo = CJD((entity['坦克'], entity['自行火炮'], entity["永备防御工事"]), 0, 10)
        self.optional_ammo.append(ammo)
        ammo = SJD((entity['坦克'], entity['自行火炮'], entity["永备防御工事"]), 1, 10)
        self.optional_ammo.append(ammo)
        ammo = PJD((entity['坦克'], entity['自行火炮'], entity["永备防御工事"]), 2, 10)
        self.optional_ammo.append(ammo)
        ammo = LD((entity['坦克'], entity['自行火炮'], entity["永备防御工事"]), 3, 10)
        self.optional_ammo.append(ammo)
        ammo = PSDD((entity['坦克'], entity['自行火炮'], entity['装甲车'], entity['直升机']), 4, 5)
        self.optional_ammo.append(ammo)
        ammo = XKJD((entity['步兵'], entity['反坦克步兵']), 0, 1000)
        self.optional_ammo.append(ammo)
        ammo = DKJD((entity['装甲车'], entity['直升机']), 1, 500)
        self.optional_ammo.append(ammo)

    def shoot(self, ammo):
        for ammoself in self.optional_ammo:
            if ammoself == ammo:
                ammoself.shoot()

class War_Report:
    target_id = 0
    target_name = ''
    target_state = ''
    target_position = (0, 0)
    target_size = (0,0)
    hurt_time = {}
    hurt_situation = []

    def print_report(self):
        print("目标编号%s" % self.target_id)
        print("目标名称%s" % self.target_name)
        print("目标状态%s" % self.target_state)
        print("目标位置(%s, %s)" % (self.target_position[0], self.target_position[1]))
        print("目标大小(%s, %s)" % (self.target_size[0], self.target_size[1]))

        print("打击用时%s" % self.hurt_time)
        print("打击状况%s" % self.hurt_situation)

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

def onFire(entities, own):
    entity_dict = {}
    reports = []
    for entity in entities:
        distance = get_distance(entity.position, own.position)

        heat_level = float(entity.equip_level * weight['equip_level']) - float(entity.armor_level * weight['armor_level']) + float(entity.command_level * weight['command_level']) - float(distance/distance_ratio * weight['distance'])
        entity_dict[heat_level] = entity
    
    for i in sorted(entity_dict,reverse=True) : 
        report = War_Report()
        report.target_id = entity_dict[i].entityID
        report.target_name = entity_dict[i].name
        report.target_size = entity_dict[i].volumes
        report.target_position = entity_dict[i].position

        distance = get_distance(entity_dict[i].position, own.position)
        angle = get_angle(entity_dict[i].position, own.position)

        rotation_time = angle_diff(angle, own.rotation)/own.angular_speed
        own.rotation = angle

        while(True):
            spread = Spread(1, 1)

            fire_ammo = Ammo([],255,0)
            for ammo in own.optional_ammo:
                if entity_dict[i].entity_type in ammo.optional_target and ammo.range[1] > distance and ammo.number > 0 and ammo.priority < fire_ammo.priority :
                    fire_ammo = ammo
                    have_ammo = True

            if fire_ammo is Ammo([],255,0):
                print("没有合适的子弹")
                break

            own.shoot(fire_ammo)

            if fire_ammo.number == 0:
                fire_ammo.priority = 255

            if not have_ammo:
                break

            have_ammo = False

            stateDict = {}
            stateDict["着弹点"] = (entity_dict[i].position[0] + spread[0], entity_dict[i].position[1] + spread[1])

            if abs(spread[0]) < entity_dict[i].volumes[0]/2 and abs(spread[1]) < entity_dict[i].volumes[0]/2:
                stateDict['是否击中'] = "击中"
                report.target_state = '损毁'
                report.hurt_situation.append(stateDict)
                break
            else:
                report.target_state = '完好'
                stateDict['是否击中'] = "未击中"

            report.hurt_situation.append(stateDict)

        reports.append(report)

    return reports, own

if __name__ == "__main__":
    own = Own_Entity((0,0), 0, 15)

    entities = [Tank(1, (800,800),Command["士兵"]), Infantry(2, (500,200),Command["师长"])]

    reports , own = onFire(entities, own)

    for ammo in own.optional_ammo:
        print(ammo.number)

    for report in reports:
        report.print_report()
