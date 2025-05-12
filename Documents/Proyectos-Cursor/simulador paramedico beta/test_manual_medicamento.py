import unittest
import tkinter as tk
from ventana_manual_medicamento import VentanaManualMedicamento

class TestVentanaManualMedicamento(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def extraer_textos(self, widget):
        textos = []
        for child in widget.winfo_children():
            if isinstance(child, tk.Label) or 'label' in str(type(child)).lower():
                try:
                    textos.append(child.cget('text'))
                except Exception:
                    pass
            textos.extend(self.extraer_textos(child))
        return textos

    def test_renderiza_todos_los_campos(self):
        info = {
            'formula': 'peso x 0.01',
            'unidad': 'mg',
            'rango': '0.1-0.5',
            'adulto': '0.5mg',
            'presentacion': 'ampolla',
            'efectos_secundarios': ['náusea', 'vómito']
        }
        ventana = VentanaManualMedicamento(self.root, "Adrenalina", info)
        textos = self.extraer_textos(ventana)
        self.assertTrue(any("Adrenalina" in t for t in textos))
        self.assertTrue(any("Fórmula dosis" in t for t in textos))
        self.assertTrue(any("Unidad" in t for t in textos))
        self.assertTrue(any("Rango" in t for t in textos))
        self.assertTrue(any("Dosis adulto" in t for t in textos))
        self.assertTrue(any("Presentación" in t for t in textos))
        self.assertTrue(any("Efectos secundarios" in t for t in textos))
        ventana.destroy()

if __name__ == "__main__":
    unittest.main()
