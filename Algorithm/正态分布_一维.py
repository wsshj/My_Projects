import numpy as np
import matplotlib.pyplot as plt

# example data
mu = 0  # mean of distribution
sigma = 1  # standard deviation of distribution
x = sigma * np.random.randn(1000) + mu

num_bins = 50

fig, ax = plt.subplots()

# the histogram of the data
n, bins, patches = ax.hist(x, num_bins, density=True)

# add a 'best fit' line
y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
     np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
ax.plot(bins, y, '--')

ax.set_title("mu:%s\nSigma:%s" % (np.mean(x, axis=0), np.std(x, axis=0)))  # 在标题栏打印，均值μ，方差σ

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()
