import socket
import threading
import json
import inspect
import ctypes
import struct
    
# 接收消息线程
class Receive(threading.Thread):
    def __init__(self, threadID, name, counter, skt, bufSize):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.skt = skt
        self.BUFSIZE = bufSize
        self.funs = []

    def register(self, id, fun):
        f = {}
        f['id'] = id
        f['fun'] = fun
        self.funs.append(f)

    # 接收消息并创建回调函数
    def recv(self):
        while True:
            try:
                data = self.skt.recvfrom(self.BUFSIZE)[0]
            except Exception as e:
                print('接收失败')
                continue

            for f in self.funs:
                if int.from_bytes(data[4:6],byteorder="little") == f['id']:
                    f['fun'](data[10:10+int.from_bytes(data[6:10],byteorder="little")])
    
    # 运行接收消息线程
    def run(self):
        print ("接收线程开始:" + self.name)
        self.recv()

# 通信类
class Communication:
    def __init__(self, localHost, host, port, bufSize = 1024):
        self.orderId = 0

        self.BUFSIZE = bufSize
        self.recv_ip_port = (localHost, (10000 + (int(localHost.split('.')[3])*10))+3)
        self.send_ip_port = (host, int(port))

        self.skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.skt.bind(self.recv_ip_port)

    def init(self):
        self.receive = Receive(1, "recvThread", 0, self.skt, self.BUFSIZE)
        self.receive.setDaemon(True) # 设置为守护进程。原本普通的线程，主线程结束也不会结束。守护进程会在主进程结束时结束

    def registerFun(self, id, fun):
        self.receive.register(id, fun)

    def start(self):
        self.receive.start()

    def reset(self, orderId):
        self.orderId = orderId * 100000

    def close(self):
        stop_thread(self.receive)
        del self.receive

    # 创建通信协议
    def createpPotocol(self,dt,i):
        format = '=4bhi%ss' % len(dt)
        data = struct.pack(format, 2,13,14,6,i,len(dt),dt)

        try:
            self.skt.sendto(data, self.send_ip_port)
        except:
            print('发送失败')  

    # 发送客户端连接指令，ip:本机ip地址
    def sendConnect(self, ip):
        format = 'i%ssi' % len(ip)
        data = struct.pack(format, len(bytes(ip,encoding='utf-8')), bytes(ip,encoding='utf-8'), 2)
        self.createpPotocol(data, 13033)
        print('连接服务器...')

    # 发送终端装备加载完成指令，ip:本机ip地址
    def sendLoadComplete(self, ip):
        format = 'i%ss' % len(ip)
        data = struct.pack(format, len(bytes(ip,encoding='utf-8')), bytes(ip,encoding='utf-8'))
        self.createpPotocol(data, 13092)
        print('终端装备加载完成')

    # 发送部署完成指令，ip:本机ip地址
    def sendDeployComplete(self, ip):
        ipLen = len(ip).to_bytes(4,byteorder="little")
        ipBytes = bytes(ip,encoding='utf-8')
        data = ipLen + ipBytes
        self.createpPotocol(data, 13031)
        print('部署完成')

    # 发送重置完成指令，ip:本机ip地址
    def sendResetComplete(self, ip):
        ipLen = len(ip).to_bytes(4,byteorder="little")
        ipBytes = bytes(ip,encoding='utf-8')
        data = ipLen + ipBytes
        self.createpPotocol(data, 13032)
        print('重置完成')

    # 发送移动指令
    # uids:被操作的装备uid的集合，一次指令最多操作9个装备
    # speed:机动速度
    # x:机动位置的x坐标
    # y:机动位置的y坐标，此为三维场景中的高度值，目前不需要处理，默认为0
    # z:机动位置的z坐标
    def sendMove(self, uids, speed, x, z, y = 0):
        if len(uids) > 9:
            print('无法进行此操作，当前操作兵力书为:%d,超过最大值限定' % (len(uids)))
            return

        self.orderId += 1

        data = struct.pack('=i4fi', self.orderId, speed, x, y, z, len(uids))

        for uid in uids:
            data += struct.pack('=Q', uid)

        self.createpPotocol(data, 13071)
        print('orderId:%d, uid:%s, 向(%f,%f)位置进行机动' % (self.orderId, uids, x, z))

    # 发送侦察指令
    # uids:被操作的装备uid的集合，一次指令最多操作9个装备
    # startAngle:开始侦察角度
    # endAngle:结束侦察角度
    def sendScout(self, uids, startAngle, endAngle):
        if len(uids) > 9:
            print('无法进行此操作，当前操作兵力书为:%d,超过最大值限定' % (len(uids)))
            return

        self.orderId += 1

        data = struct.pack('=4i', self.orderId, startAngle, endAngle, len(uids))

        for uid in uids:
            data += struct.pack('=Q', uid)

        self.createpPotocol(data, 13060)
        print('orderId:%d, uid:%s, 向%d°至%d°方向进行侦察' % (self.orderId, uids, startAngle, endAngle))

    # 发送打击指令
    # uids:被操作的装备uid的集合，一次指令最多操作9个装备
    # x:机动位置的x坐标
    # y:机动位置的y坐标，此为三维场景中的高度值，目前不需要处理，默认为0
    # z:机动位置的z坐标
    def sendAttack(self, uids, x, z, y = 0):
        if len(uids) > 9:
            print('无法进行此操作，当前操作兵力书为:%d,超过最大值限定' % (len(uids)))
            return

        self.orderId += 1

        data = struct.pack('=i3fi', self.orderId, x, y, z, len(uids))

        for uid in uids:
            data += struct.pack('=Q', uid)

        self.createpPotocol(data, 13061)
        print('orderId:%d, uid:%s, 向(%f,%f)坐标进行打击' % (self.orderId, uids, x, z))

    # 发送巡航数据
    # uids:被操作的装备uid的集合，一次指令最多操作9个装备
    # speed:机动速度
    # cruisePoints:巡航点坐标集合
    def sendStartCruise(self, uids, speed, cruisePoints):
        self.orderId += 1

        data = struct.pack('=2i', self.orderId, len(uids))

        for uid in uids:
            data += struct.pack('=Q', uid)

        data += struct.pack('=fi', speed, len(cruisePoints))

        for cruisePoint in cruisePoints:
            data += struct.pack('=3f', cruisePoint[0], cruisePoint[1], cruisePoint[2])

        self.createpPotocol(data, 13081)
        print('orderId:%d, 无人机uid:%s, 在%s坐标间巡航' % (self.orderId, uids, cruisePoints))

    # 发送取消巡航
    # uids:被操作的装备uid的集合，一次指令最多操作9个装备
    def sendStopCruise(self, uids):
        self.orderId += 1

        data = struct.pack('=2i', self.orderId, len(uids))

        for uid in uids:
            data += struct.pack('=Q', uid)

        self.createpPotocol(data, 13082)
        print('orderId:%d, 无人机uid:%s, 取消巡航' % (self.orderId, uids))

    # 装载士兵
    # uid:装载装备uid
    # uuids：被装载装备uid的集合
    def sendLoadSoldier(self, uid, uuids):
        self.orderId += 1

        data = struct.pack('=iQi', self.orderId, uid, len(uuids))

        for uuid in uuids:
            data += struct.pack('=Q', uuid)

        self.createpPotocol(data, 13093)
        print('orderId:%d, uid:%s, 对uuid:%s进行装载' % (self.orderId, uid, uuids))

    # 卸载士兵
    # uid:卸载装备uid
    def sendUnloadSoldier(self, uid):
        self.orderId += 1

        data = struct.pack('=iQ', self.orderId, uid)

        self.createpPotocol(data, 13091)
        print('orderId:%d, uid:%s 装备卸载了单兵' % (self.orderId, uid))