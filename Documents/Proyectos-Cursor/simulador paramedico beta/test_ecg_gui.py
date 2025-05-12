import unittest
import tkinter as tk
from ecg.ecg_realtime_gui import ECGRealtimeApp

class TestECGRealtimeApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = ECGRealtimeApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_actualizar_signos_vitales_externos(self):
        # Simula actualización externa de signos vitales
        self.app.actualizar_signos_vitales_externos(88, 97, 110, 36.7)
        self.assertEqual(self.app._signos_pendientes['fc'], 88)
        self.assertEqual(self.app._signos_pendientes['spo2'], 97)
        self.assertEqual(self.app._signos_pendientes['pas'], 110)
        self.assertEqual(self.app._signos_pendientes['temp'], 36.7)

    def test_toggle_alarma(self):
        # Estado inicial: no silenciada
        self.assertFalse(self.app.alarma_silenciada)
        self.app.toggle_alarma()
        self.assertTrue(self.app.alarma_silenciada)
        self.app.toggle_alarma()
        self.assertFalse(self.app.alarma_silenciada)

if __name__ == "__main__":
    unittest.main()
