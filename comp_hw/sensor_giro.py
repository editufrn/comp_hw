# -*- coding: utf-8 -*-
if (__name__=='__main__'):
    from comp_hw import ComponenteHardwareGPIO
else: 
    from .comp_hw import ComponenteHardwareGPIO

class SensorGiro(ComponenteHardwareGPIO):
    '''
    Classe que representa o comportamento dos sensores de giro
    '''

    def __init__(self, num_gpio_dir, num_gpio_esq, pull_up_down="down", modo="BOARD"):
        super().__init__([num_gpio_dir, num_gpio_esq], modo=modo, pull_up_down=pull_up_down)
        self._sensor_esq = num_gpio_esq
        self._sensor_dir = num_gpio_dir

    def get_esq(self):
        '''
        Retorna o valor lido no sensor esquerdo
        '''
        return super().estado_porta(self._sensor_esq)

    def get_dir(self):
        '''
        Retorna o valor lido no sensor direito
        '''
        return super().estado_porta(self._sensor_dir)

if __name__ == '__main__':
    import RPi.GPIO as GPIO
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('port_sensor1',type=int, help="insert port left sensor 1")
    parser.add_argument('port_sensor2', type=int,  help="insert port right sensor 2")
    parser.add_argument('port_led1', type=int,  help="insert port led for left detection 1")
    parser.add_argument('port_led2', type=int,  help="insert port led for right detection 2")
    parser.add_argument('mode', help="insert mapping port mode")
    args = parser.parse_args()
    
    led1 = args.port_led1
    led2 = args.port_led2

    sg = SensorGiro(args.port_sensor1, args.port_sensor2, args.mode, pull_up_down='down'
                    )

    # setup led pin
    GPIO.setmode(sg.modo)
    GPIO.setup(led1, GPIO.OUT)
    GPIO.setup(led2, GPIO.OUT)
    
    try:
        while True:
            if sg.get_esq:
                GPIO.output(led1, False)
            else:
                GPIO.output(led1, True)

            if sg.get_dir:
                GPIO.output(led2, False)
            else:
                GPIO.output(led2, True)
    except:
        GPIO.cleanup(led1)
        GPIO.cleanup(led2)

