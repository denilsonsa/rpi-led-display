# Custom-built RPi LED Display

This is the source-code for my custom LED display using a Raspberry Pi.

Hardware:
* Raspberry Pi 4 (but could have been any other).
* 16-digit 7-segment LED display based on LM1640/TM1640. The same one from these projects:
    * https://www.arduino-projekte.de/index.php?n=76
    * https://tronixstuff.blogspot.com/2012/04/arduino-and-tm1640-led-display-modules.html
    * https://www.instructables.com/id/Self-contained-16-Digit-display-Arduino-Attiny/
    * And I can't find this module for sale anymore.

Software:
* Any (modern) Linux distribution. I'm running Gentoo arm64 (`aarch64`), but it doesn't matter.
* Python 3.
* The code from this repository.

## Objectives and ideas

My objective is to have a nice extra display in addition to whatever else that Raspberry Pi is already doing. (Right now, it runs RetroArch, plus ssh and http servers, and some other ideas reserved for the future.) This extra display can show relevant information, such as:

* Raspberry Pi health monitors
    * CPU temperature
    * CPU clock
    * Load average
    * Memory usage
* Weather
* Clock
* Data from [Home Assistant](https://www.home-assistant.io/)
* Anything else I can come up with

Well, this is the idea, the objective. This is not completely implemented.

As for the implementation, I envision a daemon that would communicate with the display and handle some extra time-related logic (e.g. scrolling the text, updating the clock, etc.). Additionally, this daemon would expose an HTTP API to control the display. Then, I could have a static HTML page that talks to that API. This whole architecture seems to give me the most power and flexibility.

## Project status

I've written this README before starting the project. It serves as a guide on what I want to achieve. So far... I've connected the display wires to the Raspberry Pi. That's all.
