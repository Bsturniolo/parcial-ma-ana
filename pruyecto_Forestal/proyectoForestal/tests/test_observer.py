import unittest
from PythonForestal.patrones.observer.observer import Observable, Observer

class SpyObserver(Observer[int]):
    def __init__(self):
        self.values = []
    def actualizar(self, valor:int)->None:
        self.values.append(valor)

class TestObserverPattern(unittest.TestCase):
    def test_notificar_a_suscriptores(self):
        obs = Observable[int]()
        spy = SpyObserver()
        obs.suscribir(spy)
        obs.notificar(42)
        self.assertEqual(spy.values, [42])

if __name__ == "__main__":
    unittest.main()
