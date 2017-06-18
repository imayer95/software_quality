from threading import Thread

import time


class TimeOutThread(Thread):
    def __init__(self, process, timeout):
        super().__init__()
        self._process = process
        self._timeout = timeout

    def run(self):
        print('wating for time out')
        time.sleep(self._timeout)
        try:
            print('killing process')
            self._process.kill()
        except:
            print('error killing')
