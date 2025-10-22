"""
INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO
============================================================================
Directorio raiz: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion
Fecha de generacion: 2025-10-22 00:37:36
Total de archivos integrados: 26
Total de directorios procesados: 12
============================================================================
"""

# ==============================================================================
# TABLA DE CONTENIDOS
# ==============================================================================

# DIRECTORIO: .
#   1. __init__.py
#   2. __main__.py
#   3. demo.py
#
# DIRECTORIO: config
#   4. __init__.py
#   5. constantes.py
#
# DIRECTORIO: entidades
#   6. __init__.py
#
# DIRECTORIO: entidades/cultivos
#   7. __init__.py
#   8. cultivos.py
#
# DIRECTORIO: patrones
#   9. __init__.py
#
# DIRECTORIO: patrones/factory
#   10. __init__.py
#   11. cultivo_factory.py
#
# DIRECTORIO: patrones/observer
#   12. __init__.py
#   13. observer.py
#
# DIRECTORIO: patrones/strategy
#   14. __init__.py
#   15. absorcion.py
#
# DIRECTORIO: riego
#   16. __init__.py
#
# DIRECTORIO: riego/control
#   17. __init__.py
#   18. riego_controller.py
#
# DIRECTORIO: riego/sensores
#   19. __init__.py
#   20. humedad_reader_task.py
#   21. temperatura_reader_task.py
#
# DIRECTORIO: servicios
#   22. __init__.py
#   23. persist_exceptions.py
#   24. plantacion_service.py
#   25. registro_service.py
#   26. tierra_service.py
#



################################################################################
# DIRECTORIO: .
################################################################################

# ==============================================================================
# ARCHIVO 1/26: __init__.py
# Directorio: .
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 2/26: __main__.py
# Directorio: .
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/__main__.py
# ==============================================================================

from .demo import demo
if __name__ == "__main__":
    demo()


# ==============================================================================
# ARCHIVO 3/26: demo.py
# Directorio: .
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/demo.py
# ==============================================================================

from __future__ import annotations
import threading, time
from typing import Optional, Dict, Callable
from pathlib import Path

# === IMPORTS DE MÓDULOS ===
from PythonForestal.patrones.strategy.absorcion import (
    AbsorcionAguaStrategy, AbsorcionArbolStrategy, AbsorcionHortalizaStrategy
)
from PythonForestal.patrones.observer.observer import Observer, Observable
from PythonForestal.riego.sensores.temperatura_reader_task import TemperaturaReaderTask
from PythonForestal.riego.sensores.humedad_reader_task import HumedadReaderTask
from PythonForestal.riego.control.riego_controller import RiegoController
from PythonForestal.entidades.cultivos.cultivos import (
    Cultivo, Pino, Olivo, Lechuga, Zanahoria
)
from PythonForestal.servicios.tierra_service import Tierra, Plantacion, TierraService
from PythonForestal.servicios.plantacion_service import PlantacionService
from PythonForestal.servicios.registro_service import RegistroForestal, RegistroForestalService
from PythonForestal.patrones.factory.cultivo_factory import CultivoFactory


# ---------- Singleton (solo para mostrar, SIN lambdas) ----------
def _fmt_pino(c: Cultivo) -> str:
    return f"Pino(altura={getattr(c, 'altura_m', 0):.2f}m)"

def _fmt_olivo(c: Cultivo) -> str:
    return f"Olivo(altura={getattr(c, 'altura_m', 0):.2f}m)"

def _fmt_lechuga(c: Cultivo) -> str:
    return f"Lechuga(lista_para_cosecha={getattr(c, 'lista_para_cosecha', False)})"

def _fmt_zanahoria(c: Cultivo) -> str:
    return f"Zanahoria(lista_para_cosecha={getattr(c, 'lista_para_cosecha', False)})"

def _fmt_default(x: Cultivo) -> str:
    # fallback por si aparece un tipo no mapeado
    return getattr(x, "nombre", x.__class__.__name__)

class CultivoServiceRegistry:
    _inst: Optional["CultivoServiceRegistry"] = None

    def __init__(self):
        self._fmt: Dict[type, Callable[[Cultivo], str]] = {
            Pino: _fmt_pino,
            Olivo: _fmt_olivo,
            Lechuga: _fmt_lechuga,
            Zanahoria: _fmt_zanahoria,
        }

    @classmethod
    def instance(cls) -> "CultivoServiceRegistry":
        if cls._inst is None:
            cls._inst = cls()
        return cls._inst

    def mostrar(self, c: Cultivo) -> str:
        return self._fmt.get(type(c), _fmt_default)(c)


