import math
import numpy as np
from seasonal import fit_seasons, adjust_seasons
import matplotlib.pyplot as plt

# make a trended sine wave
s = [10 * math.sin(i * 2 * math.pi / 25) + i * i /100.0 for i in range(100)]

# detrend and deseasonalize
seasons, trend = fit_seasons(s)
adjusted = adjust_seasons(s, seasons=seasons)
residual = adjusted - trend

# visualize results
plt.figure()
plt.plot(s, label='data')
plt.plot(trend, label='trend')
plt.plot(seasons, label='seasons')
plt.plot(residual, label='residual')
plt.legend(loc='upper left')
plt.show()

# how about with some noise?
noisy = s + np.random.normal(0, 5, len(s))
seasons, trend = fit_seasons(noisy)
adjusted = adjust_seasons(noisy, seasons=seasons)
residual = adjusted - trend

plt.figure()
plt.plot(noisy, label='noisy')
plt.plot(noisy - residual, label='trend+season')
plt.plot(trend, label='trend')
plt.plot(seasons, label='seasons')
plt.plot(residual, label='residual')
plt.legend(loc='upper left')
plt.show()
