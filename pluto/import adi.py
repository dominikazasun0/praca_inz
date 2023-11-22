import adi
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import time
import math

phase=3/5
srednia=[]
t = np.arange(0, 25,0.1)
zmienna=0
zmienna_1=0
dominika=[]

# Sygnał transmitowany na kanał 0
i = np.cos(t) * 75
q = np.sin(t) * 75
iq = i + 1j * q

# Sygnał transmitowany na kanał 1
i1 = np.cos(t-np.pi*(phase)) * 75
q1 = np.sin(t-np.pi*(phase)) * 75
iq1 = i1 + 1j * q1

iq1_1=iq1.real+iq1.imag
iq_1=iq.real+iq.imag

phase_0=(np.arctan(iq.imag/iq.real))*(180/np.pi)
phase_1=(np.arctan(iq1.imag/iq1.real))*(180/np.pi)
diff=phase_0-phase_1

for i in range(len(phase_0)):
    if phase_0[i]>phase_1[i]:
        dominika.append(phase_0[i]-phase_1[i])
    else:
        dominika.append(phase_1[i]-phase_0[i])
subst=abs(iq1_1-iq_1)
min_index= None
min_val=subst[0]
for a in range(1,200):
    if (subst[a] < min_val) :
        min_val=subst[a]
        min_index=a
if min_index is None:
    min_index=0  
Rx_0 = np.array(iq_1[min_index:])
Rx_1 = np.array(iq1_1[min_index:])

prev_0 = Rx_0[0]
prev_1 = Rx_1[0]



for i in range(1,len(Rx_0)-1):
    if Rx_0[i] <= 0 and prev_0 > 0 :
        zmienna=i
        break
    prev_0=Rx_0[i]

for j in range(1,len(Rx_1)-1):
    if Rx_1[j] <= 0 and prev_1 > 0 :
        zmienna_1=j
        break
    prev_1=Rx_0[j]


if zmienna<zmienna_1:
    for l in range(len(diff)):
        if diff[l] > 0:
            srednia.append(diff[l])
else:
    for l in range(len(diff)):
        if diff[l] < 0:
            srednia.append(diff[l])


plt.title('faza={}pi wynik={}'.format(phase, np.mean(srednia)))
plt.plot(dominika)
#plt.plot(diff[min_index:])
plt.plot(Rx_0)
plt.plot(Rx_1)
plt.grid()
#plt.plot(phase_1)
#plt.savefig('symulacje_arctg/sym9_1.svg', format='svg')
plt.show()