#!/usr/bin/env python3

import argparse
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import config
from pheasakhmer import PheasaKhmer
from keyman import Keyman


class Controller:
    def __init__(self) -> None:
        self.keymanUrl = 'http://localhost:8050/keyman/index.html'
        self.keymanDemo = Keyman()

    def _runKeyman(self) -> None:
        self.keymanDemo.rundemo(self.keymanUrl)

    def _runPheasaKhmer(self, url) -> None:
        demo = PheasaKhmer()
        demo.rundemo(url)

    def _continueKeymanDemo(self) -> None:
        self.keymanDemo.continue_presentation(self.keymanUrl)

    def runDemo(self):
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
            self._runKeyman()
            self._runPheasaKhmer(url)
            self._continueKeymanDemo()
            if not args.loop:
                break

        config.driver.quit()


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

    controller = Controller()
    controller.runDemo()
