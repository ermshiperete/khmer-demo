#!/bin/bash

set -eu

DRIVER_VERSION=v0.36.0

if [[ "$1" == "--help" || "$1" == "-h" ]]; then
  echo "Usage: $0 [--help] [--uninstall] [--snap]"
  echo ""
  echo "Install everything needed to run the demo"
  echo ""
  echo "Options:"
  echo "  -h, --help   show this help message and exit"
  echo "  --uninstall  remove virtual environment"
  echo "  --snap       Use Snap Firefox"
  exit 0
fi

python3 -m venv venv

# shellcheck disable=SC1091
. venv/bin/activate

if [[ "$1" == "--uninstall" ]]; then
  rm -rf venv
  exit 0
elif [[ "$1" == "--snap" ]]; then
  touch venv/usesnap
else
  GECKODRIVER=geckodriver-${DRIVER_VERSION}-linux64.tar.gz
  wget https://github.com/mozilla/geckodriver/releases/download/${DRIVER_VERSION}/${GECKODRIVER}

  (
    cd venv/bin
    tar xvf ../../${GECKODRIVER}
    rm ../../${GECKODRIVER}
  )
fi

pip3 install selenium
pip3 install webdriver-manager
