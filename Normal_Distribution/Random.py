import numpy as np
from numpy.linalg import cholesky
import matplotlib.pyplot as plt
import json

file_path = "D:\\Project_Files\\My_Projects\\Random_test\\Random_test\\temp.json"

with open(file_path, "r") as f:  # 打开文件
    date = f.read()  # 读取文件

s = np.array(list(json.loads(date)['str']))

ax = plt.subplot()
ax.set_title("mu:%s\nSigma:%s" % (np.mean(s, axis=0), np.std(s, axis=0)))

plt.plot(s[:,0],s[:,1],'.')

print("均值：%s" % np.mean(s, axis=0))
print("方差：%s" % np.std(s, axis=0)) 

plt.show()
