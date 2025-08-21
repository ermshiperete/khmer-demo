#!/usr/bin/env python3

import argparse
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import config
from pheasakhmer import PheasaKhmer
from keyman import Keyman


def runKeyman():
    demo = Keyman()
    demo.rundemo('http://localhost:8050/keyman/index.html')


def runPheasaKhmer(url):
    demo = PheasaKhmer()
    demo.rundemo(url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run demo')
    parser.add_argument('--snap', action='store_true', help='Use Snap Firefox')
    parser.add_argument('--local', action='store_true', help='Use local copy of pheasakhmer.com')
    parser.add_argument('--loop', action='store_true', help='Run in a loop')
    args = parser.parse_args()

    if args.local:
        url = 'http://localhost:8050/pheasakhmer.com/'
    else:
        url = 'https://ភាសាខ្មែរ.com/'

    # create_driver(args.snap)
    if args.snap:
        opts = Options()
        firefox_path = "/snap/firefox/current/usr/lib/firefox/firefox"
        opts.binary_location = firefox_path
        geckodriver_path = Service(executable_path="/snap/firefox/current/usr/lib/firefox/geckodriver")
        config.driver = webdriver.Chrome(service=geckodriver_path, options=opts)
    else:
        config.driver = webdriver.Firefox()

    config.driver.fullscreen_window()

    while(True):
        runKeyman()
        runPheasaKhmer(url)
        if not args.loop:
            break

    config.driver.quit()
