#Celem pomiaru jest sprawdzenia działania metody próbkowania
#1) Pierwsza seria pomiarów polega na ziwększaniu przesunięcia fazowego między sygnałami o 1st
#Pomiary będą przeprowadzane dla LO=500M, 1GHz, 1.5GHZ
#dla f sygnału = 10kHz....., 150kHz co 20kHz
#założeniem pomairu jest detekcja z rozdzielczością 1st, co wymaga żeby sygnał mierzony miał 360 próbek na okres
#częstotliwość próbkowania będzie dobierana tak żeby sygnał każdy sygnał miał 360 próbek na okres
#zakłądam że każdy z pomiarów ma długość bufora taką żeby zmieściło się w nim 200 okresów sygnału

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
próbki_na_okres=360*8
# Konfigurowanie własności transmisji
sdr.rx_rf_bandwidth = 1000000 # szerokość pasma odbiornika

sdr.rx_lo = 1000000000 # częstotliwość LO odbiornika
sdr.tx_lo = 1000000000 # częstotliwość LO nadajnika
sdr.tx_cyclic_buffer = True # sygnał nadajnika jest wysyłany w nieskończonej pętli 
sdr.tx_hardwaregain_chan0 = -30
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.tx_hardwaregain_chan1 = -30
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



for fc in range (1000, 10000, 1000):

    sdr.sample_rate = fc*360*8 # częstotliwość próbkowania
    ts = 1 / float(sdr.sample_rate)
    t = np.arange(0, N * ts, ts)

    for e in np.arange(1/180,80/180,1/180):
        data = sdr.rx()

    #Podział odebranych danych na kanał 1 i 0
        subst=abs(data[0].real-data[1].real)
        min_val=subst[0]
        for a in range(1,1000):
            if (subst[a] < min_val) :
                min_val=subst[a]
                min_index=a
        Rx_0 = np.array(data[0][min_index:len(data[0])-200])
        Rx_1 = np.array(data[1][min_index:len(data[0])-200])
    
        prev=Rx_0[0]
        prev1=Rx_1[0]
        
        for i in range(0,len(Rx_0)):
                if Rx_0[i].real <= 0 and prev.real > 0 :
                    tabela0.append(i)
                    tabela0_1.append(Rx_0[i].real)
                prev=Rx_0[i]

        for j  in range(0,len(Rx_1)):
                if Rx_1[j].real <= 0 and prev1.real > 0:
                    tabela1.append(j)
                    tabela1_1.append(Rx_1[j].real)
                prev1=Rx_1[j]
        

        result = []
        for i in range(min(len(tabela1), len(tabela0))):
            if tabela0[i] < tabela1[i] :
                result.append((tabela1[i] - tabela0[i]))
            else :
                result.append((tabela0[i] - tabela1[i]))
        """
        #print(próbki_na_okres)
        if tabela0[0] < tabela1[0] :
            for i in range(min(len(tabela1), len(tabela0))) :
                result.append((tabela1[i] - tabela0[i]))
        else :
            for j in range(min(len(tabela1), len(tabela0))) :
                result.append((tabela0[j] - tabela1[j]))
        
        with open('wyniki_29_01/wyniki/{}.txt'.format(datetime.now()), 'w') as plik:
        # Zapisz dane do pliku
            for element in result:
                plik.write(str(element) + '\n')

        with open('wyniki_29_01/Rx_0/Rx_0{}.txt'.format(datetime.now()), 'w') as plik:
        # Zapisz dane do pliku
            for element in Rx_0.real:
                plik.write(str(element) + '\n')

        with open('wyniki_29_01/Rx_1/Rx_1{}.txt'.format(datetime.now()), 'w') as plik:
        # Zapisz dane do pliku
            for element in Rx_1.real:
                plik.write(str(element) + '\n')
        
        with open('wyniki_29_01/tabela0/tabela0{}.txt'.format(datetime.now()), 'w') as plik:
        # Zapisz dane do pliku
            for element in tabela0:
                plik.write(str(element) + '\n')
        
        """
        wyniki.append(statistics.median(result)*(360/próbki_na_okres))
        print("Różnica w próbkach mediana:" ,statistics.median(result))
        print('Różnica fazy w stopniach:',statistics.median(result)*(360/próbki_na_okres))   

        tabela0=[]
        tabela1=[]
        tabela1_1=[]
        tabela0_1=[]
        Rx_0=[]
        Rx_1=[]
        sdr.tx_destroy_buffer()
        i = np.cos(2 * np.pi * t * fc) * 2 ** 14
        q = np.sin(2 * np.pi * t * fc) * 2 ** 14
        iq = i + 1j * q

        i1 = np.cos(2 * np.pi * t * fc) * 2 ** 14
        q1 = np.sin(2 * np.pi * t * fc) * 2 ** 14
        iq1 = i1 + 1j * q1


        sdr.tx([iq ,iq1])
        time.sleep(2)
    
    with open('pomiary_02_02/pomiar{}_LO1GHz.txt'.format(fc), 'w') as plik:
    # Zapisz dane do pliku
        for element in wyniki:
            plik.write(str(element) + '\n')
    
    wyniki=[]
