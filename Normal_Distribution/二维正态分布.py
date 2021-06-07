# coding=utf-8

import numpy as np
from numpy.linalg import cholesky
import matplotlib.pyplot as plt

sampleNo = 1000

Sigma_x = 0.68
Sigma_y = 0.71


mu = np.array([[0, 0]])  # μ 值

Sigma = np.array([[Sigma_x, 0], [0, Sigma_y]]) 

# R = cholesky(Sigma) # 还不知道这个是要干啥

# s = np.random.randn(sampleNo, 2) # 标准二维正态分布

s = np.dot(np.random.randn(sampleNo, 2), Sigma) + mu

ax = plt.subplot()
ax.set_title("mu:%s\nSigma:%s" % (np.mean(s, axis=0), np.std(s, axis=0)))

plt.plot(s[:,0],s[:,1],'.')

print("均值：%s" % np.mean(s, axis=0))
print("方差：%s" % np.std(s, axis=0)) 

print(s)
plt.show()
