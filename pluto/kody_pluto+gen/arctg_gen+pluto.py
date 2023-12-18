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

# Konfigurowanie własności transmisji
sdr = adi.ad9361(uri="ip:192.168.2.1") #Tworzenie radia
f=10000
# Konfigurowanie własności transmisji
sdr.rx_rf_bandwidth = 1000000 # szerokość pasma odbiornika
sdr.sample_rate = 10000000 # częstotliwość próbkowania
sdr.rx_lo = 475000000 # częstotliwość LO odbiornika 
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.gain_control_mode_chan1 = "slow_attack"
sdr.rx_buffer_size = 32768


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
srednia=[]


# Odbiór danych
for m in range(360) :
    data = sdr.rx()
    
    if m % 8 == 0:
        Rx_0=data[0]
        Rx_1=data[1]

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

        diff=phase_0_seria-phase_1_seria
        subst=abs(Rx_1_sum-Rx_0_sum)
        min_index= None
        min_val=subst[0]
        for a in range(1,200):
            if (subst[a] < min_val) :
                min_val=subst[a]
                min_index=a
        if min_index is None:
            min_index=0  
        Rx_0 = np.array(Rx_0_sum[min_index:])
        Rx_1 = np.array(Rx_1_sum[min_index:])
        #print(Rx_1)

        prev_0 = Rx_0[0]
        prev_1 = Rx_1[0]


        for i in range(1,len(Rx_0)-1):
            if Rx_0[i] <= 0 and prev_0 > 0 :
                zmienna=i
                #print(Rx_0[i])
                #print(prev_0)
                break
            prev_0=Rx_0[i]

        for j in range(1,len(Rx_1)-1):
            if Rx_1[j] <= 0 and prev_1 > 0:
                zmienna_1=j
                #print(Rx_1[j])
                #print(prev_1)
                break
            prev_1=Rx_1[j]

            


        #print("chan0", zmienna)
        #print("chan1", zmienna_1)
        #print("/n")
        if zmienna<zmienna_1:
            for l in range(len(diff)):
                if diff[l] > 0:
                    phase_diff.append(diff[l])
        else:
            for l in range(len(diff)):
                if diff[l] < 0:
                    phase_diff.append(abs(diff[l]))            
        print(np.mean(phase_diff))
        srednia.append(np.mean(phase_diff))
        '''
        plt.plot(Rx_1, 'r',label="chan1")
        plt.plot(Rx_0, 'k', label="chan0")
        plt.plot(phase_1_seria, label="arctg ch1")
        plt.plot(phase_0_seria, label="arctg ch0")
        plt.plot(diff, label="arctg ch0 - arctg ch1")
        #plt.title('Metod arctg- fg={}, fs={},\nmoc={}'.format(fg, sdr.sample_rate, moc))
        plt.legend(loc='upper left')
        plt.grid()
        plt.show()
        
        time.sleep(0.1)
        '''
        Rx_0_sum=[]
        Rx_1_sum=[]
        Rx_0_img=[]
        Rx_1_img=[]
        Rx_0_real=[]
        Rx_1_real=[]
        Rx_0=[]
        Rx_1=[]

        diff=[]

        phase_0_seria=[]
        phase_1_seria=[]
        phase_diff=[]
    else:
        data=[]    

moc =-40     # Moc sygnału
fg = sdr.rx_lo+f # Częstotliwość ustawiona na generatorze
plt.legend(loc='upper left')
plt.plot(srednia)
plt.title('Metod arctg - fg={}, fs={},\nmoc={} LO={} faza=zamiana do 0 do 45 co 1°'.format(fg, sdr.sample_rate, moc,sdr.rx_lo))
plt.xlabel("Iteracja odbioru próbek")
plt.ylabel("Różnica fazy [°]")
plt.grid()
plt.savefig('arctg_pomiary/pom{}_zmiana_1.svg'.format(fg), format='svg')
plt.show()

with open('arctg_pomiary/pom{}_zmiana_1.txt'.format(fg), 'w') as plik:
     #Zapisz dane do pliku
    for element in srednia:
        plik.write(str(element) + '\n')