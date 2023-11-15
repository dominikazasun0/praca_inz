#https://github.com/analogdevicesinc/pyadi-iio/blob/master/examples/ad9361_example.py
# Copyright (C) 2022 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD
import adi
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import time
#import tkinter as tk

tabela0=[]      # Miejsca zerowe chan0
tabela0_1=[]    # Wartości miejsc zerowych chan0
tabela1=[]      # Miejsca zerowe chan1
tabela1_1=[]    # Wartości miejsc zerowych chan1
result_seria=[] # Zapis wyników pomiaru
result = []

#Dane do wykresu
moc =-40     # Moc sygnału
fg=400040000 # Częstotliwość ustawiona na generatorze
przebieg=6   # Liczba okresów sygnału jakie chcemy zobaczyć

# Konfigurowanie własności transmisji
sdr = adi.ad9361(uri="ip:192.168.2.1") #Tworzenie radia
sdr.rx_rf_bandwidth = 1000000 # szerokość pasma odbiornika
sdr.sample_rate = 10000000 # częstotliwość próbkowania
sdr.rx_lo = 400000000 # częstotliwość LO odbiornika
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.gain_control_mode_chan1 = "slow_attack"
sdr.rx_buffer_size = 32768
sdr.rx_enabled_channels = [0 ,1] # dwa kanały odbiorcze włączone


# Odbiór danych
for m in range(200) :
    data = sdr.rx()

    if m % 5 == 0: # Analizuję co piąty zestaw próbek, bo co piąty zestaw próbek przenoszą się zmiany ustawień generatora
#Podział odebranych danych na kanał 1 i 0
        Rx_0 = np.array(data[0][200:len(data[0])-200])
        Rx_1 = np.array(data[1][200:len(data[1])-200])
        
        '''
        while (Rx_0[0]>=0 and Rx_1[0]<=0) or (Rx_0[0]<=0 and Rx_1[0]>=0) :
            if Rx_0[0] >=0 :
                Rx_0[0:50] = np.full(50,-1)
            if Rx_1[0] >=0 :    
                Rx_1[0:50] = np.full(50,-1)
            print("Robię dobrą robotę")
        '''
        
        prev_0 = Rx_0[0]
        prev_1 = Rx_1[0]
        
        # Detekcja miejsc zerowych
        for i  in range(0,len(Rx_0)):
            if Rx_0[i].real <= 0 and prev_0.real > 0 :
                tabela0.append(i)
                tabela0_1.append(Rx_0[i].real)
            prev_0=Rx_0[i]

        for j  in range(0,len(Rx_1)):
            if Rx_1[j].real <= 0 and prev_1.real > 0 :
                tabela1.append(j)
                tabela1_1.append(Rx_1[j].real)
            prev_1=Rx_1[j]
        
        próbki_na_okres=tabela0[1]-tabela0[0]
        
        if Rx_0[0] > Rx_0[1] :
            if not((Rx_0[0] < 0 and Rx_1[0] < 0 ) or (Rx_0[0] > 0 and Rx_1[0] > 0 )):
                print("Będzie błąd")
                if Rx_0[0] > 0 :
                    del tabela0[0]
                if Rx_1[0] > 0:
                    del tabela1[0]   

        
        #print(len(tabela1))
        #print(len(tabela0))
        
        # Obliczenie różnicy fazy
        if tabela0[0] < tabela1[0] :
            for i in range(len(tabela1)-100) :
                result.append((tabela1[i] - tabela0[i])*(360/próbki_na_okres))
        else :
            for j in range(len(tabela1)-100) :
                result.append((tabela0[j] - tabela1[j])*(360/próbki_na_okres))
        
        print('Różnica fazy w stopniach:',np.mean(result))
        
        result_seria.append(np.mean(result))
        '''
        # Tworzenie wykresów
        chan0_plot_start = tabela0[0]
        chan0_plot_stop = tabela0[0] + przebieg*próbki_na_okres

        chan1_plot_start = tabela1[0]
        chan1_plot_stop = tabela1[0] + przebieg*próbki_na_okres

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
        
        plt.plot(Rx_0)
        plt.plot(Rx_1)
        plt.grid()
        plt.show()
        '''
        print("\n")
        
        # Usuwanie danych po pomiarze
        result = []
        tabela0=[]
        tabela1=[]
        tabela1_1=[]
        tabela0_1=[]
        

    else:
        data=[]    

plt.plot(result_seria,marker='o', linestyle='-')
plt.title('Metod bez aproksymacji - fg={}, fs={},\nmoc={}, faza=90'.format(fg, sdr.sample_rate, moc))
plt.xlabel("Iteracja odbioru próbek")
plt.ylabel("Różnica fazy [°]")
plt.grid()
plt.savefig('sym_21.svg', format='svg')
plt.show()

with open('sym_21.txt', 'w') as plik:
    # Zapisz dane do pliku
    for element in result_seria:
        plik.write(str(element) + '\n')
'''
with open('chanel1.txt', 'w') as plik:
    # Zapisz dane do pliku
    for element in Rx_1:
        plik.write(str(element) + '\n')        

'''