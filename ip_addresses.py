#!/usr/bin/env python3

import psutil
import re
import signal
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.tz import gettz
from functools import partial
from os import getloadavg
from socket import AF_INET
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
    # There is psutil.cpu_freq() as well, but that function is longer and heavier.
    # https://github.com/giampaolo/psutil/blob/release-5.8.0/psutil/_pslinux.py#L722


def raiseKeyboardInterrupt(signum, frame):
    raise KeyboardInterrupt()


def display_clock():
    # The length of this string must be a divisor of 60.
    dashes = "_-‾-"
    now = datetime.now()
    # text = now.isoformat(' ', 'seconds')
    # text = now.time().isoformat('seconds')
    text = now.strftime('%H:%M:%S  %a %d')
    text = text.replace(':', dashes[now.second % len(dashes)])
    yield text


def display_clock_timezone(tz, prefix='', suffix=''):
    # The length of this string must be a divisor of 60.
    dashes = "_-‾-"
    now = datetime.now(tz)
    time = now.strftime('%H:%M:%S')
    time = time.replace(':', dashes[now.second % len(dashes)])
    text = prefix + time + suffix
    yield text


def display_relative_time(reference, prefix='', suffix='', now=None):
    '''Given a reference time, displays how long since/until that time.

    This relative time is calculated by counting seconds. During DST changes,
    this will give different results than naively looking at a clock.

    Here: 1 week = 7 days; 1 day = 24 hours.
    '''

    if now is None:
        now = datetime.now(gettz())

    # timedelta cannot be used here, as it will not consider DST changes.
    secs = int(abs(now.timestamp() - reference.timestamp()))
    mins = secs // 60
    hours = mins // 60
    days = hours // 24
    weeks = days // 7

    secs = secs % 60
    mins = mins % 60
    hours = hours % 24
    days = days % 7

    if weeks > 0 and days > 0:
        out = '{}w {}d'.format(weeks, days)
    elif weeks > 0:
        out = '{} week{}'.format(weeks, '' if weeks == 1 else 's')
    elif days > 0:
        out = "{}d {:02d}h{:02d}'".format(days, hours, mins)
    else:
        out = "{:02d}h{:02d}'{:02d}\"".format(hours, mins, secs)

    yield prefix + out + suffix


def display_calendar_age(reference, prefix='', suffix='', now=None):
    if now is None:
        now = datetime.now(gettz())

    delta = abs(relativedelta(reference, now))
    out = '{}y {}m {}d'.format(delta.years, delta.months, delta.days)
    yield prefix + out + suffix


def display_interfaces():
    for interface, addresses in sorted(psutil.net_if_addrs().items()):
        if interface == 'lo':
            # Skip the loopback interface.
            continue
        if re.match(r'^(docker|veth|br-).+', interface):
            # Skip the docker internal network.
            continue
        for addr in addresses:
            # socket.AF_INET for IPv4
            # socket.AF_INET6 for IPv6
            # psutil.AF_LINK for hardware MAC address

            # Only show IPv4 addresses, ignore everything else.
            if addr.family == AF_INET:
                text = ip_format(addr.address, interface)
                yield text


def display_cpu_stats():
    text = ' {:2.0f}°C   {:4.0f}MHz'.format(
        read_cpu_temperature(),
        read_cpu_freq(),
    )
    yield text
    # TODO: Display only 3 digits for loadavg. I mean:
    # 0.00  to  9.99  or  10.0  to  99.9
    # Not sure if I need a custom formatting function. Have to investigate.
    text = 'load {:.2f} {:.2f} {:.2f}'.format(*getloadavg())
    yield text


def display_mem_stats():
    # Only showing RAM stats because this system doesn't have any SWAP configured.
    ram = psutil.virtual_memory()
    # ram.percent is the used percentage; but it's hard to show '%' on 7-segment display.
    # Well, '%' can be shown as '°o', but it's confusing anyway.
    text = 'RAM {:.0f}G  {:3.1f}G free'.format(ram.total / 1024**3 , ram.available / 1024**3 )
    yield text


def main():
    signal.signal(signal.SIGTERM, raiseKeyboardInterrupt)

    TZ_AMS = gettz('Europe/Amsterdam')
    TZ_BRA = gettz('America/Sao_Paulo')
    birth = datetime(2020, 9, 3, 14, 40, tzinfo=TZ_AMS)

    views = [
        *[(display_clock, 1)] * 4,
        (partial(display_calendar_age, birth, 'baby '), 3),
        (partial(display_relative_time, birth, 'baby '), 3),
        *[(partial(display_clock_timezone, TZ_BRA, prefix='Brazil '), 1)] * 4,
        *[(display_clock, 1)] * 4,
        (display_interfaces, 4),
        *[(display_clock, 1)] * 4,
        (display_cpu_stats, 3),
        (display_mem_stats, 3),
    ]

    with TM1640(clk_pin=24, din_pin=23) as display:
        try:
            display.brightness = 1
            display.write_text('{:^16}'.format('-- HELLO --'))
            sleep(1)
            while True:
                for (callback, delay) in views:
                    for text in callback():
                        # print(repr(text))
                        if isinstance(text, bytes):
                            display.write_bytes(text)
                        elif isinstance(text, str):
                            display.write_text(text)
                        else:
                            raise TypeError('Expected str or bytes, received {!r}'.format(text))
                        sleep(delay)
        except KeyboardInterrupt:
            display.write_text('GOODBYE...')
            display.brightness = 1
            sleep(1)
            display.write_text('')
            display.brightness = 0


if __name__ == '__main__':
    main()
