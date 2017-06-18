from threading import Thread

import time


class TimeOutThread(Thread):
    def __init__(self, process, timeout):
        super().__init__()
        self._process = process
        self._timeout = timeout

    def run(self):
        time.sleep(self._timeout)
        try:
            self._process.kill()
        except:
            pass
