"""
Archivo integrador generado automaticamente
Directorio: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/riego/sensores
Fecha: 2025-10-22 00:37:36
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: __init__.py
# Ruta: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/riego/sensores/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/3: humedad_reader_task.py
# Ruta: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/riego/sensores/humedad_reader_task.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 3/3: temperatura_reader_task.py
# Ruta: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/riego/sensores/temperatura_reader_task.py
# ================================================================================

import threading, time, random
from PythonForestal.patrones.observer.observer import Observable
from PythonForestal.config.constantes import TEMP_INTERVAL_S

class TemperaturaReaderTask(threading.Thread, Observable[float]):
    def __init__(self, stop_event: threading.Event):
        threading.Thread.__init__(self, daemon=True)
        Observable.__init__(self)
        self._stop_ev = stop_event

    def run(self) -> None:
        while not self._stop_ev.is_set():
            self.notificar(25 + random.uniform(-3, 6))
            time.sleep(TEMP_INTERVAL_S)


