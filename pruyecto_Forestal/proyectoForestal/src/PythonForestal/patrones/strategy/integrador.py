"""
Archivo integrador generado automaticamente
Directorio: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/patrones/strategy
Fecha: 2025-10-22 00:37:36
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/patrones/strategy/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: absorcion.py
# Ruta: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/patrones/strategy/absorcion.py
# ================================================================================

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


