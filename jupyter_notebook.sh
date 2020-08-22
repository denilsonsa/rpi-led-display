#!/bin/sh
./venv/bin/pip install notebook
exec ./venv/bin/jupyter notebook --no-browser --ip=0.0.0.0 "$@"
