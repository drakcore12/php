import matplotlib.pyplot as plt
from .ecg_generator import generar_ecg_waveform

# Ejemplo de uso: tres estados distintos
def demo_ecg():
    estados = [
        ("normal", 75, "Normal Sinusal"),
        ("taquicardia", 130, "Taquicardia Sinusal"),
        ("asistolia", 0, "Asistolia (Línea Plana)"),
        ("fv", 0, "Fibrilación Ventricular")
    ]
    fig, axs = plt.subplots(len(estados), 1, figsize=(8, 8), sharex=True)
    for ax, (estado, fc, titulo) in zip(axs, estados):
        t, señal = generar_ecg_waveform(estado, fc, duracion=2, fs=250)
        ax.plot(t, señal, lw=2)
        ax.set_title(titulo)
        ax.set_ylabel("ECG")
        ax.grid(True)
    axs[-1].set_xlabel("Tiempo (s)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    demo_ecg()
