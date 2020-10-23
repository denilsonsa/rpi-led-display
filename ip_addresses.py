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


def slurp(filename):
    with open(filename) as f:
        return f.read()


# Returns Celsius.
def read_cpu_temperature():
    # Raw data is in milliCelsius.
    return float(slurp('/sys/class/thermal/thermal_zone0/temp')) / 1000;


# Returns MHz.
def read_cpu_freq():
    # This Raspberry Pi 4 has cpu0 to cpu4.
    # I believe all of them follow the same clock, so I'm just reading one.
    # Raw data is in kHz.
    return int(slurp('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq')) / 1000;


def raiseKeyboardInterrupt(signum, frame):
    raise KeyboardInterrupt()


def display_clock(display):
    # The length of this string must be a divisor of 60.
    dashes = "_-‾-"
    now = datetime.datetime.now()
    # text = now.isoformat(' ', 'seconds')
    # text = now.time().isoformat('seconds')
    text = now.strftime('%H:%M:%S  %a %d')
    text = text.replace(':', dashes[now.second % len(dashes)])
    # print(text)
    display.write_text(text)


def display_interfaces(display, delay):
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
            sleep(delay)


def display_cpu_stats(display):
    text = " {:2.0f}°C   {:4.0f}MHz".format(
        read_cpu_temperature(),
        read_cpu_freq(),
    )
    # print(text)
    display.write_text(text)


def main():
    signal.signal(signal.SIGTERM, raiseKeyboardInterrupt)
    with TM1640(clk_pin=24, din_pin=23) as display:
        try:
            display.brightness = 1
            display.write_text('{:^16}'.format('-- HELLO --'))
            sleep(1)
            while True:
                for i in range(10):
                    display_clock(display)
                    sleep(1)
                display_interfaces(display, 4)
                display_cpu_stats(display)
                sleep(4)
        except KeyboardInterrupt:
            display.write_text('GOODBYE...')
            display.brightness = 1
            sleep(1)
            display.write_text('')
            display.brightness = 0


if __name__ == '__main__':
    main()
