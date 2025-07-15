#!/bin/bash

python3 -m venv venv
. venv/bin/activate

GECKODRIVER=geckodriver-v0.36.0-linux64.tar.gz
wget https://github.com/mozilla/geckodriver/releases/download/v0.36.0/${GECKODRIVER}

(
  cd venv/bin
  tar xvf ../../${GECKODRIVER}
  rm ${GECKODRIVER}
)

pip3 install selenium
pip3 install webdriver-manager

