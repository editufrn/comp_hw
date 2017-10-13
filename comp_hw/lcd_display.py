# http://www.arduinoecia.com.br/2016/12/como-usar-display-lcd-i2c-raspberry-pi.html
# -*- coding: utf-8 -*-
# Original code found at:
# https://gist.github.com/DenisFromHR/cc863375a6e19dce359d

"""
Compiled, mashed and generally mutilated 2014-2015 by Denis Pleic
Made available under GNU GENERAL PUBLIC LICENSE

# Modified Python I2C library for Raspberry Pi
# as found on http://www.recantha.co.uk/blog/?p=4849
# Joined existing 'i2c_lib.py' and 'lcddriver.py' into a single library
# added bits and pieces from various sources
# By DenisFromHR (Denis Pleic)
# 2015-02-10, ver 0.1

"""

# i2c bus (0 -- original Pi, 1 -- Rev 2 Pi)
I2CBUS = 1

# LCD Address
ADDRESS = 0x3f
#ADDRESS = 0x27

import smbus
import time
from datetime import datetime as dt


class i2c_device(object):
    def __init__(self, addr, port=I2CBUS):
        self.addr = addr
        self.bus = smbus.SMBus(port)

# Write a single command
    def write_cmd(self, cmd):
        self.bus.write_byte(self.addr, cmd)
        time.sleep(0.0001)

# Write a command and argument
    def write_cmd_arg(self, cmd, data):
        self.bus.write_byte_data(self.addr, cmd, data)
        time.sleep(0.0001)

# Write a block of data
    def write_block_data(self, cmd, data):
        self.bus.write_block_data(self.addr, cmd, data)
        time.sleep(0.0001)

# Read a single byte
    def read(self):
        return self.bus.read_byte(self.addr)

# Read
    def read_data(self, cmd):
        return self.bus.read_byte_data(self.addr, cmd)

# Read a block of data
    def read_block_data(self, cmd):
        return self.bus.read_block_data(self.addr, cmd)


# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100  # Enable bit
Rw = 0b00000010  # Read/Write bit
Rs = 0b00000001  # Register select bit


class lcd(object):
    # initializes objects and lcd
    def __init__(self):
        self.lcd_device = i2c_device(ADDRESS)

        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x02)

        self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE |
                       LCD_5x8DOTS | LCD_4BITMODE)
        self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
        self.lcd_write(LCD_CLEARDISPLAY)
        self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
        time.sleep(0.2)

    # clocks EN to latch command
    def lcd_strobe(self, data):
        self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
        time.sleep(.0005)
        self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
        time.sleep(.0001)

    def lcd_write_four_bits(self, data):
        self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
        self.lcd_strobe(data)

    # write a command to lcd
    def lcd_write(self, cmd, mode=0):
        self.lcd_write_four_bits(mode | (cmd & 0xF0))
        self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

    # write a character to lcd (or character rom) 0x09: backlight | RS=DR<
    # works!
    def lcd_write_char(self, charvalue, mode=1):
        self.lcd_write_four_bits(mode | (charvalue & 0xF0))
        self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))

    # escreve a string sempre come�ando da linha 1 posicao 1 com opcao de
    # limpar a tela
    def lcd_display_string_clear(self, clear, string):
        if clear:
            self.lcd_clear()
        if len(string) > 16:
            self.lcd_display_string(string[:16], 1, 0);
            self.lcd_display_string(string[16:], 2, 0);
        else:
            self.lcd_display_string(string, 1, 0)

    # put string function with optional char positioning
    def lcd_display_string(self, string, line=1, pos=0):
        if line == 1:
            pos_new = pos
        elif line == 2:
            pos_new = 0x40 + pos
        elif line == 3:
            pos_new = 0x14 + pos
        elif line == 4:
            pos_new = 0x54 + pos

        self.lcd_write(0x80 + pos_new)

        for char in string:
            self.lcd_write(ord(char), Rs)

    # clear lcd and set to home
    def lcd_clear(self):
        self.lcd_write(LCD_CLEARDISPLAY)
        self.lcd_write(LCD_RETURNHOME)

    # define backlight on/off (lcd.backlight(1); off= lcd.backlight(0)
    def backlight(self, state):  # for state, 1 = on, 0 = off
        if state == 1:
            self.lcd_device.write_cmd(LCD_BACKLIGHT)
        elif state == 0:
            self.lcd_device.write_cmd(LCD_NOBACKLIGHT)

    # add custom characters (0 - 7)
    def lcd_load_custom_chars(self, fontdata):
        self.lcd_write(0x40)
        for char in fontdata:
            for line in char:
                self.lcd_write_char(line)

