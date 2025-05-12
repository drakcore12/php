import unittest
from clases.paciente import Paciente

class TestPaciente(unittest.TestCase):
    def test_instanciacion_basica(self):
        p = Paciente(
            nombre="Juan",
            edad=30,
            sexo="M",
            peso=80,
            altura=180,
            actividad_fisica="moderada",
            estado_nutricional="normal",
            composicion="musculoso",
            condicion="sano",
            grupo_etario="adulto",
            factores_ambientales="urbano",
            signos_vitales={"fc": 70, "spo2": 98}
        )
        self.assertEqual(p.nombre, "Juan")
        self.assertEqual(p.edad, 30)
        self.assertEqual(p.sexo, "M")
        self.assertEqual(p.peso_kg, 80)
        self.assertEqual(p.altura_cm, 180)
        self.assertEqual(p.signos_vitales["fc"], 70)

    def test_repr(self):
        p = Paciente(
            nombre="Ana",
            edad=25,
            sexo="F",
            peso=60,
            altura=165,
            actividad_fisica="baja",
            estado_nutricional="delgada",
            composicion="delgada",
            condicion="sana",
            grupo_etario="adulto",
            factores_ambientales="rural",
            signos_vitales={"fc": 80, "spo2": 99}
        )
        r = repr(p)
        self.assertIn("Ana", r)
        self.assertIn("25a", r)
        self.assertIn("F", r)
        self.assertIn("60", r)
        self.assertIn("165", r)
        self.assertIn("Signos", r)

    def test_generar_nombre_aleatorio(self):
        nombre_m = Paciente.generar_nombre_aleatorio("M")
        nombre_f = Paciente.generar_nombre_aleatorio("F")
        self.assertIsInstance(nombre_m, str)
        self.assertIsInstance(nombre_f, str)
        self.assertNotEqual(nombre_m, "")
        self.assertNotEqual(nombre_f, "")

    def test_generar_aleatorio(self):
        p = Paciente.generar_aleatorio()
        self.assertIsInstance(p, Paciente)
        self.assertTrue(0 <= p.edad <= 90)
        self.assertIn(p.sexo, ["M", "F"])
        self.assertIsInstance(p.signos_vitales, dict)

if __name__ == "__main__":
    unittest.main()
