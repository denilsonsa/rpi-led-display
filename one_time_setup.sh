#!/bin/bash

# Abort on any error:
set -e

basedir="$(dirname "$(readlink -f "$0")")"
venvdir="$basedir/venv"

if [ ! -d "$venvdir" ] ; then
    python3 -m venv "$venvdir"
fi

export CFLAGS='-fcommon'
"$venvdir"/bin/pip install -r "$basedir/requirements.txt"
