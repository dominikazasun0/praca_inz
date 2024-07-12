#https://github.com/analogdevicesinc/pyadi-iio/blob/master/examples/ad9361_example.py
# Copyright (C) 2022 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD
import adi
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import statistics
import time
from datetime import datetime

tabela0=[]
tabela0_1=[]
tabela1=[]
tabela1_1=[]
# Przed użyciem kodu należy ustawić jego tryb pracy na podwójny odbiór i podwójne nadawania

sdr = adi.ad9361(uri="ip:192.168.2.1") #Tworzenie radia
wyniki=[]
fc=20000
próbki_na_okres=360
# Konfigurowanie własności transmisji
sdr.rx_rf_bandwidth = 1000000 # szerokość pasma odbiornika
sdr.sample_rate = 360*fc # częstotliwość próbkowania
sdr.rx_lo = 1000000000 # częstotliwość LO odbiornika
sdr.tx_lo = 1000000000 # częstotliwość LO nadajnika
sdr.tx_cyclic_buffer = True # sygnał nadajnika jest wysyłany w nieskończonej pętli 
sdr.tx_hardwaregain_chan0 = -30
sdr.tx_hardwaregain_chan1 = -30
#sdr.gain_control_mode_chan0 = "manual" # turn off AGC
#sdr.gain_control_mode_chan1 = "manual"
#gain = 5# allowable range is 0 to 74.5 dB
#sdr.rx_hardwaregain_chan0 = gain# set receive gain
#sdr.rx_hardwaregain_chan1 = gain
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.gain_control_mode_chan1 = "slow_attack"
sdr.rx_buffer_size = próbki_na_okres*200
sdr.tx_buffer_size = próbki_na_okres*200

# Konfiguracja kanałów nadawczych i odbiorczych
sdr.rx_enabled_channels = [0 ,1] # dwa kanały odbiorcze włączone
sdr.tx_enabled_channels = [0, 1] # dwa kanały nadawcze włączone

# Tworzenie sygnału nadawczego
#fs = int(sdr.sample_rate)
#fc = int(1000000 / (fs / N)) * (fs / N)

N = próbki_na_okres*200 # wielkość bufora danych (ilość próbek sygnału wysyłana podczas jednej transmisji)


#sdr.sample_rate = fc*360 # częstotliwość próbkowania
ts = 1 / float(sdr.sample_rate)
t = np.arange(0, N * ts, ts)

i_1 = np.cos(2 * np.pi * t * fc) * 2 ** 14
q_1 = np.sin(2 * np.pi * t * fc) * 2 ** 14
iq_1 = i_1 + 1j * q_1
sdr.tx([iq_1 ,iq_1])

for e in np.arange(1/180,80/180,1/180):
    data = sdr.rx()
    #plt.plot(data[0])
    #plt.plot(data[1])
    #plt.show()
#Podział odebranych danych na kanał 1 i 0
    subst=abs(data[0].real-data[1].real)
    min_val=subst[0]
    for a in range(1,1000):
        if (subst[a] < min_val) :
            min_val=subst[a]
            min_index=a
    Rx_0 = np.array(data[0][min_index:len(data[0])-200].real)
    Rx_1 = np.array(data[1][min_index:len(data[0])-200].real)

    prev=Rx_0[0]
    prev1=Rx_1[0]
    
    for i in range(0,len(Rx_0)-25):
            if Rx_0[i] <= 0 and prev> 0 :
                okolice_0=Rx_0[i-10:i+10]
                okolice_0_x=list(range(i-10,i+10,1))
                #print(okolice_0_x)
                #difference=len(okolice_0_x)-len(okolice_0)
                #if difference != 0:
                #    if difference % 2 == 0:
                #        okolice_0_x = okolice_0_x[difference//2:len(okolice_0_x)-difference//2]
                #    else:
                #        okolice_0_x = okolice_0_x[difference//2+1:len(okolice_0_x)-difference//2]
                coefficients = np.polyfit(okolice_0_x, okolice_0,1)
                polynomial = np.poly1d(coefficients)
                roots = polynomial.roots
                start_x=[]
                for q in range (0,len(roots)):
                    start_x.append(abs(roots[q]-i))
                tabela0.append(roots[np.argmin(start_x)].real)
            prev=Rx_0[i]

    for j  in range(0,len(Rx_1)-25):
            if Rx_1[j].real <= 0 and prev1.real > 0:
                okolice_0=Rx_1[j-10:j+10]
                okolice_0_x=list(range(j-10,j+10,1))
                difference=len(okolice_0_x)-len(okolice_0)
                #if difference != 0:
                #    if difference % 2 == 0:
                        #okolice_0_x = okolice_0_x[difference//2:len(okolice_0_x)-difference//2]
                #    else:
                #        okolice_0_x = okolice_0_x[difference//2+1:len(okolice_0_x)-difference//2]
                coefficients = np.polyfit(okolice_0_x, okolice_0,1)
                polynomial = np.poly1d(coefficients)
                roots = polynomial.roots
                start_x=[]
                for q in range (0,len(roots)):
                    start_x.append(abs(roots[q]-j))
                tabela1.append(roots[np.argmin(start_x)].real)
            prev1=Rx_1[j]
    
    result = []
    try:
        for i in range(min(len(tabela1), len(tabela0))):
            if tabela0[i] < tabela1[i] :
                result.append((tabela1[i] - tabela0[i]))
            else :
                result.append((tabela0[i] - tabela1[i]))
    except IndexError:
        # Obsługa błędu IndexError
        print("Jedna z list jest pusta lub nie ma elementów.")        
    
    #print(próbki_na_okres)
    try:
        if tabela0[0] < tabela1[0] :
            for i in range(min(len(tabela1), len(tabela0))) :
                result.append((tabela1[i] - tabela0[i]))
        else :
            for j in range(min(len(tabela1), len(tabela0))) :
                result.append((tabela0[j] - tabela1[j]))
    except IndexError:
        # Obsługa błędu IndexError
        print("Jedna z list jest pusta lub nie ma elementów.")               
    
    try:
        wyniki.append(statistics.median(result)*(360/próbki_na_okres))
        print("Różnica w próbkach mediana:" ,statistics.median(result))
        print('Różnica fazy w stopniach:',statistics.median(result)*(360/próbki_na_okres))   
    except statistics.StatisticsError:
        print("Błąd: brak mediany dla pustych danych. Kontynuacja programu bez dodania mediany.")
    #plt.plot(data[0].real)
    #plt.show()
    tabela0=[]
    tabela1=[]
    tabela1_1=[]
    tabela0_1=[]
    Rx_0=[]
    Rx_1=[]
    sdr.tx_destroy_buffer()
    i_1 = np.cos(2 * np.pi * t * fc) * 2 ** 14
    q_1 = np.sin(2 * np.pi * t * fc) * 2 ** 14
    iq_1 = i_1 + 1j * q_1

    i1_1 = np.cos(2 * np.pi * t * fc +(e*np.pi)) * 2 ** 14
    q1_1 = np.sin(2 * np.pi * t * fc+(e*np.pi)) * 2 ** 14
    iq1_1 = i1_1 + 1j * q1_1


    sdr.tx([iq_1 ,iq1_1])
    time.sleep(15)

with open('12_7/pomiar5.txt', 'w') as plik:
# Zapisz dane do pliku
    for element in wyniki:
        plik.write(str(element) + '\n')

wyniki=[]