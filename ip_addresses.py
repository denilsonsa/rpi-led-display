#!/usr/bin/env python3

import datetime
import netifaces
import signal
from time import sleep
from tm1640 import TM1640


def ip_format(ip, iface):
    total = 16
    # IPv4 digits
    digits = sum(1 for c in ip if c != '.')
    # Interface length
    letters = len(iface)
    pad = max(0, total - digits - letters)
    padding = ' ' * pad
    return ip + padding + iface


def raiseKeyboardInterrupt(signum, frame):
    raise KeyboardInterrupt()


def main():
    signal.signal(signal.SIGTERM, raiseKeyboardInterrupt)
    with TM1640(clk_pin=24, din_pin=23) as display:
        try:
            display.brightness = 1
            while True:
                for i in range(5):
                    # now = datetime.datetime.now().isoformat(' ', 'seconds')
                    # now = datetime.datetime.now().time().isoformat('seconds')
                    now = datetime.datetime.now().strftime('%H:%M:%S  %a %d')
                    # print(now)
                    display.write_text(now)
                    sleep(1)
                for interface in netifaces.interfaces():
                    if interface == 'lo':
                        # Skip the loopback interface.
                        continue
                    ipv4_data = netifaces.ifaddresses(interface).get(netifaces.AF_INET, [])
                    for cfg in ipv4_data:
                        ip = cfg.get('addr', '')
                        text = ip_format(ip, interface)
                        # print(text)
                        display.write_text(text)
                        sleep(5)
        except KeyboardInterrupt:
            display.write_text('GOODBYE')
            display.brightness = 1
            sleep(1)
            display.write_text('')
            display.brightness = 0


if __name__ == '__main__':
    main()
