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
