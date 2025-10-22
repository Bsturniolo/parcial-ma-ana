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
from PythonForestal.config.constantes import (
    TEMP_UMBRAL_ACTIVA, HUM_UMBRAL_ACTIVA,
    TEMP_INTERVAL_S, HUM_INTERVAL_S,
    ARBOLES_L_VERANO, ARBOLES_L_INVIERNO, LECHUGA_L, ZANAHORIA_L
)

# ---------- Singleton (sin lambdas) ----------
def _fmt_pino(c: Cultivo) -> str:
    return f"Pino(altura={getattr(c, 'altura_m', 0):.2f}m)"

def _fmt_olivo(c: Cultivo) -> str:
    return f"Olivo(altura={getattr(c, 'altura_m', 0):.2f}m)"

def _fmt_lechuga(c: Cultivo) -> str:
    return f"Lechuga(lista_para_cosecha={getattr(c, 'lista_para_cosecha', False)})"

def _fmt_zanahoria(c: Cultivo) -> str:
    return f"Zanahoria(lista_para_cosecha={getattr(c, 'lista_para_cosecha', False)})"

def _fmt_default(x: Cultivo) -> str:
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

# ---------- Helpers de salida bonita ----------
def imprimir_banner():
    print("="*70)
    print(" DEMO: Sistema de Gestión Forestal (modular) ")
    print("="*70)

def imprimir_config():
    print("· Umbrales de riego:")
    print(f"    - Temperatura > {TEMP_UMBRAL_ACTIVA:.1f} °C")
    print(f"    - Humedad     < {HUM_UMBRAL_ACTIVA:.1f} %")
    print("· Sensores (intervalos de lectura):")
    print(f"    - Temperatura: {TEMP_INTERVAL_S:.2f} s")
    print(f"    - Humedad:     {HUM_INTERVAL_S:.2f} s")
    print("· Reglas Strategy (consumos máximos):")
    print(f"    - Árbol (verano/invierno): {ARBOLES_L_VERANO:.1f} L / {ARBOLES_L_INVIERNO:.1f} L")
    print(f"    - Lechuga: {LECHUGA_L:.1f} L | Zanahoria: {ZANAHORIA_L:.1f} L")
    print("-"*70)

def imprimir_resumen_detallado(t: Tierra, p: Plantacion, ctrl: RiegoController):
    reg = CultivoServiceRegistry.instance()
    print("\n📋 RESUMEN DETALLADO")
    print("-"*70)
    print(f"· Tierra: id {t.id_padron_catastral} | superficie {t.superficie_m2:.0f} m² | domicilio: {t.domicilio}")
    print(f"· Plantación: {p.nombre}")
    print(f"· Sensores última lectura → Temperatura: {getattr(ctrl,'_t',0):.1f} °C  |  Humedad: {getattr(ctrl,'_h',0):.1f} %")
    print(f"· Agua disponible (actual): {p.agua_disponible_l:.2f} L")
    print("· Cultivos:")
    if not p.cultivos:
        print("    (sin cultivos)")
    else:
        for i, c in enumerate(p.cultivos, 1):
            print(f"    {i}. {c.nombre:<18} -> {reg.mostrar(c)}")
    print("-"*70)

# ---------- Demo ----------
def demo():
    imprimir_banner()
    imprimir_config()

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

    # Resumen detallado
    imprimir_resumen_detallado(t, p, ctrl)

    # Checklist final
    print("="*70); print("EJEMPLO COMPLETADO EXITOSAMENTE")
    print("[OK] SINGLETON | [OK] FACTORY | [OK] OBSERVER | [OK] STRATEGY")
    print("="*70)

if __name__ == "__main__":
    demo()
