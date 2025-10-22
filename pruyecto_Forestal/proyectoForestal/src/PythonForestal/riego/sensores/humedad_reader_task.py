import threading, time, random
from PythonForestal.patrones.observer.observer import Observable
from PythonForestal.config.constantes import HUM_INTERVAL_S

class HumedadReaderTask(threading.Thread, Observable[float]):
    def __init__(self, stop_event: threading.Event):
        threading.Thread.__init__(self, daemon=True)
        Observable.__init__(self)
        self._stop_ev = stop_event

    def run(self) -> None:
        while not self._stop_ev.is_set():
            self.notificar(50 + random.uniform(-15, 10))
            time.sleep(HUM_INTERVAL_S)
