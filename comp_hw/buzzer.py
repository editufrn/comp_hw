# -*- coding: utf-8 -*-

import time
from RPi.GPIO import PWM 
if (__name__=='__main__'):
    from comp_hw import ComponenteHardwareGPIO
else:
    from .comp_hw import ComponenteHardwareGPIO

class Buzzer(ComponenteHardwareGPIO):
    
    '''
    Inicaliza o buzzer com a porta e o modo da porta "BOARD" ou "BCM"
    '''
    def __init__(self, porta, modo="BOARD", sinal_invertido=False):
        super().__init__(porta, modo, sinal_invertido)

    def play_negado(self):
        # Inicia buzzer
        #GPIO.setup(self.gpio, GPIO.OUT)
        buzz = PWM(self.porta, 131)  # initial frequency.
        buzz.start(50)  # Start buzzer pin with 50% duty ration
        time.sleep(0.2)  # delay a note for beat * 0.5s
        buzz.ChangeFrequency(101)  # Change the frequency along the song note
        time.sleep(0.7)  # delay a note for beat * 0.5s
        buzz.stop()  # Stop the buzzer
        super().ligar_porta()  # Set buzzer pin to High

    def play_liberado(self):
        # Inicia buzzer
        #GPIO.setup(self.gpio, GPIO.OUT)
        buzz = PWM(self.porta, 500)  # initial frequency.
        buzz.start(50)  # Start buzzer pin with 50% duty ration
        time.sleep(0.2)  # delay a note for beat * 0.5s
    #    buzz.ChangeFrequency(550) # Change the frequency along the song note
    #    time.sleep(0.4) # delay a note for beat * 0.5s
        buzz.stop()  # Stop the buzzer
        super().ligar_porta()  # Set buzzer pin to High
    

'''
Exemplo de execução do componente buzzer
Uso: python3 buzzer.py port_number
'''
if (__name__=='__main__'):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('port_number', help="insert port number buzzer")
    parser.add_argument('mode', help="insert mapping port mode")
    args = parser.parse_args()
    b = Buzzer(int(args.port_number), args.mode) 
    b.play_liberado()
    time.sleep(0.3)
    b.play_liberado()
    time.sleep(0.1)
    b.play_liberado()
    time.sleep(0.9)
    b.play_negado()
    time.sleep(0.3)
    b.play_negado() 
    time.sleep(0.2)
    b.play_negado()
