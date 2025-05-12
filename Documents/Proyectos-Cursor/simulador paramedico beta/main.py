# Simulador Médico - Proyecto Base

import tkinter as tk
from clases.paciente import Paciente

class SimuladorMedicoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Médico - Proyecto Base")
        self.root.geometry("600x400")
        label = tk.Label(root, text="¡Bienvenido al Simulador Médico!", font=("Arial", 18))
        label.pack(pady=60)
        self.info = tk.Label(root, text="Aquí inicia tu nuevo proyecto", font=("Arial", 12))
        self.info.pack(pady=20)

if __name__ == "__main__":
    paciente_demo = Paciente(
        nombre="María Pérez",
        edad=45,
        sexo='F',
        peso=65,
        altura=165,
        actividad_fisica='media',
        estado_nutricional='normal',
        composicion={"grasa": 25, "musculo": 35, "agua": 48}
    )
    print("Paciente generado procedimentalmente:")
    print(paciente_demo)
    print("Signos vitales:")
    print(paciente_demo.signos_vitales)
    print("Factores ambientales:")
    print(paciente_demo.factores_ambientales)
    root = tk.Tk()
    app = SimuladorMedicoApp(root)
    root.mainloop()
