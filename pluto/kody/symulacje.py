import numpy as np
import matplotlib.pyplot as plt

I = 1
Q = 1
f = 1

# Liczba punktów na 1 okres
num_points_per_period = 1000

# Okres sygnału
period = 1 / f

# Liczba punktów całkowitych (maksymalny czas)
num_points_total = int(num_points_per_period * 2*period)

# Tworzenie danych dla sinusoidy
t = np.linspace(0, 2*period, num_points_total)  # Generowanie czasu od 0 do okresu, z określoną liczbą punktów
y = Q * np.sin(2 * np.pi * f * t)  # Sygnał Q
y1 = I * np.cos(2 * np.pi * f * t)  # Sygnał I
i = np.cos(2 * np.pi * f * t)  # Sygnał cosinusowy
q = np.sin(2 * np.pi * f * t)  # Sygnał sinusowy
iq = i + 1j * q  # Sygnał zespolony

i1 = np.cos(2 * np.pi * f * t - (1*np.pi)/4)  # Przesunięcie fazowe I
q1 = np.sin(2 * np.pi * f * t - (1*np.pi)/4)  # Przesunięcie fazowe Q
iq1 = i1 + 1j * q1  # Sygnał zespolony po przesunięciu fazowym

# Plotowanie sygnałów
color=(0,0,1)
plt.plot(iq.real+iq.imag, "r")
plt.plot(iq1.real+iq1.imag, "b")
#plt.plot(iq1.real, "b", label='135 real')
#plt.plot(iq.imag, "k", label='0 imag')
#plt.plot(iq1.imag, "g", label='135 imag')
#plt.plot(np.rad2deg(np.arctan(q / i)), color="lightcoral", label='0')
#plt.plot(np.rad2deg(np.arctan(q1 / i1)), color="lightskyblue", label='135')
plt.plot(np.arctan(q / i) - np.arctan(q1/ i1), "k")
plt.xlabel("$f_{LO}$ [GHz]")
plt.ylabel("Amplituda [rad]")
plt.grid()
plt.legend(loc='upper right')
plt.show()
print(iq1.imag[185])
print(iq1.real[185])
print(iq.real[185])
print(iq.imag[185])

import matplotlib.pyplot as plt


fig, ax1 = plt.subplots()

# Tworzenie pierwszej osi Y po lewej stronie
color = "r"
ax1.set_xlabel('Czas [s]')
ax1.set_ylabel('Amplituda [-]', color="k")
ax1.plot(t, i+q, "r")
#ax1.plot(t, i1+q1, color=color)
ax1.tick_params(axis='y', labelcolor="k")
plt.grid()
# Tworzenie drugiej osi Y po prawej stronie
ax2 = ax1.twinx()  
color = "b"
ax2.set_ylabel('Amplituda [rad]', color="k")
ax2.plot(t, np.arctan(q/ i), color="k")
ax2.tick_params(axis='y', labelcolor="k")


plt.show()
