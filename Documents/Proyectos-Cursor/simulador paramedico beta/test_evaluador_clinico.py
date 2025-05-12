import unittest
from unittest.mock import patch
from funciones.evaluador_clinico import evaluador_clinico

class TestEvaluadorClinico(unittest.TestCase):
    def setUp(self):
        # Datos mínimos simulados
        self.signos = {"fc": 110, "spo2": 97, "pa": "120/80"}
        self.historial_meds = [
            {"nombre": "amiodarona", "dosis": 1.0},
            {"nombre": "fentanilo", "dosis": 0.1},
        ]
        self.historial_procs = []
        self.condiciones_activas = []

    @patch.dict('funciones.evaluador_clinico.CONDICIONES', {"qt_largo": {"afecta": "ecg", "duracion": 10}}, clear=True)
    @patch.dict('funciones.evaluador_clinico.medicamentos_als', {}, clear=True)
    def test_combinacion_peligrosa_amiodarona_fentanilo(self):
        condiciones = evaluador_clinico(self.signos, self.historial_meds, self.historial_procs, self.condiciones_activas)
        nombres = [c["nombre"] for c in condiciones]
        self.assertIn("qt_largo", nombres)

    def test_no_condiciones_si_no_hay_combinacion(self):
        historial = [{"nombre": "paracetamol", "dosis": 0.5}]
        condiciones = evaluador_clinico(self.signos, historial, self.historial_procs, self.condiciones_activas)
        self.assertEqual(len(condiciones), 0)

    @patch.dict('funciones.evaluador_clinico.CONDICIONES', {
        "arritmia_taquicardia": {"afecta": "ecg", "duracion": 10, "ecg": "taquicardia"},
        "qt_largo": {"afecta": "ecg", "duracion": 10},
        "arritmia_bradicardia": {"afecta": "ecg", "duracion": 10}
    }, clear=True)
    @patch.dict('funciones.evaluador_clinico.medicamentos_als', {"adrenalina": {"formula": "0.1 * peso"}}, clear=True)
    def test_arritmia_por_sobredosis_adrenalina(self):
        class DummyPaciente:
            peso_kg = 70
        paciente = DummyPaciente()
        historial = [
            {"nombre": "adrenalina", "dosis": "20.0"},  # Dosis muy alta como string
        ]
        condiciones = evaluador_clinico(self.signos, historial, self.historial_procs, self.condiciones_activas, paciente=paciente)
        nombres = [c["nombre"] for c in condiciones]
        self.assertIn("arritmia_taquicardia", nombres)

    @patch.dict('funciones.evaluador_clinico.CONDICIONES', {
        "arritmia_bradicardia": {"afecta": "ecg", "duracion": 10},
        "arritmia_taquicardia": {"afecta": "ecg", "duracion": 10, "ecg": "taquicardia"},
        "qt_largo": {"afecta": "ecg", "duracion": 10}
    }, clear=True)
    @patch.dict('funciones.evaluador_clinico.medicamentos_als', {
        "morfina": {"efectos_secundarios": ["Bradicardia"]}
    }, clear=True)
    def test_condicion_por_efecto_secundario(self):
        historial = [
            {"nombre": "morfina", "dosis": 1.0, "ok": False, "efecto": "Bradicardia"},
        ]
        efecto_a_condicion = {
            "Bradicardia": "arritmia_bradicardia"
        }
        condiciones = evaluador_clinico(self.signos, historial, self.historial_procs, self.condiciones_activas, efecto_a_condicion=efecto_a_condicion)
        nombres = [c["nombre"] for c in condiciones]
        self.assertIn("arritmia_bradicardia", nombres)

if __name__ == "__main__":
    unittest.main()
