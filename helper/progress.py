# This file is part of osint.py program
# @lymbin 2021-2022

import time
from threading import Thread
from progress.spinner import Spinner


class Progress(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.progress_state = 'RUNNING'

    def run(self):
        time.sleep(1)
        spinner = Spinner('Loading ')
        while self.progress_state != 'FINISHED':
            time.sleep(0.1)
            spinner.next()

    def state(self, state):
        self.progress_state = state
