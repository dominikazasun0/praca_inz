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

#Dane do wykresu

przebieg=6   # Liczba okresów sygnału jakie chcemy zobaczyć

# Konfigurowanie własności transmisji
sdr = adi.ad9361(uri="ip:192.168.2.1") #Tworzenie radia

# Konfigurowanie własności transmisji
sdr.rx_rf_bandwidth = 1000000 # szerokość pasma odbiornika
sdr.sample_rate = 5500000 # częstotliwość próbkowania
sdr.rx_lo = 70000000 # częstotliwość LO odbiornika
sdr.tx_lo = 70000000 # częstotliwość LO nadajnika
sdr.tx_cyclic_buffer = True # sygnał nadajnika jest wysyłany w nieskończonej pętli 
sdr.tx_hardwaregain_chan0 = -30
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.tx_hardwaregain_chan1 = -30
sdr.gain_control_mode_chan1 = "slow_attack"
sdr.rx_buffer_size = 32768
sdr.tx_buffer_size = 32768
sdr.tx_enabled_channels = [0, 1] # dwa kanały nadawcze włączone
N = 32768 # wielkość bufora danych (ilość próbek sygnału wysyłana podczas jednej transmisji)
fc = 50000 # częstotliwość transmitowanego sygnału w Hz
ts = 1 / float(sdr.sample_rate)
t = np.arange(0, N * ts, ts)
# Sygnał transmitowany na kanał 0
i = np.cos(2 * np.pi * t * fc) * 2 ** 14
q = np.sin(2 * np.pi * t * fc) * 2 ** 14
iq = i + 1j * q

# Sygnał transmitowany na kanał 1
i1 = np.cos(2 * np.pi * t * fc) * 2 ** 14
q1 = np.sin(2 * np.pi * t * fc) * 2 ** 14
iq1 = i1 + 1j * q1

sdr.tx([iq ,iq1])
# Odbiór danych
for m in range(225) :
    data = sdr.rx()

    if m % 5 == 0: # Analizuję co piąty zestaw próbek, bo co piąty zestaw próbek przenoszą się zmiany ustawień generatora
#Podział odebranych danych na kanał 1 i 0
        
        # Poszukiwanie punktu w którym sygnały się przecinają na początku sygnału i wybranie go jako początkowy punkt analizy
        Rx_0 = data[0]
        Rx_1 = data[1]
        
        for i in range(len(Rx_0)) :
            phase_chan1=math.atan(Rx_1.imag[i]/Rx_1.real[i])
            phase_chan0=math.atan(Rx_0.imag[i]/Rx_0.real[i])
            if Rx_0.imag[i] > Rx_1.imag[i] :
                print(Rx_0.imag[i])
                print("faza",(phase_chan0-phase_chan1)*(180/np.pi))
            else :
                print("faza",(phase_chan0-phase_chan1)*(180/np.pi))
        # Obliczenie różnicy fazy
        '''
        for i in range(min(len(tabela0),len(tabela1))) :
            if tabela0[i] < tabela1[i] :
                result.append((tabela1[i] - tabela0[i])*(360/próbki_na_okres))
            else :
                result.append((tabela0[i] - tabela1[i])*(360/próbki_na_okres))
        print('Różnica fazy w stopniach:',np.mean(result))
        
        result_seria.append(np.mean(result))
        '''
        # Tworzenie wykresów
        '''
        chan0_plot_start = int(tabela0[0])
        chan0_plot_stop = int(tabela0[0]) + int(przebieg*próbki_na_okres)

        chan1_plot_start = int(tabela1[0])
        chan1_plot_stop = int(tabela1[0]) + int(przebieg*próbki_na_okres)

        x = range(chan0_plot_start, chan0_plot_stop)
        plt.plot(x, Rx_0[chan0_plot_start:chan0_plot_stop],'k',label='Chan0')
        plt.scatter(tabela0[0:przebieg+1], tabela0_1[0:przebieg+1], color='k', marker='o')

        x = range(chan1_plot_start, chan1_plot_stop)
        plt.plot(x, Rx_1[chan1_plot_start:chan1_plot_stop], 'r', label='Chan1')
        plt.scatter(tabela1[0:przebieg+1], tabela1_1[0:przebieg+1], color='r', marker='o')
        plt.legend(loc='upper left')
        plt.title(f'diff={np.mean(result)}')
        plt.grid()
        plt.show()
        '''
        plt.plot(Rx_0[:1500])
        plt.plot(Rx_1[:1500])
        plt.grid()
        plt.show()
        
    
        print("\n")
        
        # Usuwanie danych po pomiarze
        result = []
        tabela0=[]
        tabela1=[]
        tabela1_1=[]
        tabela0_1=[]
        time.sleep(1)

    else:
        data=[]    
'''
moc =-40     # Moc sygnału
fg = 1500060000 # Częstotliwość ustawiona na generatorze
plt.plot(result_seria[1:],marker='o', linestyle='-')
#plt.title('Metod z aproksymacją - fg={}, fs={},\nmoc={}, faza=11ch2'.format(fg, sdr.sample_rate, moc))
plt.title('Metod z aproksymacją - fg={}, fs={},\nmoc={}, faza=od 0 do 45 co 1'.format(fg, sdr.sample_rate, moc))
plt.xlabel("Iteracja odbioru próbek")
plt.ylabel("Różnica fazy [°]")
plt.grid()
plt.savefig('10_11/sym_16.svg', format='svg')
plt.show()

with open('10_11/sym_16.txt', 'w') as plik:
    # Zapisz dane do pliku
    for element in result_seria:
        plik.write(str(element) + '\n')

with open('chanel1.txt', 'w') as plik:
    # Zapisz dane do pliku
    for element in Rx_1:
        plik.write(str(element) + '\n')        

'''