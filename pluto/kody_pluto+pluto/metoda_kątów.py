import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

tabela1 = [2+3j, 2+1j, -1+3j, 4+3j, -2+4j, -3+4j, 2+4j, -3+9j]
tabela2 = []
#print(tabela1)
prev=tabela1[0]
for i  in range(1,len(tabela1)):
    if tabela1[i].real < 0 and prev.real > 0 :
        tabela2.append(tabela1[i])
        #print("było 0")
    prev=tabela1[i]
print(tabela2)