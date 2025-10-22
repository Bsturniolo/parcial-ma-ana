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
