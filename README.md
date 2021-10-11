# Custom-built RPi LED Display

This is the source-code for my custom LED display using a Raspberry Pi.

TODO: Add some photos.

## Getting started

### Requirements

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

### Setup

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

### Running

Just run: `./ip_addresses.py`

If desired, set it up to run on boot on your Raspberry Pi (see `ip_addresses.init.d` for an OpenRC script that works on Gentoo, and adapt as needed).

Finally, just edit `ip_addresses.py` according to your needs. Someday in the far future it may be restructured to read data from a configuration file… But for now everything is simply hard-coded in the script itself.

## Objectives and ideas

My objective is to have a nice extra display in addition to whatever else that Raspberry Pi is already doing. This extra display can show relevant information, such as:

* Raspberry Pi health monitors
    * [x] CPU temperature
    * [x] CPU clock frequency
    * [x] Load average
    * [x] Memory usage
* Clock and date
    * [x] Local time
    * [x] In another timezone (world clock)
    * [ ] [Swatch Internet Time](https://en.wikipedia.org/wiki/Swatch_Internet_Time) (but nobody uses it anyway)
    * [x] Age of (or countdown to) a certain moment
* [ ] Data from [Home Assistant](https://www.home-assistant.io/)
    * But which data is relevant?
    * And how to fetch data from Home Assistant? Or should Home Assistant push the data to this display?
* [ ] Weather
    * But from which service? There are many!
    * Might be a better idea to just get data from whatever service is already set up on my Home Assistant.
* Anything else I can come up with

As for the implementation, I envision a daemon that would communicate with the display and handle some extra time-related logic (e.g. scrolling the text, updating the clock, etc.). Additionally, this daemon would expose an HTTP API to control the display. Then, I could have a static HTML page that talks to that API. This whole architecture seems to give me the most power and flexibility… but we are far from getting there.

## Project status

I've written this README before starting the project. It serves as a guide on what I want to achieve. So far… I've connected the display wires to the Raspberry Pi, and I've set up a script to run on boot to display information on the display. So, yes, the project is working and running flawlessly for months. But everything is hard-coded and cannot be modified without editing the code and restarting the script.

## Known issues

### Unix user permissions

Make sure you are part of the `gpio` group. (Or whatever group is relevant for your distro.)

### Why do I get PinFactoryFallback warnings when I import gpiozero?

See [gpiozero FAQ](https://gpiozero.readthedocs.io/en/stable/faq.html#why-do-i-get-pinfactoryfallback-warnings-when-i-import-gpiozero).

### Installing `rpi.gpio` fails

Please see [this forum post](https://www.raspberrypi.org/forums/viewtopic.php?p=1665230#p1665230) and [this ticket](https://sourceforge.net/p/raspberry-gpio-python/tickets/187/). In summary, upstream `rpi.gpio` fails to compile on GCC version 10 due to `-fno-common` now being the default.