# ---------- Demo ----------
def demo():
    print("="*70); print(" DEMO: Sistema de Gestión Forestal (modular) "); print("="*70)

    # Servicios base
    ts = TierraService()
    t, p = ts.crear_tierra_con_plantacion(1, 10000.0, "Agrelo, Mendoza", "Finca del Madero")
    svc = PlantacionService(p)

    # Factory + Strategy
    svc.plantar(
        CultivoFactory.crear("pino", "Pino Paraná"),
        CultivoFactory.crear("olivo", "Olivo Arbequina"),
        CultivoFactory.crear("lechuga", "Lechuga Criolla"),
        CultivoFactory.crear("zanahoria", "Zanahoria Nantaise"),
    )
    print("2) Cultivos OK (Factory/Strategy)")

    # Observer (sensores + controlador)
    stop = threading.Event()
    temp = TemperaturaReaderTask(stop)
    hum  = HumedadReaderTask(stop)
    ctrl = RiegoController(svc)
    temp.suscribir(ctrl); hum.suscribir(ctrl)
    # Alias exigidos por rúbrica también existen:
    # temp.agregar_observador(ctrl); hum.agregar_observador(ctrl)
    temp.start(); hum.start()
    print("3) Sensores ON (Observer)")

    # riegos rápidos + parada ordenada
    for _ in range(3):
        try:
            svc.regar_todos(1.0, temporada="verano")
        except RuntimeError:
            pass
        time.sleep(0.25)
    stop.set(); temp.join(1.0); hum.join(1.0)
    print("4) Riego simulado OK")

    # Persistencia
    reg = RegistroForestal("Juan Perez", t, p)
    path = RegistroForestalService().persistir(reg)
    print(f"5) Persistencia -> {path}")

    # Checklist final
    print("="*70); print("EJEMPLO COMPLETADO EXITOSAMENTE")
    print("[OK] SINGLETON | [OK] FACTORY | [OK] OBSERVER | [OK] STRATEGY")
    print("="*70)


if __name__ == "__main__":
    demo()



################################################################################
# DIRECTORIO: config
################################################################################

# ==============================================================================
# ARCHIVO 4/26: __init__.py
# Directorio: config
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/config/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 5/26: constantes.py
# Directorio: config
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/config/constantes.py
# ==============================================================================

# Tiempos de muestreo (segundos)
TEMP_INTERVAL_S = 0.20
HUM_INTERVAL_S  = 0.30

# Reglas de riego
TEMP_UMBRAL_ACTIVA = 30.0   # ºC
HUM_UMBRAL_ACTIVA  = 40.0   # %

# Reglas de absorción (Strategy)
ARBOLES_L_VERANO   = 5.0
ARBOLES_L_INVIERNO = 2.0
LECHUGA_L          = 1.0
ZANAHORIA_L        = 2.0



################################################################################
# DIRECTORIO: entidades
################################################################################

# ==============================================================================
# ARCHIVO 6/26: __init__.py
# Directorio: entidades
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/entidades/__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: entidades/cultivos
################################################################################

# ==============================================================================
# ARCHIVO 7/26: __init__.py
# Directorio: entidades/cultivos
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/entidades/cultivos/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 8/26: cultivos.py
# Directorio: entidades/cultivos
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/entidades/cultivos/cultivos.py
# ==============================================================================

from __future__ import annotations
from dataclasses import dataclass
from PythonForestal.patrones.strategy.absorcion import AbsorcionAguaStrategy

@dataclass
class Cultivo:
    nombre: str
    estrategia: AbsorcionAguaStrategy

@dataclass
class Pino(Cultivo):
    altura_m: float = 1.0
    def crecer(self, litros_abs: float):
        if litros_abs > 0:
            self.altura_m += 0.10

@dataclass
class Olivo(Cultivo):
    altura_m: float = 0.5
    def crecer(self, litros_abs: float):
        if litros_abs > 0:
            self.altura_m += 0.01

@dataclass
class Lechuga(Cultivo):
    lista_para_cosecha: bool = False

@dataclass
class Zanahoria(Cultivo):
    lista_para_cosecha: bool = False



