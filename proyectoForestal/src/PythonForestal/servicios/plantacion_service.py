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
