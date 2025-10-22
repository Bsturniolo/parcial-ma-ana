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
