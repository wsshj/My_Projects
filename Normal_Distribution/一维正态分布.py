import numpy as np
import matplotlib.pyplot as plt

# example data
mu = 0  # mean of distribution
sigma = 0.71  # standard deviation of distribution
x = mu + sigma * np.random.randn(1000)

num_bins = 50

fig, ax = plt.subplots()

# the histogram of the data
n, bins, patches = ax.hist(x, num_bins, density=True)

# add a 'best fit' line
y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
     np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
ax.plot(bins, y, '--')

ax.set_title("mu:%s\nSigma:%s" % (np.mean(x, axis=0), np.std(x, axis=0)))

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()

# np.random.seed(19680801)

# # example data
# mu = 0  # mean of distribution
# sigma_x = 0.68  # standard deviation of distribution
# sigma_y = 0.71 
# x = mu + sigma_x * np.random.randn(1000)
# y = mu + sigma_y * np.random.randn(1000)

# plt.subplot()
# # 注意绘制的是散点图，而不是直方图
# plt.plot(x,y,'.')

# print(np.mean(x, axis=0))
# print(np.std(x, axis=0))
# print(np.mean(y, axis=0))
# print(np.std(y, axis=0))

# plt.show()