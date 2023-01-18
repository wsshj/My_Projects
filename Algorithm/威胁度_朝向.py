import matplotlib.pyplot as plt
import numpy as np

# First create some toy data:
t = np.arange(0.0, np.pi * 2.01, np.pi/100)
x = np.rad2deg(t)
y = pow(np.cos(t/2), 2) + 1

fig=plt.figure('subplot demo')

ax = fig.add_subplot()# plt.subplots()
ax.plot(x, y)

#设置坐标轴刻度
my_x_ticks = np.arange(0.0, 400.0, 45)
plt.xticks(my_x_ticks)

ax.set(xlabel='angle', ylabel='Threat degree',
       title='Threat degree of enemy aiming direction to us')
ax.grid()

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(t, y)
ax.set_rmax(2)
ax.set_theta_direction(-1)
ax.set_theta_zero_location("N")
# ax.set_rorigin(-0.1)
ax.set_rticks([0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2.0])  # Less radial ticks
ax.set_rlabel_position(0)  # Move radial labels away from plotted line
ax.grid(True)

ax.set_title("Threat degree of enemy aiming direction to us", va='bottom')

plt.show()