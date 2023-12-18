#https://github.com/analogdevicesinc/pyadi-iio/blob/master/examples/ad9361_example.py
# Copyright (C) 2022 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD
import adi
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import time
import math

tabela0=[]      # Miejsca zerowe chan0
tabela0_1=[]    # Wartości miejsc zerowych chan0
tabela1=[]      # Miejsca zerowe chan1
tabela1_1=[]    # Wartości miejsc zerowych chan1
result_seria=[] # Zapis wyników pomiaru
result = []
x =[]
ch0=[]
ch1=[]

#Dane do wykresu

przebieg=6   # Liczba okresów sygnału jakie chcemy zobaczyć

# Konfigurowanie własności transmisji
sdr = adi.ad9361(uri="ip:192.168.2.1") #Tworzenie radia

# Konfigurowanie własności transmisji
sdr.rx_rf_bandwidth = 1000000 # szerokość pasma odbiornika
sdr.sample_rate = 10000000 # częstotliwość próbkowania
sdr.rx_lo = 70000000 # częstotliwość LO odbiornika
sdr.tx_lo = 70000000 # częstotliwość LO nadajnika
sdr.tx_cyclic_buffer = True # sygnał nadajnika jest wysyłany w nieskończonej pętli 
sdr.tx_hardwaregain_chan0 = -30
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.tx_hardwaregain_chan1 = -30
sdr.gain_control_mode_chan1 = "slow_attack"
sdr.rx_buffer_size = 32768
sdr.tx_buffer_size = 32768

N = 32768 # wielkość bufora danych (ilość próbek sygnału wysyłana podczas jednej transmisji)
fc = 50000 # częstotliwość transmitowanego sygnału w Hz
ts = 1 / float(sdr.sample_rate)
t = np.arange(0, N * ts, ts)

# Konfiguracja kanałów nadawczych i odbiorczych
sdr.rx_enabled_channels = [0 ,1] # dwa kanały odbiorcze włączone
sdr.tx_enabled_channels = [0, 1] # dwa kanały nadawcze włączone

i = np.cos(2 * np.pi * t * fc) * 2 ** 14
q = np.sin(2 * np.pi * t * fc) * 2 ** 14
iq = i + 1j * q

# Sygnał transmitowany na kanał 1
i1 = np.cos(2 * np.pi * t * fc-np.pi/2) * 2 ** 14
q1 = np.sin(2 * np.pi * t * fc-np.pi/2) * 2 ** 14
iq1 = i1 + 1j * q1

sdr.tx([iq,iq1])
Rx_0_img=np.array([])
Rx_0_real=np.array([])
Rx_0_sum=np.array([])
Rx_1_img=np.array([])
Rx_1_real=np.array([])
Rx_1_sum=np.array([])
phase_0_seria=np.array([])
phase_1_seria=np.array([])
phase_diff=np.array([])

# Odbiór danych
for m in range(20) :
    data = sdr.rx()
    Rx_0=np.array(data[0])
    Rx_1=np.array(data[1])
    for i in range(len(Rx_0)):
        #Rx_0_real=np.append(Rx_0_real,Rx_0[i].real)
        #Rx_0_img=np.append(Rx_0_img,Rx_0[i].imag)
        Rx_0_sum=np.append(Rx_0_sum,Rx_0[i].real+Rx_0[i].imag)
        phase_0=np.rad2deg(np.arctan(Rx_0[i].imag/Rx_0[i].real))
        phase_0_seria=np.append(phase_0_seria,phase_0)

        #Rx_1_real=np.append(Rx_1_real,Rx_1[i].real)
        #Rx_1_img=np.append(Rx_1_img,Rx_1[i].imag)
        Rx_1_sum=np.append(Rx_1_sum,Rx_1[i].real+Rx_1[i].imag)
        phase_1=np.rad2deg(np.arctan(Rx_1[i].imag/Rx_1[i].real))
        phase_1_seria=np.append(phase_1_seria,phase_1)

    subst=abs(Rx_1_sum-Rx_0_sum)
    #print(subst)
    min_val=subst[0]
    for a in range(1,1000):
        if (subst[a] < min_val) :
            min_val=subst[a]
            min_index=a
    Rx_0_1 = np.array(Rx_0_sum[min_index:])
    Rx_1_1 = np.array(Rx_1_sum[min_index:])
    phase_0_seria1=np.array(phase_0_seria[min_index:])
    phase_1_seria1=np.array(phase_1_seria[min_index:]) 
    phase_diff=phase_0_seria1-phase_1_seria1

    #print(np.mean(phase_diff))
    #time.sleep(1)

    plt.plot(Rx_0_1,label="sum0")
    plt.plot(phase_1_seria1, label="1")
    plt.plot(phase_0_seria1, label="0")
    #plt.plot(phase_diff)
    #plt.plot(Rx_0_real)
    #plt.plot(Rx_0_img)
    plt.plot(Rx_1_1,label="sum1")
    #plt.plot(Rx_1_real)
    #plt.plot(Rx_1_img)
    #plt.grid()
    plt.legend(loc='upper left')
    plt.show()
    sdr.tx_destroy_buffer()
    sdr.tx([iq ,iq1])
    time.sleep(1)
    Rx_0_img=np.array([])
    Rx_0_real=np.array([])
    Rx_0_sum=np.array([])
    Rx_1_img=np.array([])
    Rx_1_real=np.array([])
    Rx_1_sum=np.array([])
    phase_0_seria=np.array([])
    phase_1_seria=np.array([])
    phase_diff=np.array([])
