import threading

class PolargraphTask:

    def __init__(self, plotter, task):
        self.plotter = plotter
        self._task = task
        self._running = False

    def is_running(self):
        return self._thread.is_alive()

    def start(self):
        if(self._running):
            return
        self._thread = threading.Thread(target=self._task , args=(self, ))
        self._thread.daemon = True
        self._running = True
        self._thread .start()

    def stop(self):
        self._running = False
        self._thread.join()
