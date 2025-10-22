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
