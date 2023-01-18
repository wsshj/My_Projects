from configparser import ConfigParser
import json
import os

from base import middleware
from base import bot

class ReadConfig():
    def __init__(self, fileName):
        conn = ConfigParser()
        filePath = os.path.dirname(os.path.realpath(__file__)) + '\\data\\' + fileName

        if not os.path.exists(filePath):
            raise FileNotFoundError('文件不存在')

        conn.read(filePath)

        self.localHost = conn.get('network', 'localHost')
        self.host = conn.get('network', 'host')
        self.port = int(conn.get('network', 'port'))
        self.frequency = float(conn.get('network', 'frequency'))

def readJson(fileName):
    # with open(os.path.dirname(os.path.realpath(__file__)) + '\\data\\' + fileName, encoding='utf-8') as file_obj:
    with open(os.path.dirname(os.path.realpath(__file__)) + '\\data\\' + fileName, encoding='utf-8') as file_obj:
        contents = file_obj.read()

        return json.loads(contents)

if __name__ == '__main__':
    conf = ReadConfig('config.ini')
    equipDatas = readJson('EquipData.json')
    
    bot = bot.Bot(conf.localHost, conf.host, conf.port, equipDatas)

    bot.run(conf.frequency)