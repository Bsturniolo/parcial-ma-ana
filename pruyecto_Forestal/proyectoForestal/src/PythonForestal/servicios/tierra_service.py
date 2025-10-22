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
