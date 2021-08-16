import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
t = np.arange(0.0, np.pi * 2.1, np.pi/100)
x = np.rad2deg(t)
y = pow(np.sin(t/2), 2)+0.2

fig, ax = plt.subplots()
ax.plot(x, y)

#设置坐标轴刻度
my_x_ticks = np.arange(0.0, 400.0, 45)
plt.xticks(my_x_ticks)

ax.set(xlabel='angle', ylabel='Threat degree',
       title='Relationship between threat degree and enemy location')
ax.grid()

plt.show()