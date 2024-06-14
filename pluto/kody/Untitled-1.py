#https://github.com/analogdevicesinc/pyadi-iio/blob/master/examples/ad9361_example.py
# Copyright (C) 2022 Analog Devices, Inc.
#0 22:22 zmiana pasma
# SPDX short identifier: ADIBSD
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
sdr.tx_rf_bandwidth = sdr.sample_rate # szerokość pasma odbiornikasdr.rx_lo = 1200000000 # częstotliwość LO odbiornika
sdr.tx_lo = 500000000 # częstotliwość LO nadajnika

sdr.tx_cyclic_buffer = True # sygnał nadajnika jest wysyłany w nieskończonej pętli 
sdr.tx_hardwaregain_chan0 = -20
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.tx_hardwaregain_chan1 = -20
sdr.gain_control_mode_chan1 = "slow_attack"
sdr.rx_buffer_size = 32768
sdr.tx_buffer_size = 32768


sdr.tx_enabled_channels = [0] # dwa kanały nadawcze włączone

N=sdr.tx_buffer_size

# Sygnał transmitowany na kanał 0


#Dane do wykresu
# Wysyłanie danych
ts = 1 / float(sdr.sample_rate)
t = np.arange(0, N * ts, ts)
# Odbiór danych

fc=800000

i = np.cos(2 * np.pi * t * fc) * 2 ** 14
q = np.sin(2 * np.pi * t * fc) * 2 ** 14
iq = i + 1j * q
for i in range(1000000):
    sdr.tx(iq)
    sdr.tx_destroy_buffer()

    
 