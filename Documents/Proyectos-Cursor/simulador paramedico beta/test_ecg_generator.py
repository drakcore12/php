import unittest
import numpy as np
from ecg.ecg_generator import generar_ecg_waveform

class TestECGGenerator(unittest.TestCase):
    def test_generacion_normal(self):
        """
        Debe generar una señal de ECG normal con la estructura esperada.
        """
        t, señal, qrs_pos, interpretacion = generar_ecg_waveform('normal', frecuencia_cardiaca=75, duracion=2, fs=250)
        self.assertEqual(len(t), 500)
        self.assertEqual(len(señal), 500)
        self.assertIsInstance(qrs_pos, list)
        self.assertIsInstance(interpretacion, str)
        self.assertIn('sinusal', interpretacion.lower())

    def test_generacion_taquicardia(self):
        t, señal, qrs_pos, interpretacion = generar_ecg_waveform('taquicardia', frecuencia_cardiaca=150, duracion=2, fs=250)
        self.assertGreaterEqual(np.max(señal), 0.7)  # Mayor actividad
        self.assertIn('taquicardia', interpretacion.lower())

    def test_estado_desconocido(self):
        """
        Debe lanzar ValueError si se pasa un ritmo/arritmia no reconocida.
        """
        with self.assertRaises(ValueError):
            generar_ecg_waveform('desconocido', frecuencia_cardiaca=80, duracion=2, fs=250)

    def test_parametros_fuera_de_rango(self):
        # FC muy baja
        t, señal, qrs_pos, interpretacion = generar_ecg_waveform('normal', frecuencia_cardiaca=10, duracion=2, fs=250)
        self.assertGreaterEqual(np.min(señal), -1.2)
        # FC muy alta
        t, señal, qrs_pos, interpretacion = generar_ecg_waveform('normal', frecuencia_cardiaca=500, duracion=2, fs=250)
        self.assertLessEqual(np.max(señal), 1.2)

if __name__ == "__main__":
    unittest.main()
