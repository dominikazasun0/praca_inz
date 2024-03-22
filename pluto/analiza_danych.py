import matplotlib.pyplot as plt
import numpy as np
import statistics
import matplotlib.pyplot as plt
sub=[]
avg=[]
LO=[0.6, 0.7, 0.75, 0.8, 0.9, 1.1,1.2,1.25,1.3,1.4,1.6,1.7,1.75,1.8,1.9,2]
fc_v=[60000, 80000, 100000, 120000,]
lo_max=[0.5,0.6,0.7,0.75,	0.8,0.9	,1	,1.1,	1.2,	1.21,	1.22,	1.23,	1.24,	1.25,	1.26,	1.27,	1.275,	1.28,	1.29,	1.3,	1.35,	1.4,	1.6,	1.7,	1.71,	1.72,	1.73,	1.74,	1.75,	1.76,	1.77,	1.78,	1.79,	1.8,	1.9,	2]

fs_v=[549999, 1000000, 2000000,4000000,6000000,8000000,10000000,12000000]
LO_1=[0.5, 0.6, 0.7, 0.8, 0.9, 1.1, 1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0]
#for fc in fc_v :
for lo in LO_1:
    with open("pomiary_21_02/pomiar80000_fs6000000_LO0.8GHz_med_long_1.txt", "r") as file:
        numbers = [float(line.strip()) for line in file]
        start=numbers[4]
        for j in range(5, len(numbers) - 1):
            error = abs(abs(numbers[j] - start) - 1)
            #print(numbers[j],start,error)
            if error < 20:
                if abs(abs(180 - numbers[j] - start) - 1) > error or j!=163 or j!=164:  # Warunek dodania drugiego typu błędu
                    #print(error)
                    sub.append(error)
            start = numbers[j]
        plt.plot(sub)
        plt.title("Zależność mierzonej róznicy fazy od błędu pomiaru \n dla LO=0.8GHz, fs=6MHz, fc=80kHz")
        plt.grid()
        plt.xlabel("Numer pomiaru [N]")
        plt.ylabel("Różnica fazy [°]")
        plt.savefig("long.svg")
        plt.show()
        avg.append(np.mean(sub))
        #sub=[]
        
        #plt.ylim(0,0.05)
    #plt.plot(LO,avg,'-',marker ='o', markersize='3',label="{}kHz".format(fc/1000))
    #avg=[]


plt.grid()

plt.plot(LO_1,avg,'bo-')
plt.ylabel("Wartość średnia błędu pomiaru [°]")
plt.title("Zależność częstotliwość LO od błędu pomiaru \n dla fs=2MHz, fc=80kHz")
plt.legend(loc='upper left')
plt.xlabel("Częstotliwość LO [GHz]")
#plt.savefig("Zmienne_LO_fs2M_średnie.svg")
plt.show()