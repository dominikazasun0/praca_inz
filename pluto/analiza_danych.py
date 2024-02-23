import matplotlib.pyplot as plt
import numpy as np
import statistics
sub=[]
srednia=[]
x=[20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000]
f=10000
error=0
for i in range(2500,20000,2500) :
    with open("pomiary_02_02/0.25_stopnia/seria_3/pomiar{}_LO1.5GHz.txt".format(i), "r") as file:
        numbers = [float(line.strip()) for line in file]
        #print(numbers)
        start=numbers[4]
        for j in range(5,len(numbers)-1):
            sub.append(abs(numbers[j]-start))
            if abs(numbers[j]-start) != 1:
                error=error+1
            start=numbers[j]
        print(sub)
        print(error)
        plt.plot(sub,marker='o', linestyle='-', markersize=2)
        plt.title("{} LO1.5GHz fs{} error={}".format(i, 360*i,error))
        plt.grid()
        plt.xlabel("Numer pomairu")
        plt.ylabel("Zmierzona różnica fazy [°]")
        plt.savefig('pomiary_02_02/0.25_stopnia/seria_3/wykres{}_LO1.5GHz.svg'.format(i), format='svg')  
        plt.show()
    sub=[]
    error=0
#sub=[]    


'''

for j in range(600000000,1000000000,100000000):
        #print(f+j)
    with open("arctg_pomiary/pom{}_zmiana.txt".format(f+j), "r") as file:
        numbers = [float(line.strip()) for line in file]
        prev=numbers[1]
        for i in range(2,len(numbers)-3):
            zmienna=abs(1-(abs(numbers[i]-prev)))
            if zmienna<0.8 :
                sub.append(zmienna)
            prev=numbers[i]
        #print(srednia)
    srednia.append(np.mean(sub)) 
    #plt.plot(np.mean(sub), label="{}".format(f+j))
    #plt.show()  

  

#    print(len(srednia)) 

plt.title("Bład względny pomiaru zmiany o 1 stopień f={} fs=10000000".format(f+j))
plt.xlabel("Mierzony stopień")
plt.ylabel("Bład względny pomiaru")
plt.plot(sub)
plt.grid()
plt.show()
plt.savefig('arctg_pomiary/wyniki/{}.svg'.format(f+j), format='svg')        

plt.title("Średni bład względny pomiaru zmiany o 1 stopień fs=10000000 \ndla różnych fg-LO")
#print(srednia[0:4])
plt.xlabel("fg-LO")
plt.ylabel("Średni bład względny")

plt.plot(range(10000,60000,10000),srednia[:5], label="fg=600M")
plt.plot(range(10000,60000,10000),srednia[5:10], label="fg=700M")
plt.plot(range(10000,60000,10000),srednia[10:15], label="fg=800M")
plt.plot(range(10000,50000,10000),srednia[15:19], label="fg=900M")

plt.plot(sub)
plt.title("Układ Pluto + Pluto\n Metoda próbkowania LO=800MHz fc=10kHz")
plt.xlabel("Numer pomiaru [-]")
plt.ylabel("Błąd względny pomiaru [%]")
plt.legend(loc='upper left')
plt.grid()
plt.show()
'''
