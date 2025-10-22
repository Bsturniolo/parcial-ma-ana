"""
Archivo integrador generado automaticamente
Directorio: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/riego/control
Fecha: 2025-10-22 00:37:36
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/riego/control/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: riego_controller.py
# Ruta: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/riego/control/riego_controller.py
# ================================================================================

from PythonForestal.patrones.observer.observer import Observer
from PythonForestal.config.constantes import TEMP_UMBRAL_ACTIVA, HUM_UMBRAL_ACTIVA

class RiegoController(Observer[float]):
    def __init__(self, svc):
        self._svc = svc
        self._t = 25.0
        self._h = 50.0

    def actualizar(self, v: float) -> None:
        if 0.0 <= v <= 100.0:
            self._h = v
        else:
            self._t = v
        if self._t > TEMP_UMBRAL_ACTIVA or self._h < HUM_UMBRAL_ACTIVA:
            try:
                self._svc.regar_todos(1.0, temporada="verano")
            except Exception:
                pass


