import unittest
from unittest.mock import patch, MagicMock
import sys
import tkinter as tk

# Importar las ventanas a testear
glob = sys.modules.get('__main__', None)
if glob is not None:
    # Para evitar problemas de import circular en ejecución directa
    from ventana_dosis_medicamento import VentanaDosisMedicamento
    from ventana_manual_medicamento import VentanaManualMedicamento
else:
    from .ventana_dosis_medicamento import VentanaDosisMedicamento
    from .ventana_manual_medicamento import VentanaManualMedicamento

class TestVentanaDosisMedicamento(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Oculta ventana principal

    def tearDown(self):
        self.root.destroy()

    @patch('ventana_dosis_medicamento.mostrar_advertencia')
    def test_aplicar_dosis_campos_incompletos(self, mock_advertencia):
        """Debe mostrar advertencia si algún campo está vacío."""
        ventana = VentanaDosisMedicamento(self.root, "Adrenalina", lambda *a: None)
        ventana.entry_dosis.delete(0, 'end')
        ventana.combo_unidad.set('')
        ventana.combo_via.set('')
        ventana.aplicar_dosis()
        mock_advertencia.assert_called_once_with("Por favor completa todos los campos.", "Campos incompletos")
        ventana.destroy()

    @patch('ventana_dosis_medicamento.mostrar_advertencia')
    def test_aplicar_dosis_datos_validos(self, mock_advertencia):
        """No debe mostrar advertencia si todos los campos son válidos."""
        callback = MagicMock()
        ventana = VentanaDosisMedicamento(self.root, "Adrenalina", callback)
        ventana.entry_dosis.insert(0, '1.0')
        ventana.combo_unidad.set('mg')
        ventana.combo_via.set('IV')
        ventana.aplicar_dosis()
        mock_advertencia.assert_not_called()
        callback.assert_called_once()
        ventana.destroy()

    @patch('ventana_dosis_medicamento.mostrar_advertencia')
    def test_flujo_completo_usuario_dosis(self, mock_advertencia):
        """
        Test de integración: simula el flujo completo de usuario en VentanaDosisMedicamento.
        - Ingresar datos válidos: callback recibe los datos correctos y no hay advertencia.
        - Ingresar datos inválidos: se muestra advertencia y no se llama al callback.
        """
        # Caso válido
        callback = MagicMock()
        ventana = VentanaDosisMedicamento(self.root, "Adrenalina", callback)
        ventana.entry_dosis.insert(0, '2.5')
        ventana.combo_unidad.set('mg')
        ventana.combo_via.set('IM')
        ventana.aplicar_dosis()
        mock_advertencia.assert_not_called()
        callback.assert_called_once_with("Adrenalina", "2.5", "mg", "IM")
        ventana.destroy()
        # Caso inválido (vacío)
        callback2 = MagicMock()
        ventana2 = VentanaDosisMedicamento(self.root, "Adrenalina", callback2)
        ventana2.entry_dosis.delete(0, 'end')
        ventana2.combo_unidad.set('')
        ventana2.combo_via.set('')
        ventana2.aplicar_dosis()
        mock_advertencia.assert_called_with("Por favor completa todos los campos.", "Campos incompletos")
        callback2.assert_not_called()
        ventana2.destroy()

class TestVentanaManualMedicamento(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_manual_medicamento_renderiza_info(self):
        info = {
            'formula': 'peso x 0.01',
            'unidad': 'mg',
            'rango': '0.1-0.5',
            'adulto': '0.5mg',
            'presentacion': 'ampolla',
            'efectos_secundarios': ['náusea', 'vómito']
        }
        ventana = VentanaManualMedicamento(self.root, "Adrenalina", info)
        # Buscar que los labels existan (test superficial de render)
        from tkinter.ttk import Button as TtkButton
        children = ventana.winfo_children()
        self.assertTrue(any(isinstance(w, (tk.Button, TtkButton)) for w in children))
        ventana.destroy()

if __name__ == "__main__":
    unittest.main()
