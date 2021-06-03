import random
import math

Armor = {'无装甲':0, '一般装甲':1, '中等装甲':2, '厚装甲':3}
Equip = {'子弹':0, '榴弹':1, '穿甲弹':2, '炮射导弹':3}
Command = {'士兵':0, '营长':1, '团长':2, '师长':3}
weight = {'equip_level':5,'armor_level':3,'command_level':8, 'distance':2}
entity = {'坦克':0, '步兵':1, '反坦克步兵':2, '装甲车':3, '自行火炮':4, '直升机':5}
distance_ratio = 500

class Entity:
    name = ''
    entity_type = 0
    state = 0
    health_value = 0
    volumes = (0, 0, 0)
    position = (0, 0)
    equip_level = 0
    armor_level = 0
    command_level = 0

    def __init__(self, position, command_level) -> None:
        self.position = position
        self.command_level = command_level

    def print_info(self):
        print(self.name)
        print(self.position)
        print(self.equip_level)
        print(self.armor_level)
        print(self.command_level)


class Tank(Entity) : 
    name = '坦克'
    equip_level = Equip['穿甲弹']
    armor_level = Armor['厚装甲']

class Infantry(Entity) : 
    name = '步兵'
    equip_level = Equip['穿甲弹']
    armor_level = Armor['无装甲']

class AT_Infantry(Entity) : 
    name = '反坦克步兵'
    equip_level = Equip['穿甲弹']
    armor_level = Armor['无装甲']

class Armored_Car(Entity) : 
    name = '装甲车'
    equip_level = Equip['子弹']
    armor_level = Armor['一般装甲']

class Gun(Entity) : 
    name = '自行火炮'
    equip_level = Equip['炮射导弹']
    armor_level = Armor['中等装甲']

class Helicopter(Entity) : 
    name = '直升机'
    equip_level = Equip['炮射导弹']
    armor_level = Armor['中等装甲']

class Own_Entity:
    position = (0, 0)
    cjd_num = 10
    pjd_num = 10

def get_distance(position, position_own):
    return math.sqrt(
            math.pow(position[0] - position_own[0], 2) +
            math.pow(position[1] - position_own[1], 2)
        )


def Ammo_Select(entity, own):
    if entity.entity_type == entity['坦克']: 
        if distance > 800 and own.cjd_num > 0:
            own.cjd_fire(entity_dict[i])
        else
            own.pjd_num -= 1
    elif 

    return ammo_type

def Spread(position, distance, ammo_type):
    position[0] - random.random() 

def onFire(entities, own):
    for entity in entities:
        distance = get_distance(entity.position, own.position)

        heat_level = entity.equip_level * weight['equip_level'] - entity.armor_level * weight['armor_level'] + entity.command_level * weight['command_level'] - distance/distance_ratio * weight['distance']
        entity_dict[heat_level] = entity

    for i in sorted (entity_dict) : 
        ammo_type = Ammo_Select(entity_dict[i], own)

        distance = get_distance(entity.position, own.position)
        Spread(position, distance, ammo_type):
        
        





# 写一个dll 输入：一个敌方实体列表，一个我方实体 输出：我方状态，敌方目标