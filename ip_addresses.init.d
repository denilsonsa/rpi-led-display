# This is an OpenRC init script, tested in Gentoo.
#
# How to set this up:
# 1. Copy this file into /etc/init.d/name-of-your-choice
# 2. Adjust all the paths here to point to your paths.
# 3. Adjust the command_user as well.
# 4. Remove this block of comments (the first line of the file must be the shebang).
# 5. Add it to the default runlevel: sudo rc-update add name-of-your-choice default
# 6. You can (re)start it using: sudo rc-service name-of-your-choice restart


#!/sbin/openrc-run
# Copyright 2020 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

name="denilson-display daemon"
description="Shows the current IP addresses on LED display"
command=/home/denilson/myrepos/rpi-led-display/venv/bin/python3
command_args="/home/denilson/myrepos/rpi-led-display/ip_addresses.py"
command_background=1
command_user="denilson"
pidfile="/run/${RC_SVCNAME}.pid"
