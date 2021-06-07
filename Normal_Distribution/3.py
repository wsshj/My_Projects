import random
import math
import numpy as np
from numpy.linalg import cholesky
from matplotlib.pyplot import MultipleLocator
import matplotlib.pyplot as plt

sampleNo = 1000
mu = 0
Sigma_x = 0.22
Sigma_y = 0.23

s1 = []
s2 = []

for i in range(sampleNo):
     R1 = random.uniform(0, 1)
     R2 = random.uniform(0, 1)

     x = Sigma_x * math.cos(2*math.pi*R2) * math.sqrt(-math.log(R1)/0.2274768)
     y = Sigma_y * math.sin(2*math.pi*R2) * math.sqrt(-math.log(R1)/0.2274768)
     s1.append(x)
     s2.append(y)

plt.plot(s1,s2,'.')

x_major_locator=MultipleLocator(0.1)
#把x轴的刻度间隔设置为1，并存在变量里
y_major_locator=MultipleLocator(0.1)
#把y轴的刻度间隔设置为10，并存在变量里
ax=plt.gca()
#ax为两条坐标轴的实例
ax.xaxis.set_major_locator(x_major_locator)
#把x轴的主刻度设置为1的倍数
ax.yaxis.set_major_locator(y_major_locator)
#把y轴的主刻度设置为10的倍数
plt.xlim(-1,1)
#把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
plt.ylim(-1,1)

plt.show()