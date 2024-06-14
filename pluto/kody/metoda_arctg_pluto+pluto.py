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
sdr = adi.ad9361(uri="ip:192.168.2.1") # tworzenie radia
sdr.sample_rate = 6000000 # częstotliwość próbkowania
sdr.rx_rf_bandwidth = sdr.sample_rate # szerokość pasma odbiornika
sdr.tx_rf_bandwidth = sdr.sample_rate # szerokość pasma odbiornika
sdr.tx_lo = 1500000000 # częstotliwość LO nadajnika
sdr.rx_lo = 1500000000 # częstotliwość LO odbiornika
sdr.tx_cyclic_buffer = True # sygnał nadajnika jest wysyłany w nieskończonej pętli 
sdr.tx_hardwaregain_chan0 = -30 # wzmocnienie w kanale nadawczym 0
sdr.gain_control_mode_chan0 = "slow_attack" # tryb pracy przetworników ADC kanał 0
sdr.tx_hardwaregain_chan1 = -30 # wzmocnienie w kanale nadawczym 1
sdr.gain_control_mode_chan1 = "slow_attack" # tryb pracy przetworników ADC kanał 1
sdr.rx_buffer_size = 32768
sdr.tx_buffer_size = 32768
N=sdr.tx_buffer_size
sdr.rx_enabled_channels = [0 ,1] # dwa kanały odbiorcze włączone
sdr.tx_enabled_channels = [0, 1] # dwa kanały nadawcze włączone


order=[]
ch0=[]
arctg_ch0=[]
ch1=[]
arctg_ch1=[]
arc_tg_dod=[]
zeros_ch0=[]      
zeros_ch1=[]     
wyniki_med=[]

# Tworzenie 
ts = 1 / float(sdr.sample_rate)
t = np.arange(0, N * ts, ts)
fc=80000 #częstotliwość sygnału modulującego

# kilka pierwszych iteracji nie będzie działać, bo nie jest nadawany sygnał od początku

for e in np.arange(1/180,250/180,1/180):
    data = sdr.rx() #Odbiór danych
    
    for i in range(len(data[0])):
        arctg_ch0=np.append(arctg_ch0,np.arctan(data[0][i].imag/data[0][i].real))# Obliczenie arctg(i+q) ch0
        arctg_ch1=np.append(arctg_ch1,np.arctan(data[1][i].imag/data[1][i].real)) # Obliczenie arctg(i+q) ch1

    
    # Wybranie początkowego punktu pomiaru w próbce w której ch0 i ch1 się przecinają
    
    subst=abs(data[0].real-data[1].real)
    min_val=subst[0]
    for a in range(1,1000):
        if (subst[a] < min_val) :
            min_val=subst[a]
            min_index=a
    ch0 = np.array(data[0][min_index:len(ch0)-200].real)
    ch1 = np.array(data[1][min_index:len(ch0)-200].real)
    
    prev_0 = ch0[0]
    prev_1 = ch1[0]

    for i  in range(1,len(ch0)): # Detekcja miejsc zerowych ch0
        if ch0[i]<= 0 and prev_0> 0:
            zeros_ch0.append(i)
            if len(zeros_ch0) == 50:
                break
        prev_0=ch0[i]

    for j  in range(1,len(ch1)): # Detekcja miejsc zerowych ch1
        if ch1[j] <= 0 and prev_1> 0 :
            zeros_ch1.append(j)
            if len(zeros_ch1) == 50:
                break
        prev_1=ch1[j]   

    for i in range(0,min(len(zeros_ch1),len(zeros_ch0))): # Tworzenie sygnału zero-jedynkowego określającego kolejność sygnałów
        if zeros_ch0[i]<zeros_ch1[i]: #Jeżeli 1 wyprzedza w fazie to jest 1
            order.append(1)
        elif zeros_ch0[i]>zeros_ch1[i]: #Jeżeli 0 wyprzedza w fazie to jest 0
            order.append(0)
        elif zeros_ch0[i]==zeros_ch1[i]: # Gdy numery próbek w których zarejstrowano miejsce zerowe są takie same
            #to jest prowadzona przez próbki prosta i jako miejsce zerowe jest przyjmowane miejsce zerowe obliczonej prostej
            zero_0=prosta(zeros_ch0[i],ch0[zeros_ch0[i]],zeros_ch0[i]-1,ch0[zeros_ch0[i]-1])
            zero_1=prosta(zeros_ch1[i],ch1[zeros_ch1[i]],zeros_ch1[i]-1,ch1[zeros_ch1[i]-1])
            #print(zero_0,zero_1)
            if zero_0 < zero_1:
                order.append(1)
            else:
                order.append(0)

    if statistics.median(order)>0.5: # określenie który z sygnałów jest wyprzedzający w fazie, tworzenie sygnału prostokątnego
        #z zachowaniem odpowiednej kolejności działania na bazie sygnału zero-jedynkowego
        arc_tg_diff=arctg_ch0-arctg_ch1 #sygnał z kanału 1 wyprzedza
    else:
        arc_tg_diff=arctg_ch1-arctg_ch0 #sygnał z kanału 0 wyprzedza
    
    
    for i in range(0,len(arc_tg_diff)): #oddzielenie części dodatniej sygnału prostokątnego
        if arc_tg_diff[i] > 0:
            arc_tg_dod.append(arc_tg_diff[i])
            
    
    print("srednia",np.rad2deg(np.mean(arc_tg_dod)))
    print("mediana",np.rad2deg(statistics.median(arc_tg_dod))) #zamiana na stopnie i obliczenie mediany
    print("\n")
    print(np.rad2deg(statistics.median(arc_tg_dod)))
    wyniki_med.append(np.rad2deg(statistics.median(arc_tg_dod))) # tworzenie listy do zapisu do pliku
    
    ch0=[]
    ch1=[]
    arctg_ch0=[]
    arctg_ch1=[]
    zeros_ch0=[]
    zeros_ch1=[]
    arc_tg_dod=[]
    order=[]
    sdr.tx_destroy_buffer() # Wyczyszczenie bufora

    # Tworzenie danych do transmisji
    i = np.cos(2 * np.pi * t * fc) * 2 ** 14
    q = np.sin(2 * np.pi * t * fc) * 2 ** 14
    iq = i + 1j * q

    i1 = np.cos(2 * np.pi * t * fc + (e*np.pi)) * 2 ** 14
    q1 = np.sin(2 * np.pi * t * fc + (e*np.pi)) * 2 ** 14
    iq1 = i1 + 1j * q1

    # Wysłanie danych
    sdr.tx([iq ,iq1])
    time.sleep(13)
    
    #with open('pomiary_21_02/pomiar{}_fs{}_LO{}GHz_med_long.txt'.format(fc,sdr.sample_rate,l/1000000000), 'w') as plik:
    # Zapisz dane do pliku
    #    for element in wyniki_med:
    #        plik.write(str(element) + '\n')
    
    #with open('pomiary_21_02/pomiar{}_fs{}_LO{}_sr.txt'.format(fc,sdr.sample_rate,a), 'w') as plik:
    # Zapisz dane do pliku
    #    for element in wyniki_sr:
    #        plik.write(str(element) + '\n')
    
    wyniki_med=[]
    #wyniki_sr=[]