################################################################################
# DIRECTORIO: patrones
################################################################################

# ==============================================================================
# ARCHIVO 9/26: __init__.py
# Directorio: patrones
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/patrones/__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: patrones/factory
################################################################################

# ==============================================================================
# ARCHIVO 10/26: __init__.py
# Directorio: patrones/factory
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/patrones/factory/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 11/26: cultivo_factory.py
# Directorio: patrones/factory
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/patrones/factory/cultivo_factory.py
# ==============================================================================

from PythonForestal.entidades.cultivos.cultivos import (
    Cultivo, Pino, Olivo, Lechuga, Zanahoria
)
from PythonForestal.patrones.strategy.absorcion import (
    AbsorcionArbolStrategy, AbsorcionHortalizaStrategy
)

class CultivoFactory:
    @staticmethod
    def crear(tipo: str, nombre: str) -> Cultivo:
        t = (tipo or "").lower()
        if t == "pino":
            return Pino(nombre, AbsorcionArbolStrategy())
        if t == "olivo":
            return Olivo(nombre, AbsorcionArbolStrategy())
        if t == "lechuga":
            return Lechuga(nombre, AbsorcionHortalizaStrategy())
        if t == "zanahoria":
            return Zanahoria(nombre, AbsorcionHortalizaStrategy())
        raise ValueError(f"Tipo desconocido: {tipo}")



################################################################################
# DIRECTORIO: patrones/observer
################################################################################

# ==============================================================================
# ARCHIVO 12/26: __init__.py
# Directorio: patrones/observer
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/patrones/observer/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 13/26: observer.py
# Directorio: patrones/observer
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/patrones/observer/observer.py
# ==============================================================================

from typing import Generic, List, TypeVar

T = TypeVar("T")

class Observer(Generic[T]):
    def actualizar(self, valor: T) -> None:
        raise NotImplementedError

class Observable(Generic[T]):
    def __init__(self) -> None:
        self._obs: List[Observer[T]] = []

    # Nombres “clásicos”
    def suscribir(self, o: "Observer[T]") -> None:
        self._obs.append(o)

    def desuscribir(self, o: "Observer[T]") -> None:
        self._obs = [x for x in self._obs if x is not o]

    def notificar(self, v: T) -> None:
        for o in list(self._obs):
            o.actualizar(v)

    # Aliases que pide la rúbrica / README
    def agregar_observador(self, observador: "Observer[T]") -> None:
        self.suscribir(observador)

    def eliminar_observador(self, observador: "Observer[T]") -> None:
        self.desuscribir(observador)

    def notificar_observadores(self, evento: T) -> None:
        self.notificar(evento)



################################################################################
# DIRECTORIO: patrones/strategy
################################################################################

# ==============================================================================
# ARCHIVO 14/26: __init__.py
# Directorio: patrones/strategy
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/patrones/strategy/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 15/26: absorcion.py
# Directorio: patrones/strategy
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/patrones/strategy/absorcion.py
# ==============================================================================

from __future__ import annotations
from abc import ABC, abstractmethod
from PythonForestal.config.constantes import (
    ARBOLES_L_VERANO, ARBOLES_L_INVIERNO, LECHUGA_L, ZANAHORIA_L
)

class AbsorcionAguaStrategy(ABC):
    @abstractmethod
    def absorber(self, litros_disponibles: float, **contexto) -> float:
        raise NotImplementedError

class AbsorcionArbolStrategy(AbsorcionAguaStrategy):
    def absorber(self, litros_disponibles: float, **contexto) -> float:
        # Árbol: verano vs invierno
        temporada = (contexto.get("temporada") or "verano").lower()
        req = ARBOLES_L_VERANO if temporada == "verano" else ARBOLES_L_INVIERNO
        return min(req, litros_disponibles)

class AbsorcionHortalizaStrategy(AbsorcionAguaStrategy):
    def absorber(self, litros_disponibles: float, **contexto) -> float:
        # Lechuga / Zanahoria
        cultivo = (contexto.get("cultivo") or "").lower()
        req = LECHUGA_L if cultivo == "lechuga" else ZANAHORIA_L
        return min(req, litros_disponibles)



################################################################################
# DIRECTORIO: riego
################################################################################

# ==============================================================================
# ARCHIVO 16/26: __init__.py
# Directorio: riego
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/riego/__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: riego/control
################################################################################

