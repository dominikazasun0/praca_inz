import matplotlib.pyplot as plt
import numpy as np
import statistics
sub=[]
srednia=[]
x=[20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000]
f=10000
for j in range(20000,100000,10000):
    with open("arctg_pomiary_pluto+pluto/arctg_LO599999998_fc{}_fs10000000.txt".format(j), "r") as file:
        numbers = [float(line.strip()) for line in file]
        prev=numbers[6]
        for i in range(7,len(numbers)-1):
            zmienna=abs(1-(abs(numbers[i]-prev)))
            sub.append(zmienna)
            prev=numbers[i]
            #print(srednia)
    srednia.append(np.max(sub)) 
    sub=[]
    
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
'''
plt.plot(x,srednia,marker='o')
plt.legend(loc='upper left')
plt.grid()
plt.show()

