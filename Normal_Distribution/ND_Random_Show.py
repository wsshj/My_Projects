import numpy as np
from numpy.core.fromnumeric import size
from numpy.linalg import cholesky
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import json
import os

file_path = os.path.dirname(__file__) + "\\ND_Random.json"

with open(file_path, "r") as f:  # 打开文件
    date = f.read()  # 读取文件

for key,value in json.loads(date).items():
    s = np.array(list(value))

    ax = plt.subplot(2, 3, int(key))

    plt.gca().set_aspect("equal") # 令X轴和Y轴长度相等

    plt.title("Sigma:%s" % (np.std(s, axis=0))) #添加标题

    x_major_locator=MultipleLocator(0.5) #把x轴的刻度间隔设置为1，并存在变量里
    y_major_locator=MultipleLocator(0.5) #把y轴的刻度间隔设置为10，并存在变量里
    ax.xaxis.set_major_locator(x_major_locator) #把x轴的主刻度设置为1的倍数
    ax.yaxis.set_major_locator(y_major_locator) #把y轴的主刻度设置为10的倍数
    plt.xlim(-2.1,2.1) #把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
    plt.ylim(-2.1,2.1) #把y轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白

    plt.plot(s[:,0],s[:,1],'.') # 画点

    # print("均值：%s" % np.mean(s, axis=0))
    # print("方差：%s" % np.std(s, axis=0)) 

plt.show()
