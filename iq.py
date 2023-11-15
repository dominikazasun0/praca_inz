import adi
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import time
import math


t = np.arange(0, 1000, 0.2)
x=[]
ampl=[]
phase=[]
i = np.cos(t)
q = np.sin(t)
iq = i + q * 1j

for a in range(len(t)) :
    phase1=math.atan2(q[a],i[a])
    ampl1=pow((i[a]*i[a])+(q[a]*q[a]),0.5)
    x.append(a)
    phase.append(phase1)
    ampl.append(ampl1)
# Sygnał transmitowany na kanał 1
i1 = np.cos(t-np.pi)
q1 = np.sin(t-np.pi)
iq1 = i1 + q1


#plt.plot(iq1,label='iq1')
#plt.plot(i1,label='i1')
#plt.plot(q1,label='q1')
plt.plot(phase,label='p')
plt.plot(ampl,label='a')
print()
#plt.plot(iq,label='iq')
plt.legend(loc='upper left')
plt.grid()
plt.show()