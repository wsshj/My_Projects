import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
x = np.arange(100.0, 5000, 100)
y = -pow(10,-6) * pow(x-1200, 2) + 10

fig, ax = plt.subplots()
ax.plot(x, y)

#设置坐标轴刻度
my_x_ticks = np.arange(0.0, 3500.0, 500)
plt.xticks(my_x_ticks)
my_y_ticks = np.arange(0.0, 15.0, 1)
plt.yticks(my_y_ticks)
plt.xlim(0,3500)
plt.ylim(0,12)

ax.set(xlabel='distance', ylabel='Threat degree',
       title='Relationship between threat degree and enemy distance')
ax.grid()

plt.show()