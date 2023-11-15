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
sdr.rx_lo = 800000000 # częstotliwość LO odbiornika
sdr.tx_cyclic_buffer = True # sygnał nadajnika jest wysyłany w nieskończonej pętli 
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.gain_control_mode_chan1 = "slow_attack"
sdr.rx_buffer_size = 32768
sdr.tx_buffer_size = 32768

Rx_0_img=[]
Rx_0_real=[]
Rx_0_sum=[]
Rx_1_img=[]
phase_diff_mean=[]
Rx_1_real=[]
Rx_1_sum=[]
phase_0_seria=[]
phase_1_seria=[]
phase_diff=[]

# Odbiór danych
for m in range(225) :
    data = sdr.rx()
    
    if m % 5 == 0:
        Rx_0=data[0]
        Rx_1=data[1]

        for i in range(len(Rx_0)):

            Rx_0_real.append(Rx_0[i].real)
            Rx_0_img.append(Rx_0[i].imag)
            Rx_0_sum.append(Rx_0[i].real+Rx_0[i].imag)
            phase_0=np.rad2deg(np.arctan(Rx_0[i].imag/Rx_0[i].real))
            phase_0_seria.append(phase_0)

            Rx_1_real.append(Rx_1[i].real)
            Rx_1_img.append(Rx_1[i].imag)
            Rx_1_sum.append(Rx_1[i].real+Rx_1[i].imag)
            phase_1=np.rad2deg(np.arctan(Rx_1[i].imag/Rx_1[i].real))
            phase_1_seria.append(phase_1)

            #subst=abs(phase_1_seria-phase_0_seria)
            #min_val=subst[0]
            phase_diff.append(phase_0-phase_1)
 

        print(np.mean(phase_diff))
        phase_diff_mean.append(np.mean(phase_diff))

        time.sleep(1)
        
        plt.plot(Rx_0_sum,label='sum0')
        plt.plot(phase_1_seria, label="1")
        plt.plot(phase_0_seria, label="0")
        plt.plot(Rx_1_sum,label='sum1')
        plt.plot(phase_diff)
        plt.legend(loc='upper left')
        #plt.plot(Rx_0_real)
        #plt.plot(Rx_0_img)
        
        #plt.plot(Rx_1_real)
        #plt.plot(Rx_1_img)
        #plt.grid()
        plt.show()
        
        time.sleep(1)
        Rx_0_img=[]
        Rx_0=[]
        Rx_1=[]
        Rx_0_real=[]
        Rx_0_sum=[]
        Rx_1_img=[]
        Rx_1_real=[]
        Rx_1_sum=[]
        phase_0_seria=[]
        phase_1_seria=[]
        phase_diff=[]
    else:
        data=[]    

moc =-40     # Moc sygnału
fg = 800020000 # Częstotliwość ustawiona na generatorze
plt.legend(loc='upper left')
plt.plot(phase_diff_mean)
plt.title('Metod arctg- fg={}, fs={},\nmoc={}, faza=zmiana o 45 co 1'.format(fg, sdr.sample_rate, moc))
#plt.title('Metod arctg - fg={}, fs={},\nmoc={}'.format(fg, sdr.sample_rate, moc))
plt.xlabel("Iteracja odbioru próbek")
plt.ylabel("Różnica fazy [°]")
plt.grid()
plt.savefig('arctg/pom3.svg', format='svg')
plt.show()

with open('arctg/pom3.txt', 'w') as plik:
    # Zapisz dane do pliku
    for element in phase_diff_mean:
        plik.write(str(element) + '\n')