import socket
import threading
import json
import inspect
import ctypes

# 停止线程（没用）
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

# 停止线程（没用）
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)
    
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
                data = json.loads(self.skt.recvfrom(self.BUFSIZE)[0])
            except:
                print('接收失败')
                continue

            for f in self.funs:
                if data['i'] == f['id']:
                    f['fun'](data['dt'])

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

    def reset(self):
        self.orderId = 0

    def close(self):
        stop_thread(self.receive)
        del self.receive

    # 创建通信协议
    def createpPotocol(self,dt,i):
        data = {}
        data['h'] = 1
        data['s'] = 8
        data['d'] = 14
        data['i'] = i
        data['t'] = 0
        data['dt'] = dt
        data['c'] = 1

        # try:
        #     self.skt.sendto(json.dumps(data).encode('utf-8'), self.send_ip_port)
        # except:
        #     print('发送失败')
        self.skt.sendto(json.dumps(data).encode('utf-8'), self.send_ip_port)

    # 发送客户端连接指令
    def sendConnect(self, ip):
        data = {}
        data['ip'] = ip
        self.createpPotocol(data, 13033)
        print('连接服务器...')

    # 发送终端装备加载完成指令
    def sendLoadComplete(self, ip):
        data = {}
        data['ip'] = ip
        self.createpPotocol(data, 13092)
        print('加载完成')

    # 发送部署完成指令
    def sendDeployComplete(self, ip):
        data = {}
        data['ip'] = ip
        self.createpPotocol(data, 13031)
        print('部署完成')

    # 发送重置完成指令
    def sendResetComplete(self, ip):
        data = {}
        data['ip'] = ip
        self.createpPotocol(data, 13032)
        print('重置完成')

    # 发送移动指令
    def sendMove(self, code,id,camp,speed,range_type,longitude1,latitude1,longitude2 = 0,latitude2 = 0):
        data = {}
        self.orderId += 1
        data['orderId'] = self.orderId
        data['code'] = code
        data['id'] = id
        data['camp'] = camp
        data['speed'] = speed
        data['range_type'] = range_type
        data['longitude1'] = longitude1
        data['latitude1'] = latitude1
        data['longitude2'] = longitude2
        data['latitude2'] = latitude2
        self.createpPotocol(data, 13071)
        print('orderId:%d, code:%s, id:%s, 向(%f,%f)位置进行机动' % (self.orderId, code, id, longitude1, latitude1))

    # 发送侦察指令
    def sendScout(self,code,id,camp,startAngle,endAngle):
        data = {}
        self.orderId += 1
        data['orderId'] = self.orderId
        data['code'] = code
        data['id'] = id
        data['camp'] = camp
        data['startAngle'] = startAngle
        data['endAngle'] = endAngle
        self.createpPotocol(data, 13060)
        print('orderId:%d, code:%s, id:%s, 向%f°至%f°方向进行侦察' % (self.orderId, code, id, startAngle, endAngle))

    # 发送打击指令
    def sendAttack(self,code,id,camp,range_type,longitude1,latitude1,longitude2 = 0,latitude2 = 0):
        data = {}
        self.orderId += 1
        data['orderId'] = self.orderId
        data['code'] = code
        data['id'] = id
        data['camp'] = camp
        data['range_type'] = range_type
        data['longitude1'] = longitude1
        data['latitude1'] = latitude1
        data['longitude2'] = longitude2
        data['latitude2'] = latitude2
        self.createpPotocol(data, 13061)
        print('orderId:%d, code:%s, id:%s, 向(%f,%f)坐标进行打击' % (self.orderId, code, id, longitude1, latitude1))

    # 发送无人机巡航路线

    # 发送删除无人机规划

    # 发送装载单兵

    # 发送卸载全部装备
