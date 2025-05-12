import unittest
from unittest.mock import MagicMock
import tkinter as tk
from ventana_hoja_clinica import VentanaHojaClinica

class TestVentanaHojaClinica(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_actualizar_muestra_datos(self):
        datos = {'diagnostico': 'Infarto', 'glucosa': 120, 'glucosa_tiempo': 5}
        ventana = VentanaHojaClinica(self.root, datos)
        contenido = ventana.text.get('1.0', 'end')
        self.assertIn('diagnostico: Infarto', contenido)
        self.assertIn('glucosa: 120', contenido)
        self.assertNotIn('glucosa_tiempo', contenido)  # No debe mostrar claves _tiempo
        ventana.destroy()

    def test_temporizador_visual(self):
        datos = {'diagnostico': 'Arritmia'}
        ventana = VentanaHojaClinica(self.root, datos)
        ventana.actualizar(datos, iniciar_temporizador=2)
        self.assertTrue(ventana._temporizador_activo)
        ventana.detener_temporizador()
        self.assertFalse(ventana._temporizador_activo)
        ventana.destroy()

if __name__ == "__main__":
    unittest.main()
