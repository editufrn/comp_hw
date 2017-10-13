keymap = {
    "KEY_ESC": (0x01, 1),
    "KEY_1": (0x01, 2, 1, '!'),
    "KEY_2": (0x01, 3, 2, '@'),
    "KEY_3": (0x01, 4, 3, '#'),
    "KEY_4": (0x01, 5, 4, '$'),
    "KEY_5": (0x01, 6, 5, '%'),
    "KEY_6": (0x01, 7, 6, '^'),
    "KEY_7": (0x01, 8, 7, '&'),
    "KEY_8": (0x01, 9, 8, '*'),
    "KEY_9": (0x01, 10, 9, '('),
    "KEY_0": (0x01, 11, 0, '),'),
    "KEY_MINUS": (0x01, 12, '-', '_'),
    "KEY_EQUAL": (0x01, 13, '=', '+'),
    "KEY_BACKSPACE": (0x01, 14),
    "KEY_TAB": (0x01, 15),
    "KEY_Q": (0x01, 16, 'q', 'Q'),
    "KEY_W": (0x01, 17, 'w', 'W'),
    "KEY_E": (0x01, 18, 'e', 'E'),
    "KEY_R": (0x01, 19, 'r', 'R'),
    "KEY_T": (0x01, 20, 't', 'T'),
    "KEY_Y": (0x01, 21, 'y', 'Y'),
    "KEY_U": (0x01, 22, 'u', 'U'),
    "KEY_I": (0x01, 23, 'i', 'I'),
    "KEY_O": (0x01, 24, 'o', 'O'),
    "KEY_P": (0x01, 25, 'p', 'P'),
    "KEY_LEFTBRACE": (0x01, 26),
    "KEY_RIGHTBRACE": (0x01, 27),
    "KEY_ENTER": (0x01, 28, '\n'),
    "KEY_LEFTCTRL": (0x01, 29),
    "KEY_A": (0x01, 30, 'a', 'A'),
    "KEY_S": (0x01, 31, 's', 'S'),
    "KEY_D": (0x01, 32, 'd', 'D'),
    "KEY_F": (0x01, 33, 'f', 'F'),
    "KEY_G": (0x01, 34, 'g', 'G'),
    "KEY_H": (0x01, 35, 'h', 'H'),
    "KEY_J": (0x01, 36, 'j', 'J'),
    "KEY_K": (0x01, 37, 'k', 'K'),
    "KEY_L": (0x01, 38, 'l', 'L'),
    "KEY_SEMICOLON": (0x01, 39, ';', '":'),
    "KEY_APOSTROPHE": (0x01, 40, '\'', '\"'),
    "KEY_GRAVE": (0x01, 41,),
    "KEY_LEFTSHIFT": (0x01, 42),
    "KEY_BACKSLASH": (0x01, 43, '\\', '|'),
    "KEY_Z": (0x01, 44, 'z', 'Z'),
    "KEY_X": (0x01, 45, 'x', 'X'),
    "KEY_C": (0x01, 46, 'c', 'C'),
    "KEY_V": (0x01, 47, 'v', 'V'),
    "KEY_B": (0x01, 48, 'b', 'B'),
    "KEY_N": (0x01, 49, 'n', 'N'),
    "KEY_M": (0x01, 50, 'm', 'M'),
    "KEY_COMMA": (0x01, 51, ',', '<'),
    "KEY_DOT": (0x01, 52, '.', '>'),
    "KEY_SLASH": (0x01, 53, ';', '?'),
    "KEY_RIGHTSHIFT": (0x01, 54),
    "KEY_PASTERISK": (0x01, 55),
    "KEY_LEFTALT": (0x01, 56),
    "KEY_SPACE": (0x01, 57, ' '),
    "KEY_RO": (0x01, 89, '?')
}

# Baseado em:
# http://python-evdev.readthedocs.io/en/latest/tutorial.html#reading-events-from-multiple-devices-using-asyncio

import asyncio
import evdev
import time
from multiprocessing import Process, Queue

class KeyBoard(Process):

    reader = None
    _devices = None
    shift_press = False

    def __init__(self, vendor, product, queue=None):
        Process.__init__(self)
        if type(vendor) == str and type(product) == str:
            self.vendor = int(vendor, 16)
            self.product = int(product, 16)
        elif type(vendor) == int and type(product) == int:
            self.vendor = vendor
            self.product = product
        if queue is None:
            queue = Queue(-1)
        self._queue = queue
        self._setup()

    def run(self):
        asyncio.ensure_future(self.processa_evento())
        loop = asyncio.get_event_loop()
        try:
            loop.run_forever()
        except KeyboardInterrupt as e:
            print("Capturou interrupção por teclado. Liberando dispositivo...")
            try:
                self.reader.ungrab()
            except IOError:
                pass

    def _setup(self):
        # find card reader from vendor and product ids
        try:
            self._devices = [evdev.InputDevice(
                device) for device in evdev.list_devices()]
            self.reader = next(
                device for device in self._devices
                if device.info.vendor == self.vendor
                and device.info.product == self.product)
        except StopIteration:
            print('Device not found: productID: {0}, vendorID: {1}'.format(
                hex(self.vendor), hex(self.product)))
            for device in self._devices:
                device.close()

        try:
            # take full control of reader (requires root)
            self.reader.grab()
            print('Dispositivo conectado: productID: {0}, vendorID: {1}'
                  .format(hex(self.vendor), hex(self.product)))
        except OSError as ose:
            print('Dispositivo: productID: {0}, vendorID: {1}, em ocupado'
                  .format(hex(self.vendor), hex(self.product)))

    async def processa_evento(self):
        async for ev in self.reader.async_read_loop():
            tecla = self.ler_tecla_pressionada(ev)
            if tecla:
                mapeamento_tecla = keymap[tecla]
                tecla_lida = self.decodificar_key(mapeamento_tecla)
                self._queue.put(tecla_lida)
    

    def decodificar_key(self, d):
        msg=""
        if d[1] == 42:
            self.shift_press=True
        else:
            if self.shift_press:
                if len(d) == 4:
                    msg=str(d[3])
                else:
                    msg=str(d[2])
                self.shift_press=False
            else:
                msg=str(d[2])
        return msg

    def ler_tecla_pressionada(self, event):
        tecla=None
        # only get keypress events
        if event.type == evdev.ecodes.EV_KEY:
            decoded_key=evdev.categorize(event)
            # only get downpress
            if decoded_key.keystate == decoded_key.key_down:
                tecla=decoded_key.keycode
                # self.data.put(decoded_key.keycode)
                # print(keymap[decoded_key.keycode])
        return tecla

if __name__ == "__main__" :
    import sys
    if len(sys.argv) == 3:
        vendor = int(sys.argv[1], 16)
        product = int(sys.argv[2], 16)
    else:
        vendor = '0x0802'
        product = '0x3000'
    
    keyboard =  KeyBoard(vendor, product)
    keyboard.start()

    keyboard.join()

