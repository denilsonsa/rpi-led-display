'''
Module to control the 16-digit 7-segment LED display based on TM1640 chip.

This code was written from scratch, but it was inspired by:
* https://github.com/fmmr/lm1640_display
* https://github.com/rjbatista/tm1638-library
* https://github.com/maxint-rd/TM16xx
* https://github.com/mcauser/micropython-tm1640
* https://github.com/mattytrentini/micropython-tm1640
* https://github.com/mcauser/micropython-tm1637
* https://github.com/WaltonSimons/TM1637

The datasheet is still available on https://web.archive.org/web/20161020100322/http://www.titanmic.com:80/pic/other/2014-11-20-15-36-028.pdf

'''

import segment7
import gpiozero
import warnings
from typing import Callable


def clamp(n, lower, upper):
    '''Clamps/clips a number n into the lower and upper bounds (both inclusive)
    
    >>> clamp(1, 2, 4)
    2
    >>> clamp(2, 2, 4)
    2
    >>> clamp(3, 2, 4)
    3
    >>> clamp(4, 2, 4)
    4
    >>> clamp(5, 2, 4)
    4
    '''
    if n < lower:
        return lower
    if n > upper:
        return upper
    return n


# NOTE: I could try subclassing some class from gpiozero.
# If it works well, I could event try submitting it upstream.
# But, for now, no subclassing.

class TM1640:
    def __init__(self, clk_pin:int, din_pin:int, sleep:Callable = lambda:None, pin_factory=None):
        '''
        Parameters:
        clk_pin: The RPi GPIO pin number for SCLK
        din_pin: The RPi GPIO pin number for DIN
        sleep: A function to sleep between each pin output value change
        pin_factory: Parameter passed to gpiozero constructors
        
        Regarding `sleep` parameter: Technically, the code has to wait a few microseconds between each pin state change. The datasheet says the TM1640 chip has an oscillation frequency of 450MHz, and a maximum clock frequency of 1MHz. However, given this is interpreted Python code running on Raspberry Pi, the amount of time between one state change statement and the next one is already long enough, so we don't need to wait, in practice.
        '''
        self.clk_pin = clk_pin
        self.din_pin = din_pin
        self.clk = gpiozero.OutputDevice(self.clk_pin, initial_value=True, pin_factory=pin_factory)
        self.din = gpiozero.OutputDevice(self.din_pin, initial_value=True, pin_factory=pin_factory)
        self.sleep = sleep
        
        self._brightness = None  # It's unknown at this time.
        self._command1_data()

    def __repr__(self):
        # Note: this is not a 100% representation of this object, because the sleep parameter is omitted. However, it's close enough, and it's sufficient for most purposes.
        return 'TM1640(clk_pin={0.clk_pin}, din_pin={0.din_pin})'.format(self)

    # Context manager support:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def close(self):
        self.clk.close()
        self.din.close()

    # Low-level communication with the device: send_start, send_byte, send_end
    def _send_start(self):
        self.clk.on()
        self.sleep()
        self.din.on()
        self.sleep()
        self.din.off()
        self.sleep()

    def _send_end(self):
        self.clk.off()
        self.sleep()
        self.din.off()
        self.sleep()
        self.clk.on()
        self.sleep()
        self.din.on()
        self.sleep()

    def _send_byte(self, byte:int):
        for i in range(8):
            bit = byte & 1
            byte >>= 1
            self.clk.off()
            self.sleep()
            self.din.value = bit
            self.sleep()
            self.clk.on()
            self.sleep()
        self.clk.off()
        self.sleep()

    def _command1_data(self, fixed_address:bool = False):
        # Bits:
        # index: 7654 3210
        # value: 01xx 0?xx
        # B7+B6: must be 01 to identify a Data command
        # B3: 0 is normal mode, 1 is testing mode (internal use)
        # B2: 0 is auto-increment address, 1 is fixed address
        # x: Other bits are unused and must be zero
        byte = 0b_0100_0000
        if fixed_address:
            byte |= 0b_0000_0100
        self._send_start()
        self._send_byte(byte)
        self._send_end()

    # FIXME: Type annotation should mention "bytes" OR "sequence of integers"
    def _command2_address(self, payload:bytes, address:int = 0):
        # Bits:
        # index: 7654 3210
        # value: 11xx ????
        # B7+B6: must be 11 to identify an Address command
        # B3-B0: the address, from 0 to 15 (there are 16 digits)
        # x: Other bits are unused and must be zero
        byte = 0b_1100_0000 | (address & 0b_0000_1111)
        self._send_start()
        self._send_byte(byte)
        if len(payload) > 16:
            warnings.warn('The payload must be at most 16 bytes, received {0} bytes'.format(len(payload)))
        for b in payload[:16]:
            self._send_byte(b)
        self._send_end()

    def _command3_display_control(self, display_on:bool = True, brightness:int = 0):
        # Bits:
        # index: 7654 3210
        # value: 10xx ?bbb
        # B7+B6: must be 10 to identify a Display Control command
        # B3: 0 is display off, 1 is display on
        # B2-B0: set pulse width to:
        #        0: 1/16
        #        1: 2/16
        #        2: 4/16
        #        3: 10/16
        #        4: 11/16
        #        5: 12/16
        #        6: 13/16
        #        7: 14/16
        # x: Other bits are unused and must be zero
        byte = 0b_1000_0000 | (brightness & 0b_0000_0111)
        if display_on:
            byte |= 0b_0000_1000
        self._send_start()
        self._send_byte(byte)
        self._send_end()

    @property
    def brightness(self):
        '''Brightness goes from 0 (display off) to 8 (maximum brightness).
        
        This means there are 8 levels, plus the level 0 for the display off.
        '''
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = clamp(int(value), 0, 8)
        self._command3_display_control(
            display_on=bool(self._brightness),
            brightness=self._brightness - 1,
        )

    # FIXME: Type annotation should mention "bytes" OR "sequence of integers"
    def write_bytes(self, payload:bytes, address:int = 0):
        self._command2_address(payload, address)

    # Ideas:
    # We can try mapping one char to two digits. It may or may not look good.
    # We should move this conversion from string to bytes into segment7.py
    def write_text(self, text:str, address:int = 0):
        payload = [0] * 16
        i = 0
        for c in text:
            if i >= len(payload):
                warnings.warn('Text is longer than the display.')
                break
            if c == '.':
                if i > 0:
                    payload[i - 1] |= 0b_1000_0000
            else:
                b = segment7.char_to_bin(c)
                payload[i] = b
                i += 1
        self._command2_address(payload, address)
