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
sdr.sample_rate = 6000000 # częstotliwość próbkowania
sdr.rx_rf_bandwidth = sdr.sample_rate # szerokość pasma odbiornika
sdr.rx_lo = 1000080000 # częstotliwość LO odbiornika
#
#sdr.gain_control_mode_chan0 = "manual" # turn off AGC
#sdr.gain_control_mode_chan1 = "manual"
#gain = 25# allowable range is 0 to 74.5 dB
#sdr.rx_hardwaregain_chan0 = 25# set receive gain
#sdr.rx_hardwaregain_chan1 = gain
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.gain_control_mode_chan1 = "slow_attack"
sdr.rx_buffer_size = 32768
sdr.tx_buffer_size = 32768


sdr.rx_enabled_channels = [0,1] # dwa kanały odbiorcze włączone

N=sdr.tx_buffer_size

# Sygnał transmitowany na kanał 0

order=[]
ch0=[]
arctg_ch0=[]

ch1=[]
arctg_ch1=[]
arc_tg_dod=[]

zeros_ch0=[]      # Miejsca zerowe chan0
zeros_ch1=[]      # Miejsca zerowe chan1

wyniki_med=[]

for e in range(30):
    
    data = sdr.rx() #Odbiór danych
    
    for i in range(len(data[0])):
        arctg_ch0=np.append(arctg_ch0,np.arctan(data[0][i].real/data[0][i].imag))# Obliczenie arctg(i+q) ch0
        arctg_ch1=np.append(arctg_ch1,np.arctan(data[1][i].real/data[1][i].imag)) # Obliczenie arctg(i+q) ch1

    
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

    for i in range(0,min(len(zeros_ch1),len(zeros_ch0))):# Tworzenie sygnału zero-jedynkowego określającego kolejność sygnałów
        if zeros_ch0[i]<zeros_ch1[i]:
            order.append(1)
        elif zeros_ch0[i]>zeros_ch1[i]:
            order.append(0)
        elif zeros_ch0[i]==zeros_ch1[i]:
            zero_0=prosta(zeros_ch0[i],ch0[zeros_ch0[i]],zeros_ch0[i]-1,ch0[zeros_ch0[i]-1])
            zero_1=prosta(zeros_ch1[i],ch1[zeros_ch1[i]],zeros_ch1[i]-1,ch1[zeros_ch1[i]-1])
            #print(zero_0,zero_1)
            if zero_0 < zero_1:
                order.append(1)
            else:
                order.append(0)
    #print(order)

    

    if statistics.median(order)>0.5:# określenie który z sygnałów jest wyprzedzający w fazie, tworzenie sygnału prostokątnego
        #z zachowaniem odpowiednej kolejności działania na bazie sygnału zero-jedynkowego
        arc_tg_diff=arctg_ch0-arctg_ch1
    else:
        arc_tg_diff=arctg_ch1-arctg_ch0

    
    for i in range(0,len(arc_tg_diff)):#oddzielenie części dodatniej sygnału prostokątnego
        if arc_tg_diff[i] > 0:
            arc_tg_dod.append(arc_tg_diff[i])
            
    print("mediana",np.rad2deg(statistics.median(arc_tg_dod)))
    print("\n")
    wyniki_med.append(np.rad2deg(statistics.median(arc_tg_dod)))
    
    plt.plot(ch0[:100], 'ro-')
    plt.plot(ch1[:100], 'bo-')

    plt.show()
    


    ch0=[]
    ch1=[]
    arctg_ch0=[]
    arctg_ch1=[]
    zeros_ch0=[]
    zeros_ch1=[]
    arc_tg_dod=[]
    order=[]
    time.sleep(13)


#with open('26_03/pomiar{}_fs{}_LO{}GHz_longxd.txt'.format(80000,sdr.sample_rate,1.25), 'w') as plik:
# Zapisz dane do pliku
#    for element in wyniki_med:
#        plik.write(str(element) + '\n')