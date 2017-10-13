# -*- coding: utf-8 -*-
'''Implementação da classe abstrata de led'''
if (__name__=='__main__'):
    from comp_hw import ComponenteHardwareGPIO
else: 
    from .comp_hw import ComponenteHardwareGPIO

class LedUnicolor(ComponenteHardwareGPIO):
    '''Classe que simula um led unicolor'''

    def __init__(self, porta, cor, modo="BOARD", sinal_invertido=False):
        super().__init__(porta, modo, sinal_invertido)
        self._cor = cor

    def ligar(self):
        '''Liga o led.'''
        super().ligar_porta()


    def desligar(self):
        '''Desliga o led.'''
        super().desligar_porta()

    def get_cor(self):
        '''
        retorna a cor do led.
        '''
        return self._cor

if (__name__=='__main__'):
    import argparse
    import time
    parser = argparse.ArgumentParser()
    parser.add_argument('port_number', help="insert port number buzzer")
    parser.add_argument('cor', help="insert color of led")
    parser.add_argument('mode', help="insert mapping port mode")
    args = parser.parse_args()
    
    led = LedUnicolor(int(args.port_number), args.cor, args.mode)
    led_info = "led " + args.cor

    print ("Ligando", led_info, "por 10 segundos...")
    #led.ligar()
    time.sleep(10)
    print (led_info, "desligado")

