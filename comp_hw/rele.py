if (__name__=='__main__'):
    from comp_hw import ComponenteHardwareGPIO
else:
    from .comp_hw import ComponenteHardwareGPIO


class Rele(ComponenteHardwareGPIO):
    '''Simula o comportamento de um rele'''

    def __init__(self, porta, sinal_invertido, modo="BOARD"):
        super().__init__(porta, modo, sinal_invertido)
    
    def ligar(self):
        '''Liga o dispositivo'''
        super().ligar_porta()

    def desligar(self):
        '''Desliga o dispositivo'''
        super().desligar_porta()


if __name__ == '__main__':
    import argparse
    import time
    parser = argparse.ArgumentParser()
    parser.add_argument('port_number', help="insert port number")
    parser.add_argument('mode', help="insert mapping port mode")
    parser.add_argument('command', help="insert comand [on]/[off]")
    args = parser.parse_args()

    r = Rele(int(args.port_number), args.mode)

    command = args.command.lower()

    if command == 'on':
        r.ligar()
    elif command == 'off':
        r.desligar()
    else:
        raise ValueError('command', args.command, 'invalido')
    time.sleep(3)
