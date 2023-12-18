#https://github.com/analogdevicesinc/pyadi-iio/blob/master/examples/ad9361_example.py
# Copyright (C) 2022 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD
import adi
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import time



przebieg=6   # Liczba okresów sygnału jakie chcemy zobaczyć

# Konfigurowanie własności transmisji
sdr = adi.ad9361(uri="ip:192.168.2.1") #Tworzenie radia
sdr.rx_rf_bandwidth = 1000000 # szerokość pasma odbiornika
sdr.sample_rate = 10000000 # częstotliwość próbkowania
sdr.rx_lo = 1000000000 # częstotliwość LO odbiornika
sdr.tx_lo = 1000000000 # częstotliwość LO nadajnika
sdr.tx_cyclic_buffer = True # sygnał nadajnika jest wysyłany w nieskończonej pętli 
sdr.tx_hardwaregain_chan0 = -30
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.tx_hardwaregain_chan1 = -30
sdr.gain_control_mode_chan1 = "slow_attack"
sdr.rx_buffer_size = 32768
sdr.tx_buffer_size = 32768

sdr.rx_enabled_channels = [0 ,1] # dwa kanały odbiorcze włączone
sdr.tx_enabled_channels = [0, 1] # dwa kanały nadawcze włączone

N = 32768 # wielkość bufora danych (ilość próbek sygnału wysyłana podczas jednej transmisji)
#fc = 10000 # częstotliwość transmitowanego sygnału w Hz
ts = 1 / float(sdr.sample_rate)
t = np.arange(0, N * ts, ts)

# Sygnał transmitowany na kanał 0


imag_ch0=[]
real_ch0=[]
sum_ch0=[]
arctg_ch0=[]

imag_ch1=[]
real_ch1=[]
sum_ch1=[]
arctg_ch1=[]


arctg_diff_pos=[]
arctg_diff_neg=[]
result_seria_arctg=[]

zeros_ch0=[]      # Miejsca zerowe chan0
zeros_ch1=[]      # Miejsca zerowe chan1
result_sample_seria=[] # Zapis wyników pomiaru
result_sample = []
#Dane do wykresu
# Wysyłanie danych


