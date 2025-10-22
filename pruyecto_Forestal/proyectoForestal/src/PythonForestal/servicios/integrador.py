"""
Archivo integrador generado automaticamente
Directorio: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/servicios
Fecha: 2025-10-22 00:37:36
Total de archivos integrados: 5
"""

# ================================================================================
# ARCHIVO 1/5: __init__.py
# Ruta: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/servicios/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/5: persist_exceptions.py
# Ruta: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/servicios/persist_exceptions.py
# ================================================================================

class PersistenciaException(Exception):
    def __init__(self, mensaje: str, nombre_archivo: str = "", operacion: str = ""):
        super().__init__(mensaje)
        self._mensaje = mensaje
        self._nombre = nombre_archivo
        self._op = operacion
    def get_user_message(self) -> str: return self._mensaje
    def get_nombre_archivo(self) -> str: return self._nombre
    def get_tipo_operacion(self) -> str: return self._op


# ================================================================================
# ARCHIVO 3/5: plantacion_service.py
# Ruta: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/servicios/plantacion_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 4/5: registro_service.py
# Ruta: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/servicios/registro_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 5/5: tierra_service.py
# Ruta: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/servicios/tierra_service.py
# ================================================================================

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