class LCD2x16(object):
    """
    Classe que representa o comportamento de um display lcd
    equipado com um circuito integrado 2x16
    """

    def __init__(self):
        self._lcdi2c = None
        self.msg = ""
        self.setup()

    def setup(self):
        self._lcdi2c = lcd()
        self._lcdi2c.lcd_clear()


    #TODO implementar a exibição da mensagem completa
    # com ou sem rolagem e com ou sem quebra de palavra
    def mostrar_mensagem_completa(self, msg, scroll=False, split_word=False):
        if split_word:
            self._verificar_quebra_menssagem(msg)

        if self.msg != msg:
            if scroll:
                self._mensagem_rolagem(msg)
            else:
                self._mensagem_completa(msg)

    #TODO implementar a verificação da possibilidade de quebrar
    # a mensagem. Lançar execeção de ValuerError, caso não haja
    # possibilidade
    def _verificar_quebra_mensagem(self, msg):
        raise NotImplementedError

    #TODO implementar a mensagem completa respeitando
    # as dimensões do display
    def _mensagem_completa(self, msg):
        raise NotImplementedError
            
    #TODO implementar rolagem da mensagem
    def _mensagem_rolagem(self, msg):
        raise NotImplementedError

    def mostrar_mensagem(self, msg, linha=1, coluna=0):
        if self.msg != msg:
            self.msg = msg
            self._lcdi2c.lcd_display_string(msg, linha, coluna)

    def mostrar_nova_mensagem(self, msg, linha=1, coluna=1):
        if self.msg != msg:
            self.msg = msg
            self._lcdi2c.lcd_display_string_clear(True, msg)

    def definir_backlight(self, status):
        ''''
        define o backlight do lcd como ativo(True) ou
        desativo (False)
        '''
        self._lcdi2c.backlight(status)

    def limpar(self):
        self.msg = ""
        self._lcdi2c.lcd_clear()

    def get_estado(self):
        '''Returno True se o display estiver ligado, False caso contrario'''
        return self._lcdi2c is None

class LCDTimerDisplay(LCD2x16):
    """
    Classe que representa o comportamento de um display lcd
    equipado com um circuito integrado 2x16 com adicao da exibicao
    da data e hora na linha superior
    """
    formatter = r"%d/%m/%Y %H:%M"
    
    def init(self):
        print("O formato é:" + self.formatter)
        super().__init__()

    def mostrar_mensagem(self, msg, linha=2, coluna=0):
        now = dt.now().strftime(self.formatter)
        self._lcdi2c.lcd_display_string(now, 1, 0)
        if self.msg != msg:
            self.msg = msg
            self._lcdi2c.lcd_display_string(msg, linha, coluna)

    def mostrar_nova_mensagem(self, msg, linha=2, coluna=0):
        if self.msg != msg:
            self._lcdi2c.lcd_clear()
        now = dt.now().strftime(self.formatter)
        self._lcdi2c.lcd_display_string(now, 1, 0)
        if self.msg != msg:
            self.msg = msg
            self._lcdi2c.lcd_display_string(msg, linha, coluna)

'''
Exemplo de uso do display lcd
'''
if (__name__=='__main__'):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('msg_display', help='inserir mensagem do display')
    parser.add_argument('linha', help='linha do display em que será exibida')
    args = parser.parse_args()
    msg = args.msg_display
    linha = args.linha

    display = LCDTimerDisplay()
    display.mostrar_nova_mensagem(msg, linha=int(linha))
    '''
    if msg <= 32:
        display.mostrar_mensagem_completa(msg)
    elif msg > 32:
        display.mostrar_mensagem_completa(msg, scroll=True)
    '''



