
Armor = {'无装甲':0, '一般装甲':1, '中等装甲':2, '厚装甲':3}
Equip = {'子弹':0, '榴弹':1, '穿甲弹':2, '炮射导弹':3}
Command = {'士兵':0, '营长':1, '团长':2, '师长':3}
weight = {'equip_level':5,'armor_level':3,'command_level':8}

class Entity:
    name = ''
    state = 0
    health_value = 0
    volumes = (0, 0, 0)
    position = (0, 0)
    equip_level = 0
    armor_level = 0
    command_level = 0

    def __init__(self, position, equip_level, armor_level, command_level) -> None:
        self.position = position
        self.equip_level = equip_level
        self.armor_level = armor_level
        self.command_level = command_level

    def print_info(self):
        print(self.name)
        print(self.position)
        print(self.equip_level)
        print(self.armor_level)
        print(self.command_level)


class Tank(Entity) : 
    name = '坦克'
    state = 0
    health_value = 0
    volumes = (0, 0, 0)
    position = (600, 800)
    equip_level = Equip['穿甲弹']
    armor_level = Armor['厚装甲']
    command_level = Command['士兵']


def onFire(entities, own):
    for entity in entities:
        entity.equip_level * weight['equip_level'] - entity.armor_level * weight['armor_level'] + entity.command_level * weight['command_level']

    own



# 写一个dll 输入：一个敌方实体列表，一个我方实体 输出：我方状态，敌方目标