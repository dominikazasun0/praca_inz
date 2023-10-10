import time

import adi
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

sample_rate = 90000000

fs = int(sample_rate)
N = 10240
fc=5000000
#fc = int(1000000 / (fs / N)) * (fs / N)
#print(fc)
ts = 1 / float(fs)
#print(ts)
t = np.arange(0, N * ts, ts)
#t1 = np.arange(N)/sample_rate
print(t)
i = np.cos(2 * np.pi * t * fc-np.pi) * 2 ** 14
q = np.sin(2 * np.pi * t * fc- np.pi) * 2 ** 14
iq = i + 1j * q

i1 = np.cos(2 * np.pi * t * fc) * 2 ** 14
q1 = np.sin(2 * np.pi * t * fc) * 2 ** 14
iq1 = i1 + 1j * q1

plt.plot(iq)
plt.plot(iq1)
plt.show()