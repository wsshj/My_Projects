import random
import math
import numpy as np
from numpy.linalg import cholesky
from matplotlib.pyplot import MultipleLocator
import matplotlib.pyplot as plt

sampleNo = 10000
mu = 0
Sigma = 1

x = []

for i in range(sampleNo):
    R1 = random.uniform(0, 1)
    R2 = random.uniform(0, 1)

    sx = Sigma * math.cos(2*math.pi*R2) * math.sqrt(-math.log(R1)/0.2274768)
    x.append(sx)

num_bins = 50

fig, ax = plt.subplots()

# the histogram of the data
n, bins, patches = ax.hist(x, num_bins, density=True)

# add a 'best fit' line
y = ((1 / (np.sqrt(2 * np.pi) * Sigma)) *
     np.exp(-0.5 * (1 / Sigma * (bins - mu))**2))
ax.plot(bins, y, '--')
ax.set_title("mu:%s\nSigma:%s" % (np.mean(x, axis=0), np.std(x, axis=0)))

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()