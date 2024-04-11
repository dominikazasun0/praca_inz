#https://github.com/analogdevicesinc/pyadi-iio/blob/master/examples/ad9361_example.py
# Copyright (C) 2022 Analog Devices, Inc.
#0 22:22 zmiana pasma
# SPDX short identifier: ADIBSD
import adi
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal 
import time
import statistics

def prosta(x1,y1,x0,y0):
    a=(y0-y1)/(x0-x1)
    b=y0-a*x0
    return -b/a

# Konfigurowanie własności transmisji 
sdr = adi.ad9361(uri="ip:192.168.2.1") #Tworzenie radia
sdr.sample_rate = 2000000 # częstotliwość próbkowania
sdr.rx_rf_bandwidth = sdr.sample_rate # szerokość pasma odbiornika
sdr.rx_lo = 1000050000 # częstotliwość LO odbiornika
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.gain_control_mode_chan1 = "slow_attack"
sdr.rx_buffer_size = 32768
sdr.tx_buffer_size = 32768


sdr.rx_enabled_channels = [0,1] # dwa kanały odbiorcze włączone

N=sdr.tx_buffer_size

# Sygnał transmitowany na kanał 0

order=[]
sum_ch0=[]
arctg_ch0=[]

sum_ch1=[]
arctg_ch1=[]
arc_tg_dod=[]

zeros_ch0=[]      # Miejsca zerowe chan0
zeros_ch1=[]      # Miejsca zerowe chan1

wyniki_med=[]

for e in range(250):
    if e%5==0 :
        data = sdr.rx() #Odbiór danych
        
        for i in range(len(data[0])):
            arctg_ch0=np.append(arctg_ch0,np.arctan(data[0][i].imag/data[0][i].real))# Obliczenie arctg(i+q) ch0
            arctg_ch1=np.append(arctg_ch1,np.arctan(data[1][i].imag/data[1][i].real)) # Obliczenie arctg(i+q) ch1

        
        # Wybranie początkowego punktu pomiaru w próbce w której sum_ch0 i sum_ch1 się przecinają
        
        subst=abs(data[0].real-data[1].real)
        min_val=subst[0]
        for a in range(1,1000):
            if (subst[a] < min_val) :
                min_val=subst[a]
                min_index=a
        sum_ch0 = np.array(data[0][min_index:len(sum_ch0)-200].real)
        sum_ch1 = np.array(data[1][min_index:len(sum_ch0)-200].real)
        

        # Metoda próbkowa pomiaru fazy
        prev_0 = sum_ch0[0]
        prev_1 = sum_ch1[0]

        for i  in range(1,len(sum_ch0)): # Detekcja miejsc zerowych sum_ch0
            if sum_ch0[i]<= 0 and prev_0> 0:
                zeros_ch0.append(i)
                if len(zeros_ch0) == 50:
                    break
            prev_0=sum_ch0[i]

        for j  in range(1,len(sum_ch1)): # Detekcja miejsc zerowych sum_ch1
            if sum_ch1[j] <= 0 and prev_1> 0 :
                zeros_ch1.append(j)
                if len(zeros_ch1) == 50:
                    break
            prev_1=sum_ch1[j]   

        for i in range(0,min(len(zeros_ch1),len(zeros_ch0))):
            if zeros_ch0[i]<zeros_ch1[i]:
                order.append(1)
            elif zeros_ch0[i]>zeros_ch1[i]:
                order.append(0)
            elif zeros_ch0[i]==zeros_ch1[i]:
                zero_0=prosta(zeros_ch0[i],sum_ch0[zeros_ch0[i]],zeros_ch0[i]-1,sum_ch0[zeros_ch0[i]-1])
                zero_1=prosta(zeros_ch1[i],sum_ch1[zeros_ch1[i]],zeros_ch1[i]-1,sum_ch1[zeros_ch1[i]-1])
                #print(zero_0,zero_1)
                if zero_0 < zero_1:
                    order.append(1)
                else:
                    order.append(0)
        #print(order)

        

        if statistics.median(order)==0:
            arc_tg_diff=arctg_ch0-arctg_ch1
        else:
            arc_tg_diff=arctg_ch1-arctg_ch0

        
        for i in range(0,len(arc_tg_diff)):
            if arc_tg_diff[i] > 0:
                arc_tg_dod.append(arc_tg_diff[i])
             
        #plt.plot(sum_ch0[:100], 'ro-')
        #plt.plot(sum_ch1[:100], 'bo-')
        #plt.plot(np.rad2deg(arc_tg_diff[:100]),'go-') 
        #plt.grid()
        #plt.show()
        
        print("Numer pomairu", e/5)
        print("mediana",np.rad2deg(statistics.median(arc_tg_dod)))
        print("\n")
        wyniki_med.append(np.rad2deg(statistics.median(arc_tg_dod)))
        
        #plt.plot(arc_tg_diff)   
        #plt.plot(arctg_ch1,  'ro-',label="arctg ch1")
        #plt.plot(arctg_ch0, 'bo-',label="arctg ch0")
        #plt.grid()
        #plt.show()
        
        #plt.xlabel("Próbki [-]")
        #plt.ylabel("Amplituda [-]")
        #plt.title('Metoda arctg')
        #plt.legend(loc='upper left')
        #plt.grid()
        
        #plt.savefig("wukres_{}_{}.svg".format(e*180,l/1000000000))
        #plt.clf()
        sum_ch0=[]
        sum_ch1=[]
        arctg_ch0=[]
        arctg_ch1=[]
        zeros_ch0=[]
        zeros_ch1=[]
        arc_tg_dod=[]
        order=[]
        
        time.sleep(13)

with open('26_03/pomiar{}_fs{}_LO{}GHz_zmiana.txt'.format(50000,sdr.sample_rate,1), 'w') as plik:
# Zapisz dane do pliku
    for element in wyniki_med:
        plik.write(str(element) + '\n')

