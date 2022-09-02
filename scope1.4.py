import random
import time
import sys
from oscilloscope import Osc
from ADS1x15 import ADS1115
adc = ADS1115()

A0 = 0
A1 = 1



osc = Osc(nrows=2, ncols=2)

try: 
    @osc.signal
    def signal1(state):
        while True:
            A0 = adc.read_adc(0, 1)
            state.draw((A0))
            time.sleep(0.1)


    @osc.signal
    def signal2(state):
        while True:
            A1 = adc.read_adc(1, 2)
            state.draw(A1, row=0, col=1)
            time.sleep(0.1)
            
    @osc.signal
    def signal3(state):
        while True:
            A2 = adc.read_adc(2, 4)
            state.draw(A2, row=1, col=0)
            time.sleep(0.1)
            
    @osc.signal
    def signal4(state):
        while True:
            A3 = adc.read_adc(3, 8)
            state.draw(A3, row=1, col=1)
            time.sleep(0.1)
            

    osc.start()


except KeyboardInterrupt:
    print("keyboardInterrupt")
    print("\nBye")
    sys.exit()