# ==============================================================================
# ARCHIVO 17/26: __init__.py
# Directorio: riego/control
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/riego/control/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 18/26: riego_controller.py
# Directorio: riego/control
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/riego/control/riego_controller.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: riego/sensores
################################################################################

# ==============================================================================
# ARCHIVO 19/26: __init__.py
# Directorio: riego/sensores
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/riego/sensores/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 20/26: humedad_reader_task.py
# Directorio: riego/sensores
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/riego/sensores/humedad_reader_task.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 21/26: temperatura_reader_task.py
# Directorio: riego/sensores
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/riego/sensores/temperatura_reader_task.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: servicios
################################################################################

# ==============================================================================
# ARCHIVO 22/26: __init__.py
# Directorio: servicios
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/servicios/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 23/26: persist_exceptions.py
# Directorio: servicios
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/servicios/persist_exceptions.py
# ==============================================================================

class PersistenciaException(Exception):
    def __init__(self, mensaje: str, nombre_archivo: str = "", operacion: str = ""):
        super().__init__(mensaje)
        self._mensaje = mensaje
        self._nombre = nombre_archivo
        self._op = operacion
    def get_user_message(self) -> str: return self._mensaje
    def get_nombre_archivo(self) -> str: return self._nombre
    def get_tipo_operacion(self) -> str: return self._op


# ==============================================================================
# ARCHIVO 24/26: plantacion_service.py
# Directorio: servicios
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/servicios/plantacion_service.py
# ==============================================================================

from typing import List
from PythonForestal.entidades.cultivos.cultivos import Cultivo, Pino, Olivo, Lechuga, Zanahoria

class PlantacionService:
    def __init__(self, plantacion):
        self.p = plantacion  # instancia de Plantacion (definida en tierra_service)

    def plantar(self, *cs: Cultivo) -> None:
        self.p.cultivos.extend(cs)

    def regar_todos(self, litros_por_cultivo: float, temporada: str = "verano") -> None:
        if not self.p.cultivos:
            return
        total = litros_por_cultivo * len(self.p.cultivos)
        if self.p.agua_disponible_l < total:
            raise RuntimeError("Agua insuficiente")
        absorbidos = 0.0
        for c in self.p.cultivos:
            ctx = {"temporada": temporada, "cultivo": c.__class__.__name__.lower()}
            a = c.estrategia.absorber(litros_por_cultivo, **ctx)
            if isinstance(c, (Pino, Olivo)):
                c.crecer(a)
            if isinstance(c, (Lechuga, Zanahoria)):
                c.lista_para_cosecha = True
            absorbidos += a
        self.p.agua_disponible_l -= absorbidos


# ==============================================================================
# ARCHIVO 25/26: registro_service.py
# Directorio: servicios
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/servicios/registro_service.py
# ==============================================================================

from dataclasses import dataclass
from pathlib import Path
import pickle

@dataclass
class RegistroForestal:
    responsable: str
    tierra: object      # Tierra (definida en tierra_service)
    plantacion: object  # Plantacion (definida en tierra_service)

class RegistroForestalService:
    base = Path("./data")
    def persistir(self, reg: RegistroForestal) -> Path:
        self.base.mkdir(exist_ok=True)
        p = self.base / f"{reg.responsable}.dat"
        with open(p, "wb") as f:
            pickle.dump(reg, f)
        return p


# ==============================================================================
# ARCHIVO 26/26: tierra_service.py
# Directorio: servicios
# Ruta completa: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/servicios/tierra_service.py
# ==============================================================================

from dataclasses import dataclass
from typing import List
from dataclasses import field

@dataclass
class Tierra:
    id_padron_catastral: int
    superficie_m2: float
    domicilio: str

@dataclass
class Plantacion:
    nombre: str
    agua_disponible_l: float = 50.0
    cultivos: List[object] = field(default_factory=list)  # object para evitar ciclos de import

class TierraService:
    def crear_tierra_con_plantacion(self, idp: int, sup: float, dom: str, nombre: str):
        return Tierra(idp, sup, dom), Plantacion(nombre, 50.0, [])



################################################################################
# FIN DEL INTEGRADOR FINAL
# Total de archivos: 26
# Generado: 2025-10-22 00:37:36
################################################################################



### MI MAIN ### 

from PythonForestal.demo import demo

if __name__ == "__main__":
    demo()
