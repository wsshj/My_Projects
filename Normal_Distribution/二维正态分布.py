# coding=utf-8

import numpy as np
from numpy.linalg import cholesky
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

np.random.seed(19680801) # 设置随机数种子

sampleNo = 1000

mu = np.array([[0, 0]])  # μ 值

Sigma_x = 1
Sigma_y = 1

Sigma = np.array([[Sigma_x, 0], [0, Sigma_y]]) 

# R = cholesky(Sigma) # 还不知道这个是要干啥

# 生成 X 和 Y 具备关联性的二维正态分布随机数
s = np.dot(np.random.randn(sampleNo, 2), Sigma) + mu  # 二维正态分布

ax = plt.subplot(1, 2, 1)  #要生成一行两列，这是第一个图plt.subplot('行','列','编号')
ax.set_title("Relevant\nmu:%s\nSigma:%s" % (np.mean(s, axis=0), np.std(s, axis=0))) # 在标题栏打印，均值μ，方差σ

x_major_locator=MultipleLocator(0.5) #把x轴的刻度间隔设置为1，并存在变量里
y_major_locator=MultipleLocator(0.5) #把y轴的刻度间隔设置为10，并存在变量里
ax.xaxis.set_major_locator(x_major_locator) #把x轴的主刻度设置为1的倍数
ax.yaxis.set_major_locator(y_major_locator) #把y轴的主刻度设置为10的倍数
plt.xlim(-4.1,4.1) #把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
plt.ylim(-4.1,4.1) #把y轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白

plt.plot(s[:,0],s[:,1],'.')

mu = 0

# 生成 X 和 Y 不具备关联性的二维正态分布随机数
x = Sigma_x * np.random.randn(1000) + mu
y = Sigma_y * np.random.randn(1000) + mu

ax = plt.subplot(1, 2, 2)  #要生成一行两列，这是第二个图plt.subplot('行','列','编号')
ax.set_title("Not relevant\nmu:[%.8f,%.8f]\nSigma:[%.8f,%.8f]" % (np.mean(x, axis=0), np.mean(y, axis=0), np.std(x, axis=0),  np.std(y, axis=0))) # 在标题栏打印，均值μ，方差σ

x_major_locator=MultipleLocator(0.5) #把x轴的刻度间隔设置为1，并存在变量里
y_major_locator=MultipleLocator(0.5) #把y轴的刻度间隔设置为10，并存在变量里
ax.xaxis.set_major_locator(x_major_locator) #把x轴的主刻度设置为1的倍数
ax.yaxis.set_major_locator(y_major_locator) #把y轴的主刻度设置为10的倍数
plt.xlim(-4.1,4.1) #把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
plt.ylim(-4.1,4.1) #把y轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白

plt.plot(x, y, '.')

plt.show()
