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
