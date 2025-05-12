import tkinter as tk
from tkinter import ttk
from utils import mostrar_advertencia, mostrar_error, mostrar_info

class VentanaHojaClinica(tk.Toplevel):
    """
    Ventana para mostrar la hoja clínica con los datos acumulados y temporizador visual.
    Permite actualizar el contenido y el temporizador desde el exterior.
    """
    def __init__(self, master, datos):
        """
        Inicializa la ventana de hoja clínica.
        Args:
            master: ventana padre.
            datos: diccionario con los datos clínicos a mostrar.
        """
        super().__init__(master)
        self.title("Hoja Clínica - Datos Acumulados")
        self.geometry("500x520")
        self.resizable(True, True)
        self.configure(bg="#f8f8f8")

        ttk.Label(self, text="Hoja Clínica", font=("Arial", 16, "bold")).pack(pady=10)
        self.label_tiempo = ttk.Label(self, text="Tiempo consulta: - s", font=("Arial", 12, "italic"))
        self.label_tiempo.pack(pady=(0,6))
        self._temporizador_activo = False
        self._tiempo_objetivo = None
        self._tiempo_actual = 0
        self.text = tk.Text(self, font=("Consolas", 11), height=25, width=60)
        self.text.pack(padx=12, pady=8, fill=tk.BOTH, expand=True)
        self.tiempo_ultima_consulta = None
        self.actualizar(datos)
        ttk.Button(self, text="Cerrar", command=self.destroy).pack(pady=10)

    def actualizar(self, datos, tiempo_ultima_consulta=None, iniciar_temporizador=None):
        """
        Actualiza el contenido de la hoja clínica y gestiona el temporizador visual.
        Args:
            datos: diccionario con los datos clínicos a mostrar.
            tiempo_ultima_consulta: tiempo final de la consulta (opcional).
            iniciar_temporizador: segundos para iniciar temporizador regresivo (opcional).
        """
        self.text.delete("1.0", tk.END)
        for clave, valor in datos.items():
            if not clave.endswith('_tiempo'):
                self.text.insert(tk.END, f"{clave}: {valor}\n")
        # Gestionar temporizador visual de consulta
        if iniciar_temporizador is not None:
            self._temporizador_activo = True
            self._tiempo_objetivo = iniciar_temporizador
            self._tiempo_actual = iniciar_temporizador
            self._consulta_terminada = False
            self._actualizar_temporizador_regresivo()
        elif tiempo_ultima_consulta is not None:
            # Mostrar el tiempo final si ya terminó
            self._temporizador_activo = False
            self.label_tiempo.config(text=f"Tiempo consulta: {tiempo_ultima_consulta} s")

    def detener_temporizador(self):
        """
        Detiene el temporizador visual de la consulta.
        """
        self._consulta_terminada = True
        self._temporizador_activo = False
        self.label_tiempo.config(text="¡Consulta lista!")

    def _actualizar_temporizador_regresivo(self):
        """
        Actualiza el temporizador regresivo visualmente cada segundo.
        """
        if self._temporizador_activo and self._tiempo_objetivo is not None:
            if hasattr(self, '_consulta_terminada') and self._consulta_terminada:
                self._temporizador_activo = False
                self.label_tiempo.config(text="¡Consulta lista!")
                return
            if self._tiempo_actual > 0:
                self.label_tiempo.config(text=f"Tiempo consulta: {self._tiempo_actual} s")
                self._tiempo_actual -= 1
                self.after(1000, self._actualizar_temporizador_regresivo)
            else:
                self._temporizador_activo = False
                self.label_tiempo.config(text="¡Consulta lista!")
