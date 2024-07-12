import matplotlib.pyplot as plt
import numpy as np
import statistics
import matplotlib.pyplot as plt
sub=[]
jeden=[]
avg=[]
srednia=[4.2701529630623805,4.205778602600615, 5.2849044596388755, 11.146809918627614, 15.145158037309294]
x=[0.5,0.4,0.3,0.2,0.1]
colors=['r','b']
LO=[1,2]
fc_v=[20000, 40000,60000, 80000, 100000, 120000,140000,140000]
lo_max=[0.5,0.6,0.7,0.75,	0.8,0.9	,1	,1.1,	1.2,	1.21,	1.22,	1.23,	1.24,	1.25,	1.26,	1.27,	1.275,	1.28,	1.29,	1.3,	1.35,	1.4,	1.6,	1.7,	1.71,	1.72,	1.73,	1.74,	1.75,	1.76,	1.77,	1.78,	1.79,	1.8,	1.9,	2]
lol=[2, 1]
fs_v=[1000000, 2000000,4000000,6000000,8000000]
LO_1=[0.5, 0.6, 0.7, 0.8, 0.9, 1.1, 1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0]

for i in range(0,180,5):
    print(i)
    avg.append(i+0.5)
#for i in range(-100,49,3):
#    jeden.append(i)

#avg=avg+jeden
for fc in fc_v :
    for lo in lol:

        #with open("praca_inz/pluto/pomiary_21_02/1.5GHz/pomiar100000_fs8000000_LO1.5GHz_med.txt", "r") as file:
        #with open("praca_inz/pluto/pomiary_21_02/LO1GHz/pomiar160000_fs8000000_LO1GHz_med.txt", "r") as file:
        #with open("praca_inz/pluto/pomiary_21_02/LO/120k/{}.txt".format(a), "r") as file:
        #with open("praca_inz/pluto/pomiary_21_02/pomiar80000_fs6000000_LO0.8GHz_med_long_1.txt", "r") as file:
        #with open("praca_inz/pluto/pomiary_21_02/pomiar80000_fs6000000_LO0.8GHz_med_long_1.txt".format(lo), "r") as file:
        #with open("wyniki_29_01/Rx_0/Rx_071.0.txt".format(lo), "r") as file:
        #with open("pomiary_02_02/0.125_stopnia/seria_1/pomir1000_LO500MHz.txt".format(lo), "r") as file:
        with open("26_03/pomiar80000_fs6000000_LO1GHz_20_G0_inny_dzielnik.txt", "r") as file:
        #with open("15_04/pomiar80000_fs2000000_LO2GHz_zmiana_5.txt", "r") as file:
            numbers = [float(line.strip()) for line in file]
            #numbers[44+8]=180-numbers[44+8]
            start=numbers[0]
            for j in range(1, len(numbers)):
                error = (abs(numbers[j] - start)-5)
                #print(numbers[j],start,error)
                if error < 5000:
                    #if abs(abs(180 - numbers[j] - start) - 1) > error:  # Warunek dodania drugiego typu błędu
                        #print(error)
                    sub.append(error)
                start = numbers[j]
       
        
        #numbers.reverse()
        #sub.reverse()
        #sub[35]=0.49
        #sub.pop(17)
        #numbers[6+46]=180-numbers[6+46]
        plt.plot(sub)
        #plt.plot(avg,np.array(numbers[4:40])-np.array(avg))
        #plt.plot(numbers[15:],sub[14:])
        #plt.plot(numbers[9:45],"o-")
        #plt.plot(avg,avg , "b", label="charakterystyka idealna")
        #plt.plot(avg,numbers[9:45],"r",label="charakterystyka zmierzona")
        #print(np.mean(sub))
        #plt.plot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],numbers[80:100], "r",label="0.5 GHz")
        #plt.plot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],numbers[40:60], "b", label="1 GHz")
        #plt.plot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],numbers[60:80], "g", label="1.25 GHz")
        #plt.plot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],numbers[20:40], "m",label="2 GHz")
        #plt.plot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],numbers[:20], "k",label="3 GHz")
        #plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
        #plt.yticks([0.44,0.45,0.46,0.47,0.48,0.49,0.5,0.51,0.52,0.53,0.54,0.55])
        #plt.plot(avg,sub,color=colors[a-1], label="{}={} GHz".format("$f_{LO}$",a-0.3*(a-2)))
        #plt.plot(avg,numbers[4:])
        #plt.plot(avg,numbers[4:48],'-')
        #plt.legend(loc='upper left')
        #plt.plot(avg,avg)
        plt.xlabel("Wprowadzona różnica fazy [°]")
        #plt.xlabel("Numer pomiaru [N]")
        plt.ylabel("Zmierzona różnica fazy [°]")
        #plt.ylabel("Błąd pomiaru różnicy fazy [°]")
        #plt.plot(srednia)
        #plt.title("2GHz")
        plt.grid()
        #plt.xlabel("Numer pomiaru")
        #plt.ylabel("Zmierzona różnica fazy [°]")
        plt.show()
        #plt.plot(sub,'-',label="seria {}".format(3-lo),linewidth="{}".format(1.25*lo),color=colors[lo-1])
        sub=[]
    #plt.grid()  
    #plt.legend(loc='upper right')
    #plt.show()     
    #plt.plot(jeden)   
    #jeden=[]
#plt.title("Zależność mierzonej różnicy fazy od błędu pomiaru \n dla LO=0.8GHz, fs=6MHz, fc=80kHz")

#plt.show()
"""
plt.plot(jeden)
plt.grid()

plt.xlabel("Numer pomiaru [-]")
#plt.xlabel("Mierzona różnica fazy [°]")
plt.legend(loc='upper right')
plt.ylabel("Bład pomiaru [°]")
#plt.savefig("26_03/long_p+p.svg")
plt.show()
avg.append(np.mean(sub))
print(np.mean(sub))
    
        
        #plt.ylim(0,0.05)
    #plt.plot(LO,avg,'-',marker ='o', markersize='3',label="{}kHz".format(fc/1000))
    #avg=[]


plt.grid()

plt.plot(srednia,'bo-')
plt.ylabel("Wartość średnia błędu pomiaru [°]")
plt.title("Zależność częstotliwość LO od błędu pomiaru \n dla fs=2MHz, fc=80kHz")
plt.legend(loc='upper left')
plt.xlabel("Częstotliwość LO [GHz]")
#plt.savefig("Zmienne_LO_fs2M_średnie.svg")
plt.show()

"""