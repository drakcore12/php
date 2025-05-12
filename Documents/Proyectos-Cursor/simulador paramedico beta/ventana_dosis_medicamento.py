import tkinter as tk
from tkinter import ttk
from utils import mostrar_advertencia

class VentanaDosisMedicamento(tk.Toplevel):
    """
    Ventana para aplicar dosis de medicamento. Permite ingresar dosis, unidad y vía de administración.
    """
    def __init__(self, master, nombre_medicamento, callback_aplicar):
        """
        Inicializa la ventana de dosis de medicamento.
        Args:
            master: ventana padre.
            nombre_medicamento: nombre del medicamento a administrar.
            callback_aplicar: función callback para aplicar la dosis.
        """
        super().__init__(master)
        self.title(f"Aplicar dosis: {nombre_medicamento}")
        self.geometry("350x250")
        self.resizable(False, False)
        self.nombre_medicamento = nombre_medicamento
        self.callback_aplicar = callback_aplicar
        self.configure(bg="#f4f4f4")

        ttk.Label(self, text=f"{nombre_medicamento}", font=("Arial", 16, "bold")).pack(pady=(15,5))

        frame = ttk.Frame(self)
        frame.pack(pady=10, padx=15, fill=tk.X)

        ttk.Label(frame, text="Dosis:").grid(row=0, column=0, sticky="w", pady=4)
        self.entry_dosis = ttk.Entry(frame)
        self.entry_dosis.grid(row=0, column=1, pady=4)

        ttk.Label(frame, text="Unidad:").grid(row=1, column=0, sticky="w", pady=4)
        self.combo_unidad = ttk.Combobox(frame, values=["mg", "mcg", "g", "UI", "ml", "gotas", "tabletas", "ampollas"])
        self.combo_unidad.grid(row=1, column=1, pady=4)
        self.combo_unidad.current(0)

        ttk.Label(frame, text="Vía:").grid(row=2, column=0, sticky="w", pady=4)
        self.combo_via = ttk.Combobox(frame, values=["IV", "IM", "SC", "SL", "IN", "Oral", "Inhalatoria"])
        self.combo_via.grid(row=2, column=1, pady=4)
        self.combo_via.current(0)

        ttk.Button(self, text="Aplicar", command=self.aplicar_dosis).pack(pady=18)

    def aplicar_dosis(self):
        """
        Valida los campos y llama al callback para aplicar la dosis.
        """
        dosis = self.entry_dosis.get()
        unidad = self.combo_unidad.get()
        via = self.combo_via.get()
        if not dosis or not unidad or not via:
            mostrar_advertencia("Por favor completa todos los campos.", "Campos incompletos")
            return
        self.callback_aplicar(self.nombre_medicamento, dosis, unidad, via)
        self.destroy()
