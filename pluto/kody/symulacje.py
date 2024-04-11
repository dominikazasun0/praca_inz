import numpy as np
import matplotlib.pyplot as plt
I=100
Q=100
f=50
# Tworzenie danych dla sinusoidy
t = np.linspace(0.0095, 0.05, 1000)  # 100 punktów równomiernie rozłożonych od 0 do 2*pi
y = Q*np.sin(2*np.pi*f*t+np.pi/4)  # sinus dla każdego punktu x
y1= I*np.cos(2*np.pi*f*t+np.pi/4)

y4 = Q*np.sin(2*np.pi*f*t)  # sinus dla każdego punktu x
y5= I*np.cos(2*np.pi*f*t)

y3=np.arctan(y/y1)
y2=((I**2+Q**2)**0.5)*np.cos(t+y3)

"""
subst=abs(y-y1)
min_val=subst[0]
for a in range(1,1000):
    if (subst[a] < min_val) :
        min_val=subst[a]
        min_index=a
Rx_0 = np.array(y[min_index:len(y)])
Rx_1 = np.array(y1[min_index:len(y)])
""" 
# Tworzenie wykresu
#plt.plot(y5)
#plt.plot(y1)
plt.plot(y4+y5,'b',label="0")
plt.plot(y+y1,'r', label="pi/4")
plt.plot(np.rad2deg(np.arctan(y4/y5)),label="0")
plt.plot(np.rad2deg(np.arctan(y/y1)),label="pi/4")
plt.plot(np.rad2deg(np.arctan(y/y1)-np.arctan(y4/y5)),label="pi/4-0")
plt.title('Przykładowy przebieg z nieprawidłowo\nwybranym punktem początkowym')
plt.xlabel('Czas [s]')
plt.ylabel('Amplituda [n]')
plt.legend(loc='upper left')
plt.grid(True)
plt.show()
"""
plt.plot(t[min_index:],Rx_0,'b')
plt.plot(t[min_index:],Rx_1,'r')
plt.title('Przykładowy przebieg z nieprawidłowo\nwybranym punktem początkowym')
plt.xlabel('Czas [s]')
plt.ylabel('Amplituda [n]')
plt.grid(True)
plt.show()
"""