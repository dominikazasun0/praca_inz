#https://github.com/analogdevicesinc/pyadi-iio/blob/master/examples/ad9361_example.py
# Copyright (C) 2022 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD
import adi
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

tabela0=[]
tabela0_1=[]
tabela1=[]
tabela1_1=[]
# Przed użyciem kodu należy ustawić jego tryb pracy na podwójny odbiór i podwójne nadawania

sdr = adi.ad9361(uri="ip:192.168.2.1") #Tworzenie radia

# Konfigurowanie własności transmisji
sdr.rx_rf_bandwidth = 1000000 # szerokość pasma odbiornika
sdr.sample_rate = 1000000 # częstotliwość próbkowania
sdr.rx_lo = 70000000 # częstotliwość LO odbiornika
sdr.tx_lo = 70000000 # częstotliwość LO nadajnika
sdr.tx_cyclic_buffer = True # sygnał nadajnika jest wysyłany w nieskończonej pętli 
sdr.tx_hardwaregain_chan0 = -30
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.tx_hardwaregain_chan1 = -30
sdr.gain_control_mode_chan1 = "slow_attack"
sdr.rx_buffer_size = 32768
sdr.tx_buffer_size = 32768

# Konfiguracja kanałów nadawczych i odbiorczych
sdr.rx_enabled_channels = [0 ,1] # dwa kanały odbiorcze włączone
sdr.tx_enabled_channels = [0, 1] # dwa kanały nadawcze włączone

# Tworzenie sygnału nadawczego
#fs = int(sdr.sample_rate)
#fc = int(1000000 / (fs / N)) * (fs / N)

N = 32768 # wielkość bufora danych (ilość próbek sygnału wysyłana podczas jednej transmisji)
fc = 10000 # częstotliwość transmitowanego sygnału w Hz
ts = 1 / float(sdr.sample_rate)
t = np.arange(0, N * ts, ts)

# Sygnał transmitowany na kanał 0
i = np.cos(2 * np.pi * t * fc) * 2 ** 14
q = np.sin(2 * np.pi * t * fc) * 2 ** 14
iq = i + 1j * q

# Sygnał transmitowany na kanał 1            
i1 = np.cos(2 * np.pi * t * fc -np.pi/2) * 2 ** 14
q1 = np.sin(2 * np.pi * t * fc -np.pi/2) * 2 ** 14
iq1 = i1 + 1j * q1

'''
plt.plot(iq1)
plt.plot(iq)
plt.show()
'''

# Wysyłanie danych
sdr.tx([iq ,iq1])

# Odbiór danych 20 razy (20 x N próbek)
for r in range(20):
    data = sdr.rx()

#Podział odebranych danych na kanał 1 i 0
    próbki_na_okres=(1/fc)/(1/sdr.sample_rate)
    Rx_0=data[0]
    Rx_1=data[1] 
#plt.plot(Rx_0)
#plt.plot(Rx_1[2*int(próbki_na_okres):])
#plt.show()
#plt.plot(Rx_0[10000:])
#print(Rx_0
#plt.show()
#print(Rx_1)
#for i in range (2*int(próbki_na_okres), len(Rx_0)-2*)

    prev=Rx_0[0]
    prev1=Rx_1[0]

    for i  in range(0,len(Rx_0)):
        if Rx_0[i].real <= 0 and prev.real > 0 :
            tabela0.append(i)
            tabela0_1.append(Rx_0[i].real)
        #print("było 0")
        prev=Rx_0[i]

    for j  in range(0,len(Rx_1)):
        if Rx_1[j].real <= 0 and prev1.real > 0 :
            tabela1.append(j)
            tabela1_1.append(Rx_1[j].real)
        #print("było 0")
        prev1=Rx_1[j]


    próbki_na_okres=(1/fc)/(1/sdr.sample_rate)

    x = range(tabela0[0], tabela0[0] + 6 * int(próbki_na_okres))
    plt.plot(x, Rx_0[tabela0[0]:tabela0[0] + int(6 * próbki_na_okres)])
    plt.scatter(tabela0[0:7], tabela0_1[0:7], color='red', label='Zero Crossing', marker='o')



    x = range(tabela1[0], tabela1[0] + 6 * int(próbki_na_okres))
    plt.plot(x, Rx_1[tabela1[0]:tabela1[0] + int(6 * próbki_na_okres)])
    plt.scatter(tabela1[0:7], tabela1_1[0:7], color='black', label='Zero Crossing', marker='o')
    plt.grid()
    plt.show()
    print(tabela0[0:7])
    print(tabela1[0:7])

    result = []
    for i in range(20):
        result.append((tabela1[i] - tabela0[i])/próbki_na_okres)
    print(np.mean(result))
'''
with open('chanel0.txt', 'w') as plik:
    # Zapisz dane do pliku
    for element in Rx_0:
        plik.write(str(element) + '\n')

with open('chanel1.txt', 'w') as plik:
    # Zapisz dane do pliku
    for element in Rx_1:
        plik.write(str(element) + '\n')        
'''