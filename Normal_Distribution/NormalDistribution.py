import random
import math
import numpy as np
from numpy.linalg import cholesky
from matplotlib.pyplot import MultipleLocator, xcorr
import matplotlib.pyplot as plt

a = []

for i in range(100000):
     b = random.random()
     if b in a:
          print("找到相同啦：%s" % b)
     
     a.append(b)



# print("a的值有：%s" % a)