# Custom-built RPi LED Display

This is the source-code for my custom LED display using a Raspberry Pi.

TODO: Add some photos.

## Requirements

Hardware:

* Raspberry Pi 4 (but could have been any other board that provides two GPIO pins).
* 16-digit 7-segment LED display based on TM1640 chip.
    * Mine has this text printed on the back of the PCB: *JY-MCU JY-LM1640 V:1.1*
    * It's the same one from these projects:
        * https://www.arduino-projekte.de/index.php?n=76
        * https://tronixstuff.blogspot.com/2012/04/arduino-and-tm1640-led-display-modules.html
        * https://www.instructables.com/id/Self-contained-16-Digit-display-Arduino-Attiny/
    * And I can't find this module for sale anymore.

Software:

* Any (modern) Linux distribution. I'm running Gentoo arm64 (`aarch64`), but it doesn't matter.
* Python 3.
* The code from this repository.

## Setup

Hardware setup:

* Connect the LED display module to the pins on the Raspberry Pi.
    * The module has four wires:
        * VDD 5V (for powering the LEDs and the board)
        * GND (ground, AKA 0V)
        * DIN (data input, data transmitted from the Raspberry Pi to the display)
        * SCLK (serial clock, driven by the Raspberry Pi via software)
    * Connect VDD and GND.
    * Pick any two GPIO pins and connect DIN and SCLK to those pins. Remember to take note of the number (e.g. GPIO23 and GPIO24).
    * Confused about the pins in your Raspberry Pi? There are a few ideas:
        * Look at <https://pinout.xyz/>.
        * Run the command-line tool `pinout` (also available in `./venv/bin/pinout`), [provided by `gpiozero` package](https://gpiozero.readthedocs.io/en/stable/cli_tools.html#pinout).
* Make sure your power supply is good enough.
    * According to the datasheet, this module can have 400mW of power consumption, which roughly translates to 80mA at 5V. I haven't measured the actual consumption, though.

Software setup:

1. Run: `./one_time_setup.sh`

## Objectives and ideas

My objective is to have a nice extra display in addition to whatever else that Raspberry Pi is already doing. (Right now, it runs RetroArch, plus ssh and http servers, and some other ideas reserved for the future.) This extra display can show relevant information, such as:

* Raspberry Pi health monitors
    * CPU temperature
    * CPU clock
    * Load average
    * Memory usage
* Weather
* Clock
    * Local time
    * Some other timezone
    * [Swatch Internet Time](https://en.wikipedia.org/wiki/Swatch_Internet_Time) ([online clock](https://github.com/Clidus/swatch))
* Data from [Home Assistant](https://www.home-assistant.io/)
* Anything else I can come up with

Well, this is the idea, the objective. This is not completely implemented.

As for the implementation, I envision a daemon that would communicate with the display and handle some extra time-related logic (e.g. scrolling the text, updating the clock, etc.). Additionally, this daemon would expose an HTTP API to control the display. Then, I could have a static HTML page that talks to that API. This whole architecture seems to give me the most power and flexibility.

## Project status

I've written this README before starting the project. It serves as a guide on what I want to achieve. So far... I've connected the display wires to the Raspberry Pi. That's all.

## Known issues

### Unix user permissions

Make sure you are part of the `gpio` group. (Or whatever group is relevant for your distro.)

### Why do I get PinFactoryFallback warnings when I import gpiozero?

See [gpiozero FAQ](https://gpiozero.readthedocs.io/en/stable/faq.html#why-do-i-get-pinfactoryfallback-warnings-when-i-import-gpiozero).

### Installing `rpi.gpio` fails

Please see [this forum post](https://www.raspberrypi.org/forums/viewtopic.php?p=1665230#p1665230) and [this ticket](https://sourceforge.net/p/raspberry-gpio-python/tickets/187/). In summary, upstream `rpi.gpio` fails to compile on GCC version 10 due to `-fno-common` now being the default.
