#!/bin/bash

set -eu

python3 -m venv venv
. venv/bin/activate

if [[ "$1" == "--help" ]]; then
  echo "Install everything needed to run the demo"
  echo "Usage: $0 [--help|--uninstall|--snap]"
  echo "  --help show this help"
  echo "  --uninstall  remove virtual environment"
  echo "  --snap       for use with Snap Firefox"
  exit 0
elif [[ "$1" == "--uninstall" ]]; then
  rm -rf venv
  exit 0
elif [[ "$1" == "--snap" ]]; then
  touch venv/usesnap
else
  GECKODRIVER=geckodriver-v0.36.0-linux64.tar.gz
  wget https://github.com/mozilla/geckodriver/releases/download/v0.36.0/${GECKODRIVER}

  (
    cd venv/bin
    tar xvf ../../${GECKODRIVER}
    rm ../../${GECKODRIVER}
  )
fi

pip3 install selenium
pip3 install webdriver-manager
