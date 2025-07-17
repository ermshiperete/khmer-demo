#!/bin/bash
if [[ ! -d venv ]]; then
  ./install.sh "$@"
fi

. venv/bin/activate

if [[ -f venv/usesnap ]]; then
  SNAP="--snap"
else
  SNAP=""
fi
./demo.py ${SNAP}
