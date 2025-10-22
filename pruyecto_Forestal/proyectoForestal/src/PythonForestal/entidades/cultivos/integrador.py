"""
Archivo integrador generado automaticamente
Directorio: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/entidades/cultivos
Fecha: 2025-10-22 00:37:36
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/entidades/cultivos/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: cultivos.py
# Ruta: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/entidades/cultivos/cultivos.py
# ================================================================================

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


