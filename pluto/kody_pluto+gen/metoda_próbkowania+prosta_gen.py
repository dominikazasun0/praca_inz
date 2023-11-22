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

def oblicz_prosta(x1, y1, x2, y2):
    # Oblicz współczynnik kierunkowy (slope) prostej
    m = (y2 - y1) / (x2 - x1)
    
    # Oblicz przesunięcie wertykalne (y-intercept) prostej (b) używając jednego z punktów
    b = y1 - m * x1
    
    # Wyświetl równanie prostej
    
    # Oblicz miejsce zerowe (x-intercept) prostej (gdzie y = 0)
    x_intercept = -b / m
    
    return x_intercept


tabela0=[]      # Miejsca zerowe chan0
tabela0_1=[]    # Wartości miejsc zerowych chan0
tabela1=[]      # Miejsca zerowe chan1
tabela1_1=[]    # Wartości miejsc zerowych chan1
result_seria=[] # Zapis wyników pomiaru
result = []
moc =-40     # Moc sygnału
fg = 800040000 # Częstotliwość ustawiona na generatorze
#Dane do wykresu

przebieg=6   # Liczba okresów sygnału jakie chcemy zobaczyć

# Konfigurowanie własności transmisji
sdr = adi.ad9361(uri="ip:192.168.2.1") #Tworzenie radia
sdr.rx_rf_bandwidth = 1000000 # szerokość pasma odbiornika
sdr.sample_rate = 10000000 # częstotliwość próbkowania
sdr.rx_lo = 800000000 # częstotliwość LO odbiornika
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.gain_control_mode_chan1 = "slow_attack"
sdr.rx_buffer_size = 32768
sdr.rx_enabled_channels = [0 ,1] # dwa kanały odbiorcze włączone


# Odbiór danych
for m in range(225) :
    data = sdr.rx()

    if m % 5 == 0: # Analizuję co piąty zestaw próbek, bo co piąty zestaw próbek przenoszą się zmiany ustawień generatora
#Podział odebranych danych na kanał 1 i 0
        
        # Poszukiwanie punktu w którym sygnały się przecinają na początku sygnału i wybranie go jako początkowy punkt analizy
        subst=abs(data[0].real-data[1].real)
        min_val=subst[0]
        for a in range(1,1000):
            if (subst[a] < min_val) :
                min_val=subst[a]
                min_index=a
        Rx_0 = np.array(data[0][min_index:len(data[0])-200])
        Rx_1 = np.array(data[1][min_index:len(data[1])-200])
        
        
        # Detekcja miejsc zerowych
        prev_0 = Rx_0[0]
        prev_1 = Rx_1[0]
        
        for i  in range(0,len(Rx_0)):
            if Rx_0[i].real == 0 and prev_0.real > 0:
                tabela0.append(i)
                tabela0_1.append(Rx_0[i].real)
            elif Rx_0[i].real <= 0 and prev_0.real > 0 :
                tabela0.append(oblicz_prosta(i-1,prev_0.real,i,Rx_0[i].real))
                tabela0_1.append(0)
            prev_0=Rx_0[i]

        for j  in range(0,len(Rx_1)):
            if Rx_1[j].real == 0 and prev_1.real > 0:
                tabela1.append(j)
                tabela1_1.append(Rx_1[j].real)
            elif Rx_1[j].real <= 0 and prev_1.real > 0 :
                tabela1.append(oblicz_prosta(j-1,prev_1.real,j,Rx_1[j].real))
                tabela1_1.append(0)
            prev_1=Rx_1[j]
        
        próbki_na_okres=tabela0[1]-tabela0[0]

        
        # Obliczenie różnicy fazy
        
        for i in range(min(len(tabela0),len(tabela1))) :
            if tabela0[i] < tabela1[i] :
                result.append((tabela1[i] - tabela0[i])*(360/próbki_na_okres))
            else :
                result.append((tabela0[i] - tabela1[i])*(360/próbki_na_okres))
        print('Różnica fazy w stopniach:',np.mean(result))
        
        result_seria.append(np.mean(result))

        # Tworzenie wykresów
        
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
    
        plt.plot(Rx_1, 'r',label="chan1")
        plt.plot(Rx_0, 'k', label="chan0")
        plt.legend(loc='upper left')
        plt.title('Metod z aproksymacją - fg={}, fs={},\nmoc={}'.format(fg, sdr.sample_rate, moc))
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
'''
with open('chanel1.txt', 'w') as plik:
    # Zapisz dane do pliku
    for element in Rx_1:
        plik.write(str(element) + '\n')        

'''