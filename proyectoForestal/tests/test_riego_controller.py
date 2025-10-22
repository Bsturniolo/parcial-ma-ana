import unittest
from PythonForestal.riego.control.riego_controller import RiegoController

class DummySvc:
    def __init__(self):
        self.calls = []
    def regar_todos(self, litros_por_cultivo:float, temporada:str="verano"):
        self.calls.append((litros_por_cultivo, temporada))

class TestRiegoController(unittest.TestCase):
    def test_activa_por_temperatura_alta(self):
        svc = DummySvc()
        ctrl = RiegoController(svc)
        ctrl.actualizar(31.0)  # temperatura
        self.assertTrue(len(svc.calls) >= 1)

    def test_activa_por_humedad_baja(self):
        svc = DummySvc()
        ctrl = RiegoController(svc)
        ctrl.actualizar(35.0)  # humedad %
        self.assertTrue(len(svc.calls) >= 1)

if __name__ == "__main__":
    unittest.main()
