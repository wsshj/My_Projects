import numpy as np
import matplotlib.pyplot as plt


theta = np.arange(0.0, np.pi * 2.1, np.pi/100)
r = pow(np.sin(theta/2), 2)+0.2

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(theta, r)
ax.set_rmax(1.2)
ax.set_theta_direction(-1)
ax.set_theta_zero_location("N")
# ax.set_rorigin(-0.1)
ax.set_rticks([0, 0.2, 0.4, 0.6, 0.8, 1, 1.2])  # Less radial ticks
ax.set_rlabel_position(180)  # Move radial labels away from plotted line
ax.grid(True)

ax.set_title("Relationship between threat degree and enemy location", va='bottom')
plt.show()