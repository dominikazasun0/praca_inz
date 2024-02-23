#https://github.com/analogdevicesinc/pyadi-iio/blob/master/examples/ad9361_example.py
# Copyright (C) 2022 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD
import adi
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal 
import time
import statistics

# Konfigurowanie własności transmisji
sdr = adi.ad9361(uri="ip:192.168.2.1") #Tworzenie radia
sdr.rx_rf_bandwidth = 1000000 # szerokość pasma odbiornika
sdr.sample_rate = 10000000 # częstotliwość próbkowania
sdr.rx_lo = 500000000 # częstotliwość LO odbiornika
sdr.tx_lo = 500000000 # częstotliwość LO nadajnika
sdr.tx_cyclic_buffer = True # sygnał nadajnika jest wysyłany w nieskończonej pętli 
sdr.tx_hardwaregain_chan0 = -30
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.tx_hardwaregain_chan1 = -30
sdr.gain_control_mode_chan1 = "slow_attack"
sdr.rx_buffer_size = 32768
sdr.tx_buffer_size = 32768

sdr.rx_enabled_channels = [0 ,1] # dwa kanały odbiorcze włączone
sdr.tx_enabled_channels = [0, 1] # dwa kanały nadawcze włączone

N = 32768 # wielkość bufora danych (ilość próbek sygnału wysyłana podczas jednej transmisji)
#fc = 10000 # częstotliwość transmitowanego sygnału w Hz
ts = 1 / float(sdr.sample_rate)
t = np.arange(0, N * ts, ts)

# Sygnał transmitowany na kanał 0

order=[]
sum_ch0=[]
arctg_ch0=[]

sum_ch1=[]
arctg_ch1=[]
arc_tg_dod=[]

zeros_ch0=[]      # Miejsca zerowe chan0
zeros_ch1=[]      # Miejsca zerowe chan1

#Dane do wykresu
# Wysyłanie danych
fc=100000

# Odbiór danych

for e in np.arange(1/180,50/180,1/180):
    data = sdr.rx() #Odbiór danych
    
    for i in range(len(data[0])):
        arctg_ch0=np.append(arctg_ch0,np.rad2deg(np.arctan(data[0][i].imag/data[0][i].real))) # Obliczenie arctg(i+q) ch0
        arctg_ch1=np.append(arctg_ch1,np.rad2deg(np.arctan(data[1][i].imag/data[1][i].real))) # Obliczenie arctg(i+q) ch1

    
    # Wybranie początkowego punktu pomiaru w próbce w której sum_ch0 i sum_ch1 się przecinają
    
    subst=abs(data[0].real-data[1].real)
    min_val=subst[0]
    for a in range(1,1000):
        if (subst[a] < min_val) :
            min_val=subst[a]
            min_index=a
    sum_ch0 = np.array(data[0][min_index:len(sum_ch0)-200])
    sum_ch1 = np.array(data[1][min_index:len(sum_ch0)-200])
    
    # Metoda próbkowa pomiaru fazy
    prev_0 = sum_ch0[0]
    prev_1 = sum_ch1[0]

    for i  in range(1,len(sum_ch0)): # Detekcja miejsc zerowych sum_ch0
        if sum_ch0[i].real <= 0 and prev_0.real > 0:
            zeros_ch0.append(i)
            if len(zeros_ch0) == 50:
                break
        prev_0=sum_ch0[i]

    for j  in range(1,len(sum_ch1)): # Detekcja miejsc zerowych sum_ch1
        if sum_ch1[j].real <= 0 and prev_1.real > 0 :
            zeros_ch1.append(j)
            if len(zeros_ch1) == 50:
                break
        prev_1=sum_ch1[j]   

    for i in range(0,min(len(zeros_ch1),len(zeros_ch0))):
        if zeros_ch0[i]<zeros_ch1[i]:
            order.append(1)
        else:
            order.append(0)
    #print(order)
    
    if statistics.median(order)==1:
        arc_tg_diff=arctg_ch0-arctg_ch1
    else:
        arc_tg_diff=arctg_ch1-arctg_ch0
    
    for i in range(0,len(arc_tg_diff)):
        if arc_tg_diff[i] > 0:
            arc_tg_dod.append(arc_tg_diff[i])
    print(statistics.median(arc_tg_dod))
   
    
    

    #plt.plot(arc_tg_diff)    
    #plt.plot(arctg_ch1, label="arctg ch1")
    #plt.plot(arctg_ch0, label="arctg ch0")
    #plt.plot(sum_ch0, 'r-')
    #plt.plot(sum_ch1, 'b-')
    #plt.plot(arctg_diff, label="arctg ch0 - arctg ch1")
    #plt.xlabel("Próbki [-]")
    #plt.ylabel("Amplituda [-]")
    #plt.title('Metoda arctg')
    #plt.legend(loc='upper left')
    #plt.grid()
    #plt.show()

    

    sum_ch0=[]
    sum_ch1=[]
    arctg_ch0=[]
    arctg_ch1=[]
    zeros_ch0=[]
    zeros_ch1=[]
    arc_tg_dod=[]
    order=[]
    sdr.tx_destroy_buffer()

    i = np.cos(2 * np.pi * t * fc) * 2 ** 14
    q = np.sin(2 * np.pi * t * fc) * 2 ** 14
    iq = i + 1j * q

    i1 = np.cos(2 * np.pi * t * fc +(e*np.pi)) * 2 ** 14
    q1 = np.sin(2 * np.pi * t * fc + (e*np.pi)) * 2 ** 14
    iq1 = i1 + 1j * q1


    sdr.tx([iq ,iq1])
    time.sleep(2)
