"""
Archivo integrador generado automaticamente
Directorio: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/patrones/factory
Fecha: 2025-10-22 00:37:36
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/patrones/factory/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: cultivo_factory.py
# Ruta: /home/bautista/Escritorio/pruyecto_Forestal/proyectoForestal/python_forestacion/patrones/factory/cultivo_factory.py
# ================================================================================

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


