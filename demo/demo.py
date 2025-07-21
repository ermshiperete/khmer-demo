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
    demo.rundemo('http://localhost:8050/index.html')


def runPheasaKhmer(url):
    demo = PheasaKhmer()
    demo.rundemo(url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run demo')
    parser.add_argument('--snap', action='store_true', help='Use Snap Firefox')
    parser.add_argument('--url', metavar='URL', default='https://ភាសាខ្មែរ.com/', help='Use alternate URL for pheasakhmer.com')
    args = parser.parse_args()

    # create_driver(args.snap)
    if args.snap:
        opts = Options()
        firefox_path = "/snap/firefox/current/usr/lib/firefox/firefox"
        opts.binary_location = firefox_path
        geckodriver_path = Service(executable_path="/snap/firefox/current/usr/lib/firefox/geckodriver")
        config.driver = webdriver.Chrome(service=geckodriver_path, options=opts)
    else:
        config.driver = webdriver.Firefox()

    runKeyman()
    runPheasaKhmer(args.url)
    config.driver.quit()
