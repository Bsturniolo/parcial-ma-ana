import unittest
from PythonForestal.patrones.factory.cultivo_factory import CultivoFactory
from PythonForestal.patrones.strategy.absorcion import AbsorcionArbolStrategy, AbsorcionHortalizaStrategy

class TestFactoryStrategy(unittest.TestCase):
    def test_crea_pino_con_estrategia_arbol(self):
        pino = CultivoFactory.crear("pino", "Pino X")
        self.assertIsInstance(pino.estrategia, AbsorcionArbolStrategy)

    def test_crea_lechuga_con_estrategia_hortaliza(self):
        lechuga = CultivoFactory.crear("lechuga", "Lechuga X")
        self.assertIsInstance(lechuga.estrategia, AbsorcionHortalizaStrategy)

    def test_absorcion_arbol_verano_invierno(self):
        s = AbsorcionArbolStrategy()
        self.assertEqual(s.absorber(10, temporada="verano"), 5.0)
        self.assertEqual(s.absorber(10, temporada="invierno"), 2.0)

    def test_absorcion_hortalizas(self):
        h = AbsorcionHortalizaStrategy()
        self.assertEqual(h.absorber(10, cultivo="lechuga"), 1.0)
        self.assertEqual(h.absorber(10, cultivo="zanahoria"), 2.0)

if __name__ == "__main__":
    unittest.main()