# Odbiór danych
for fc in range(10000,100000,10000):
    for e in np.arange(1/180,50/180,1/180):
        data = sdr.rx() #Odbiór danych
        samples_per_period=int((1/fc)/(1/sdr.sample_rate))
        print("częstotliwość",fc)
        print("samples_per_period", samples_per_period)
        
        for i in range(len(data[0])):

            #real_ch0=np.append(real_ch0,data[0][i].real)
            #imag_ch0=np.append(imag_ch0,data[0][i].imag)
            sum_ch0=np.append(sum_ch0,data[0][i].real+data[0][i].imag) # Obliczenie i+q ch0
            arctg_ch0=np.append(arctg_ch0,np.rad2deg(np.arctan(data[0][i].imag/data[0][i].real))) # Obliczenie arctg(i+q) ch0

            #real_ch1=np.append(real_ch1,data[1][i].real)
            #imag_ch1=np.append(imag_ch1,data[1][i].imag)
            sum_ch1=np.append(sum_ch1,data[1][i].real+data[1][i].imag) # Obliczenie i+q ch1
            arctg_ch1=np.append(arctg_ch1,np.rad2deg(np.arctan(data[1][i].imag/data[1][i].real))) # Obliczenie arctg(i+q) ch1

        
        # Wybranie początkowego punktu pomiaru w próbce w której sum_ch0 i sum_ch1 się przecinają
        subst=abs(sum_ch0-sum_ch1)
        min_val=subst[0]
        for a in range(1,1000):
            if (subst[a] < min_val) :
                min_val=subst[a]
                min_index=a
        sum_ch0 = np.array(sum_ch0[min_index:len(sum_ch0)-200])
        sum_ch1 = np.array(sum_ch1[min_index:len(sum_ch0)-200])

        # Metoda próbkowa pomiaru fazy
        prev_0 = sum_ch0[0]
        prev_1 = sum_ch1[0]

        for i  in range(1,len(sum_ch0)): # Detekcja miejsc zerowych sum_ch0
            if sum_ch0[i].real <= 0 and prev_0.real > 0:
                zeros_ch0.append(i)
            prev_0=sum_ch0[i]

        for j  in range(1,len(sum_ch1)): # Detekcja miejsc zerowych sum_ch1
            if sum_ch1[j].real <= 0 and prev_1.real > 0 :
                zeros_ch1.append(j)
            prev_1=sum_ch1[j]   


        #print(zeros_ch0[:20])
        #print(zeros_ch1[:20])
        #print(len(zeros_ch0))
        #samples_per_period=zeros_ch0[3]-zeros_ch0[2]
        #print("okres:",samples_per_period)
        # Obliczenie różnicy fazy metodą próbkową
        for i in range(1,min(len(zeros_ch0),len(zeros_ch1))):
            
            if zeros_ch0[i] < zeros_ch1[i] :
                result_sample.append((zeros_ch1[i] - zeros_ch0[i])*(360/samples_per_period))

            else :
                result_sample.append((zeros_ch0[i] - zeros_ch1[i])*(360/samples_per_period))

        print('Różnica fazy w stopniach:',np.mean(result_sample))

        result_sample_seria.append(np.mean(result_sample))

        # Metoda arctg

        arctg_diff=arctg_ch0-arctg_ch1 

        #Określenie który sygnał jest pierwszy
        zmienna=0
        for b in range(1,min(len(zeros_ch0),len(zeros_ch1)),10):
            if (zeros_ch0[b]-zeros_ch0[b-1] < samples_per_period + 2) and (zeros_ch1[b]-zeros_ch1[b-1] < samples_per_period + 2) and (zeros_ch0[b]-zeros_ch0[b-1] > samples_per_period -2)  and (zeros_ch1[b]-zeros_ch1[b-1] > samples_per_period -2):
                if zeros_ch1[b] < zeros_ch0[b]:
                    zmienna=1
                    break

        for l in range(len(arctg_diff)):
            if arctg_diff[l] > 0:
                arctg_diff_pos.append(arctg_diff[l])
            else: 
                arctg_diff_neg.append(arctg_diff[l])
        #print(np.mean(arctg_diff_pos))
        #print(np.mean(arctg_diff_neg))

        
        if zmienna == 1:
            print("ARCTG faza to ", abs(np.mean(arctg_diff_neg)))
            
            result_seria_arctg.append(abs(np.mean(arctg_diff_neg)))
        else:
            print("ARCTG faza to ", abs(np.mean(arctg_diff_pos)))
            result_seria_arctg.append(abs(np.mean(arctg_diff_pos)))
        
        
        '''
        if abs((np.mean(result_sample)-abs(np.mean(arctg_diff_neg))))<abs((np.mean(result_sample)-np.mean(arctg_diff_pos))):
            print("faza to ", abs(np.mean(arctg_diff_neg)))
            
            result_seria_arctg.append(abs(np.mean(arctg_diff_neg)))
        else:
            print("faza to ", abs(np.mean(arctg_diff_pos)))
            result_seria_arctg.append(abs(np.mean(arctg_diff_pos)))
        '''
    
        '''
        plt.plot(sum_ch1, 'r',label="chan1")
        plt.plot(sum_ch0, 'k', label="chan0")
        #plt.plot(arctg_ch1, label="arctg ch1")
        #plt.plot(arctg_ch0, label="arctg ch0")
        plt.plot(arctg_diff, label="arctg ch0 - arctg ch1")
        #plt.title('Metod arctg- fg={}, fs={},\nmoc={}'.format(fg, sdr.sample_rate, moc))
        plt.legend(loc='upper left')
        plt.grid()
        plt.show()
        '''

        sum_ch0=[]
        sum_ch1=[]
        imag_ch0=[]
        imag_ch1=[]
        real_ch0=[]
        real_ch1=[]
        zeros_ch0=[]
        arctg_diff=[]
        zeros_ch1=[]
        arctg_diff_neg=[]
        arctg_diff_pos=[]
        arctg_ch0=[]
        arctg_ch1=[]
        phase_diff=[]
        result_sample=[]
        sdr.tx_destroy_buffer()

        i = np.cos(2 * np.pi * t * fc) * 2 ** 14
        q = np.sin(2 * np.pi * t * fc) * 2 ** 14
        iq = i + 1j * q

        i1 = np.cos(2 * np.pi * t * fc +(e*np.pi)) * 2 ** 14
        q1 = np.sin(2 * np.pi * t * fc + (e*np.pi)) * 2 ** 14
        iq1 = i1 + 1j * q1


        sdr.tx([iq ,iq1])
        time.sleep(40)

    
    with open('arctg_LO{}_fc{}_fs{}.txt'.format(sdr.rx_lo,fc,sdr.sample_rate), 'w') as plik:
        # Zapisz dane do pliku
        for element in result_seria_arctg:
            plik.write(str(element) + '\n')
    
    with open('samples_LO{}_fc{}_fs{}.txt'.format(sdr.rx_lo,fc,sdr.sample_rate), 'w') as plik:
        # Zapisz dane do pliku
        for element in result_sample_seria:
            plik.write(str(element) + '\n')        
    result_seria_arctg=[]
    result_sample_seria=[]
'''
moc =-40     # Moc sygnału
fg = 1500060000 # Częstotliwość ustawiona na generatorze
plt.plot(result_sample[1:],marker='o', linestyle='-')
#plt.title('Metod z aproksymacją - fg={}, fs={},\nmoc={}, faza=11ch2'.format(fg, sdr.sample_rate, moc))
plt.title('Metod z aproksymacją - fg={}, fs={},\nmoc={}, faza=od 0 do 45 co 1'.format(fg, sdr.sample_rate, moc))
plt.xlabel("Iteracja odbioru próbek")
plt.ylabel("Różnica fazy [°]")
plt.grid()
plt.savefig('10_11/sym_16.svg', format='svg')
plt.show()
'''