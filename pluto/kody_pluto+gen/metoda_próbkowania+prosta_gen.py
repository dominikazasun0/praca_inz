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


tabela0=[]
tabela0_1=[]
tabela1=[]
tabela1_1=[]
# Przed użyciem kodu należy ustawić jego tryb pracy na podwójny odbiór i podwójne nadawania

sdr = adi.ad9361(uri="ip:192.168.2.1") #Tworzenie radia

# Konfigurowanie własności transmisji
sdr.rx_rf_bandwidth = 1000000 # szerokość pasma odbiornika
sdr.sample_rate = 10000000 # częstotliwość próbkowania
sdr.rx_lo = 800000000 # częstotliwość LO odbiornika
sdr.gain_control_mode_chan0 = "fast_attack"
sdr.gain_control_mode_chan1 = "fast_attack"
sdr.rx_buffer_size = 32768

# Konfiguracja kanałów dbiorczych
sdr.rx_enabled_channels = [0 ,1] # dwa kanały odbiorcze włączone

#Ustawienia generatora (do wykresu)
moc =-40
fg=800200000
faza=0

result_seria=[]
# Odbiór danych 20 razy (20 x N próbek)
for m in range(200) :
    data = sdr.rx()

#Podział odebranych danych na kanał 1 i 0
    Rx_0=data[0]
    Rx_1=data[1] 
    prev=Rx_0[0]
    prev1=Rx_1[0]

    for i  in range(0,len(Rx_0)):
        if Rx_0[i].real == 0 and prev.real > 0:
            tabela0.append(i)
            tabela0_1.append(Rx_0[i].real)
        elif Rx_0[i].real <= 0 and prev.real > 0 :
            tabela0.append(oblicz_prosta(i-1,prev.real,i,Rx_0[i].real))
            tabela0_1.append(0)
        prev=Rx_0[i]

    for j  in range(0,len(Rx_1)):
        if Rx_1[j].real == 0 and prev1.real > 0:
            tabela1.append(j)
            tabela1_1.append(Rx_1[j].real)
        elif Rx_1[j].real <= 0 and prev1.real > 0 :
            tabela1.append(oblicz_prosta(j-1,prev1.real,j,Rx_1[j].real))
            tabela1_1.append(0)
        prev1=Rx_1[j]


    #próbki_na_okres=(1/fc)/(1/sdr.sample_rate)
    próbki_na_okres=tabela0[1]-tabela0[0]
    '''
    x = range(tabela0[0], tabela0[0] + 6*int(próbki_na_okres))
    plt.plot(x, Rx_0[tabela0[0]:tabela0[0] + 6*int(próbki_na_okres)])
    plt.scatter(tabela0[0:7], tabela0_1[0:7], color='red', label='Zero Crossing', marker='o')



    x = range(tabela1[0], tabela1[0] + 6 * int(próbki_na_okres))
    plt.plot(x, Rx_1[tabela1[0]:tabela1[0] + 6*int(próbki_na_okres)])
    plt.scatter(tabela1[0:7], tabela1_1[0:7], color='black', label='Zero Crossing', marker='o')
    plt.grid()
    plt.show()
    '''
    #print(tabela0[0:5])
    #print(tabela1[0:5])

    #print(len(tabela1))
    #print(len(tabela0))
    result = []
    
    if tabela0[0] < tabela1[0] :
        for i in range(len(tabela1)-150) :
            result.append((tabela1[i] - tabela0[i])*(360/próbki_na_okres))
    else :
        for j in range(20) :
            result.append((tabela1[j+1] - tabela0[j])*(360/próbki_na_okres))
    #print('Różnica fazy w stopniach:',np.mean(result))    
    #plt.title(f'LO={sdr.rx_lo} fs={sdr.sample_rate} fc={fc}')
    result_seria.append(np.mean(result))
    
    tabela0=[]
    tabela1=[]
    tabela1_1=[]
    tabela0_1=[]

plt.plot(result_seria)
plt.title('Metod z aproksymacją - fg={}, fs={}, moc={}, faza={}, LO={}'.format(fg, sdr.sample_rate, moc, faza, sdr.rx_lo))
plt.grid()
plt.show()
'''

with open('result_seria.txt', 'w') as plik:
    # Zapisz dane do pliku
    for element in result_seria:
        plik.write(str(element) + '\n')

with open('chanel1.txt', 'w') as plik:
    # Zapisz dane do pliku
    for element in Rx_1:
        plik.write(str(element) + '\n')        

'''