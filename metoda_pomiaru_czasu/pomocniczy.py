#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import time
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from datetime import datetime


##Ten Kod wyswietla próbki syganłu, pozwala zaobserwować próbki i określić dokładkość wyznaczenia zera.


class MyFlowGraph(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)
        self.samp_rate = samp_rate = 50000

        # Tworzenie bloków

        #Bloki tworzące sygnaly
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 1000, 1, 0, 3.14)
        self.analog_sig_source_x_1 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 1000, 1, 0, 3.14)
        
        #Bloki pobierania probek
        self.probe0 = blocks.probe_signal_f()
        self.probe1 = blocks.probe_signal_f()
        
        #Bloki throttle 
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        
        #Zmienne zapisujące poprzedni czas i poprzednia probke
        self.previous_sample0 = None
        self.previous_sample_time0 = None
        
        self.previous_sample1 = None
        self.previous_sample_time1 = None


        
        # Dodawanie bloków do grafu
        
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.probe0, 0))
	
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_throttle_1, 0))
        self.connect((self.blocks_throttle_1, 0), (self.probe1, 0))
        

    def run(self):
        self.start()
        current_time0 = 0
        current_time1 = 0
        while True:
            samples0 = self.probe0.level()
            samples1 = self.probe1.level()
            #time.sleep(0.3) po dodaniu opóźnienia próbki są wyświetlane jednokrotnie
            print(samples1)
            

if __name__ == "__main__":
    try:
        fg = MyFlowGraph()
        fg.run()
    except KeyboardInterrupt:
        pass
