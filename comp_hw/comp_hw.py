import RPi.GPIO as GPIO

class ComponenteHardwareGPIO(object):
    
    def __init__(self, porta=[], modo='board', sinal_invertido=False, pull_up_down='notset'):
        '''
        Aloca as portas GPIO de um componente de hardware
        '''
        modo_lower = modo.lower()
        pud = pull_up_down.lower()
        self._sinal_invertido = sinal_invertido

        if pud == 'up':
            self.pull_up_down = GPIO.PUD_UP
        elif pud == 'down':
            self.pull_up_down = GPIO.PUD_DOWN
        else:
            self.pull_up_down = 'notset'

        if modo_lower == 'board':
            self._modo = GPIO.BOARD
        elif modo_lower == 'bcm':
            self._modo = GPIO.BCM
        else:
            raise ValueError('modo: ', modo, 'desconhecido.')
        
        if type(porta) is int:
            self._porta = [porta]
        elif type(porta) is list:
            self._porta = porta
        else:
            raise ValueError('expect int or list')
        self._setup()

    @property
    def porta(self):
        '''
        Retorna uma lista de portas ou uma porta
        '''
        num_portas = len(self._porta)
        if num_portas is 1:
            return self._porta[0]
        else:
            return self._porta

    def _setup(self):
        '''
        Aloca as portas do componente de hardware
        '''
        GPIO.setmode(self._modo)
        for porta in self._porta:
            if self.pull_up_down is not 'notset':
                GPIO.setup(porta, GPIO.IN, self.pull_up_down)
            else:
                GPIO.setup(porta, GPIO.OUT)

    def ligar_porta(self):
        for porta in self._porta:
            GPIO.output(porta, not self._sinal_invertido)

    def desligar_porta(self):
        for porta in self._porta:
            GPIO.output(porta, self._sinal_invertido)

    def estado_porta(self, porta):
        if porta in self._porta:
            return GPIO.input(porta)

    def _cleanup(self):
        '''
        Desaloca as portas utilizadas pelo componente de hardware
        '''
        GPIO.setmode(self._modo)
        for porta in self._porta:
            GPIO.cleanup(porta)

    def __del__(self):
        self._cleanup()

