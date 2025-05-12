# test_ecg.py
# Pruebas unitarias básicas para la lógica de ECG
import unittest
import numpy as np

# Nota: No se importa 'actualizar_ecg' porque es un método de instancia de ECGRealtimeApp.
# Para pruebas de lógica de ECG, importar funciones puras o usar mocks de clase si es necesario.

class TestECG(unittest.TestCase):
    def test_buffer_roll(self):
        """
        Prueba la operación de roll (desplazamiento circular) de numpy, útil para simular buffers de señales.
        """
        arr = np.arange(10)
        rolled = np.roll(arr, -1)
        self.assertTrue(np.array_equal(rolled, [1,2,3,4,5,6,7,8,9,0]))

    # Plantilla: Agrega aquí pruebas para lógica de ECG, filtrado, detección de picos, etc.
    # def test_algo_ecg(self):
    #     ...

if __name__ == "__main__":
    unittest.main()
