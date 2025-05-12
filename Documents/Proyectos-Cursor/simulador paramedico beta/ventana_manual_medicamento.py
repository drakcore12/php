import tkinter as tk
from tkinter import ttk
from utils import mostrar_advertencia, mostrar_error, mostrar_info

class VentanaManualMedicamento(tk.Toplevel):
    """
    Ventana para mostrar el manual de un medicamento, incluyendo fórmula de dosis, unidad, rango, presentación y efectos secundarios.
    """
    def __init__(self, master, nombre_medicamento, info_medicamento):
        """
        Inicializa la ventana de manual de medicamento.
        Args:
            master: ventana padre.
            nombre_medicamento: nombre del medicamento.
            info_medicamento: diccionario con la información del medicamento.
        """
        super().__init__(master)
        self.title(f"Manual: {nombre_medicamento}")
        self.geometry("400x350")
        self.resizable(False, False)
        self.configure(bg="#f4f4f4")

        ttk.Label(self, text=nombre_medicamento, font=("Arial", 15, "bold")).pack(pady=(10,5))
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=18, pady=8)

        ttk.Label(frame, text=f"Fórmula dosis: {info_medicamento.get('formula', '-')}", font=("Arial", 11)).pack(anchor="w", pady=3)
        ttk.Label(frame, text=f"Unidad: {info_medicamento.get('unidad', '-')}", font=("Arial", 11)).pack(anchor="w", pady=3)
        ttk.Label(frame, text=f"Rango: {info_medicamento.get('rango', '-')}", font=("Arial", 11)).pack(anchor="w", pady=3)
        if 'adulto' in info_medicamento:
            ttk.Label(frame, text=f"Dosis adulto: {info_medicamento['adulto']}", font=("Arial", 11)).pack(anchor="w", pady=3)
        if 'presentacion' in info_medicamento:
            ttk.Label(frame, text=f"Presentación: {info_medicamento['presentacion']}", font=("Arial", 11)).pack(anchor="w", pady=3)
        if 'efectos_secundarios' in info_medicamento:
            ttk.Label(frame, text="Efectos secundarios:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10,0))
            for ef in info_medicamento['efectos_secundarios']:
                ttk.Label(frame, text=f"- {ef}", font=("Arial", 10)).pack(anchor="w")
        ttk.Button(self, text="Cerrar", command=self.destroy).pack(pady=15)
