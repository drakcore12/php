import tkinter as tk
from tkinter import ttk
from ecg.ecg_generator import generar_ecg_waveform
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import os

from resources import TEXTOS_UI
from utils import mostrar_error, mostrar_info, mostrar_advertencia, setup_logger

setup_logger()

def determinar_estado_ecg(fc, spo2, pas, temp):
    if fc == 0:
        return 'asistolia'
    elif fc > 150:
        return 'taquicardia'
    elif fc < 50:
        return 'bradicardia'
    else:
        return 'normal'

import sys
import threading
import time
try:
    import simpleaudio as sa  # Para reproducir .wav si está disponible
except ImportError:
    sa = None
if sys.platform == 'win32':
    import winsound

class ECGRealtimeApp:
    """
    Aplicación de ECG en tiempo real para el simulador paramédico.
    Visualiza la señal ECG, permite actualizar signos vitales desde el simulador y gestiona alarmas.
    """
    def actualizar_signos_vitales_externos(self, fc, spo2, pas, temp):
        """
        Permite actualizar los signos vitales del ECG desde fuera (ej: simulador).
        Ahora almacena los signos pendientes y los aplica solo al final del ciclo de la onda.
        """
        self._signos_pendientes = {
            'fc': fc,
            'spo2': spo2,
            'pas': pas,
            'temp': temp
        }

    def __init__(self, root, cola_salida=None):
        """
        Inicializa la ventana principal del ECG en tiempo real.
        Args:
            root: ventana raíz de Tkinter.
            cola_salida: cola para recibir signos vitales externos.
        """
        self.root = root
        self.root.title(TEXTOS_UI["titulo_ecg"])
        self.root.geometry('950x650')

        # Variables de entrada
        self.fc_var = tk.DoubleVar(value=75)
        self.spo2_var = tk.DoubleVar(value=98)
        self.pas_var = tk.DoubleVar(value=120)
        self.temp_var = tk.DoubleVar(value=36.5)

        # Inicializar arritmia_var y arritmia_map antes de cualquier update
        self.arritmia_var = tk.StringVar(value='auto')
        self.arritmia_map = {'auto': 'auto'}

        self._build_ui()
        self._init_plot()  # <-- Esto asegura que self.ax y self.line existen antes de usarlos
        # Define estilos para el botón de alarma visualmente
        style = ttk.Style()
        style.configure('AlarmaOn.TButton', background='green', foreground='white')
        style.map('AlarmaOn.TButton', background=[('active', 'green')])
        style.configure('AlarmaOff.TButton', background='red', foreground='white')
        style.map('AlarmaOff.TButton', background=[('active', 'red')])
        self.qrs_last_time = 0
        self.qrs_flash = False
        self.qrs_flash_time = 0
        self.last_qrs_pos = []
        self.alarma_activa = False
        self.alarma_silenciada = False
        self.alarma_thread = None
        # Estado visual del botón de alarma al iniciar
        self.silenciar_btn.config(style='AlarmaOn.TButton')
        self.alarma_stop_event = threading.Event()
        self.desconexion_timer = 0
        self._cola_salida = cola_salida
        self._signos_pendientes = None  # Buffer temporal para signos vitales pendientes
        self.beep_pendiente = False  # <--- NUEVO: beep pendiente de sonar
        if self._cola_salida is not None:
            self._start_consumidor_signos()
        self.root.after(30, self.actualizar_ecg)

    def _start_consumidor_signos(self):
        def consumir():
            while True:
                try:
                    # Si hay backlog, solo tomar el dato más reciente
                    if self._cola_salida is not None and not self._cola_salida.empty():
                        ultimo_signo = None
                        while not self._cola_salida.empty():
                            signos = self._cola_salida.get()
                            ultimo_signo = signos
                        if ultimo_signo is not None:
                            signos_vitales = ultimo_signo.get("signos_vitales", {})
                            # Si hay un segundo nivel de 'signos_vitales', extraerlo
                            if 'signos_vitales' in signos_vitales:
                                signos_vitales = signos_vitales['signos_vitales']
                            # Solo actualizar si el widget sigue existiendo
                            if self.root.winfo_exists():
                                print('[DEBUG][ECG][COLA] Recibido:', signos_vitales)
                                self._signos_pendientes = {
                                    'fc': signos_vitales.get("frecuencia_cardiaca", 75),
                                    'spo2': signos_vitales.get("spo2", 98),
                                    'pas': signos_vitales.get("presion_arterial_sistolica", 120),
                                    'temp': round(signos_vitales.get("temperatura", 36.5), 1)
                                }
                                # Leer arritmia_ecg si está presente
                                self._arritmia_ecg = ultimo_signo.get('arritmia_ecg', None)

                except Exception as e:
                    print("[DEBUG][ECG] Error al consumir cola_salida:", e)
                time.sleep(0.5)
        threading.Thread(target=consumir, daemon=True).start()

    def _build_ui(self):
        frame = ttk.Frame(self.root)
        frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        # (Controles manuales eliminados: solo visualización automática)
        self.estado_label = ttk.Label(frame, text='', font=('Arial', 12, 'bold'))
        self.estado_label.pack(pady=10)
        # Indicador digital de FC
        self.fc_display = ttk.Label(frame, text='FC: 75', font=('Arial', 28, 'bold'), foreground='green')
        self.fc_display.pack(pady=15)
        # Indicador digital de Temperatura
        self.temp_display = ttk.Label(frame, text='Temp: 36,5°C', font=('Arial', 22, 'bold'), foreground='blue')
        self.temp_display.pack(pady=8)
        # Label de interpretación del ritmo
        self.interpret_label = ttk.Label(frame, text='', font=('Arial', 13, 'italic'), foreground='purple')
        self.interpret_label.pack(pady=7)
        # Botón silenciar alarma
        style = ttk.Style()
        style.configure('AlarmaOn.TButton', foreground='black', background='#ffe680', font=('Arial', 11, 'bold'))
        style.configure('AlarmaOff.TButton', foreground='black', background='#cccccc', font=('Arial', 11, 'bold'))
        self.silenciar_btn = ttk.Button(frame, text='Silenciar alarma', command=self.toggle_alarma, style='AlarmaOn.TButton')
        self.silenciar_btn.pack(pady=10)


    def _init_plot(self):
        self.fs = 250  # Frecuencia de muestreo
        self.window_sec = 4  # Ventana visible en segundos
        self.buffer_len = self.fs * self.window_sec
        self.t_buffer = np.linspace(0, self.window_sec, self.buffer_len, endpoint=False)
        self.signal_buffer = np.zeros(self.buffer_len)
        self.fig, self.ax = plt.subplots(figsize=(8,3))
        self.line, = self.ax.plot(self.t_buffer, self.signal_buffer, lw=2)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_xlim(0, self.window_sec)
        self.ax.set_xlabel('Tiempo (s)')
        self.ax.set_ylabel('ECG')
        self.ax.grid(True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.last_estado = None
        self.last_fc = None
        self.last_spo2 = None
        self.last_pas = None
        self.last_temp = None

    def actualizar_ecg(self):
        try:
            fc = self.fc_var.get()
            spo2 = self.spo2_var.get()
            pas = self.pas_var.get()
            temp = round(self.temp_var.get(), 1)
            # --- PROGRESIÓN DE ARRITMIA POR FC EXTREMA ---
            if not hasattr(self, '_fc_extrema_timer'):
                self._fc_extrema_timer = 0
                self._fv_timer = 0
                self._advertencia_extrema = False
                self._progresion_forzada = None
            if fc > 220:
                self._fc_extrema_timer += 1
                if self._fc_extrema_timer > int(15 * 1000 / 30):  # 15 segundos
                    self._advertencia_extrema = True
                    if self._progresion_forzada != 'fv':
                        self._progresion_forzada = 'fv'
                        self._fv_timer = 0
                if self._progresion_forzada == 'fv':
                    self._fv_timer += 1
                    if self._fv_timer > int(10 * 1000 / 30):  # 10 segundos más
                        self._progresion_forzada = 'asistolia'
            else:
                self._fc_extrema_timer = 0
                self._fv_timer = 0
                self._advertencia_extrema = False
                if self._progresion_forzada != 'asistolia':
                    self._progresion_forzada = None
            ritmo_ecg = getattr(self, '_arritmia_ecg', None)
            if self._progresion_forzada:
                ritmo_ecg = self._progresion_forzada
            # --- RESTO DE LA FUNCIÓN ORIGINAL SIGUE ABAJO ---
            # Si hay arritmia activa desde el motor, forzar ese ritmo
            ritmo_ecg = getattr(self, '_arritmia_ecg', None)
            # Si la FC es 0 o hay paro_cardiaco, forzar asistolia
            if fc == 0 or (ritmo_ecg and 'paro' in ritmo_ecg):
                ritmo_ecg = 'asistolia'
            # Mapeo de arritmias recibidas a las válidas para el generador
            arritmia_map = {
                'fibrilacion': 'fv',  # fibrilación ventricular
                'fibrilacion_ventricular': 'fv',
                'fv': 'fv',
                'taquicardia': 'taquicardia',
                'asistolia': 'asistolia',
                'paro_cardiaco': 'asistolia',
                'paro': 'asistolia',
                'bradicardia': 'bradicardia',
                'asistolia': 'asistolia',
                'tv': 'tv',
                'flutter': 'flutter',
                'normal': 'normal',
                'sinusal': 'normal',
                None: None,
                'auto': 'auto',
            }
            if ritmo_ecg is not None and ritmo_ecg != 'auto':
                ritmo_ecg_key = ritmo_ecg.lower()
                estado = arritmia_map.get(ritmo_ecg_key, None)
                if estado is None:
                    # Si recibimos una arritmia no soportada, mostrarlo y graficar asistolia
                    self.estado_label.config(text=f'Arritmia no soportada: {ritmo_ecg_key}')
                    estado = 'asistolia'
                else:
                    # Mostrar advertencia si progresión automática
                    if getattr(self, '_advertencia_extrema', False) and self._progresion_forzada == 'fv':
                        self.estado_label.config(text=f'¡FC extrema! Progresión automática: Fibrilación Ventricular')
                    elif getattr(self, '_progresion_forzada', None) == 'asistolia':
                        self.estado_label.config(text=f'¡Paro cardíaco! Progresión automática: Asistolia')
                    else:
                        self.estado_label.config(text=f'Arritmia activa: {ritmo_ecg_key}')
            else:
                estado = determinar_estado_ecg(fc, spo2, pas, temp)
                if getattr(self, '_advertencia_extrema', False) and self._progresion_forzada == 'fv':
                    self.estado_label.config(text=f'¡FC extrema! Progresión automática: Fibrilación Ventricular')
                elif getattr(self, '_progresion_forzada', None) == 'asistolia':
                    self.estado_label.config(text=f'¡Paro cardíaco! Progresión automática: Asistolia')
                else:
                    self.estado_label.config(text=f'Estado ECG: {estado.capitalize()}')

            # Alarma de desconexión si línea plana mucho tiempo
            if estado == 'asistolia':
                self.desconexion_timer += 1
                if self.desconexion_timer > int(6*1000/30):  # 6 segundos
                    if not self.alarma_silenciada:
                        self.alarma_stop_event.clear()
                        self.alarma_thread = threading.Thread(target=self.sonar_alarma, args=('desconexion',), daemon=True)
                        self.alarma_thread.start()
                        self.alarma_activa = True
            else:
                self.desconexion_timer = 0

            # Alarma visual si estado crítico
            if estado in ('asistolia', 'fv') or fc < 40 or fc > 150 or spo2 < 85:
                self.ax.set_facecolor('#ffeaea')
                self.line.set_color('red')
            else:
                self.ax.set_facecolor('white')
                self.line.set_color('green')

            # Determinar arritmia seleccionada
            arritmia_sel = self.arritmia_map.get(self.arritmia_var.get(), 'auto')
            # Solo regenerar latido base si cambia el tipo de arritmia o el estado (no por cada pequeño cambio de FC)
            if (estado != self.last_estado) or (arritmia_sel != getattr(self, 'last_arritmia', None)):
                self.latido_t, self.latido, self.latido_qrs, interpretacion = generar_ecg_waveform(
                    estado, frecuencia_cardiaca=fc, duracion=1.2, fs=self.fs, arritmia=arritmia_sel)
                # Inicia el índice justo antes del primer QRS si existe, para beep inmediato
                if self.latido_qrs:
                    self.latido_idx = max(0, self.latido_qrs[0] - 1)
                    # Si el primer QRS está en el primer índice, dispara beep inmediato
                    if self.latido_idx + 1 == self.latido_qrs[0]:
                        threading.Thread(target=self.sonar_beep, args=('pip',), daemon=True).start()
                        self.qrs_flash = True
                        self.qrs_flash_time = time.time()
                else:
                    self.latido_idx = 0
                self.last_estado = estado
                self.last_fc = fc
                self.last_arritmia = arritmia_sel
                self.qrs_flash = False
                self.qrs_flash_time = 0
                self.last_qrs_pos = self.latido_qrs
                self.last_qrs_idx = -1
                self.interpret_label.config(text=interpretacion)
                # Dispara beep inmediatamente si el índice inicia en un QRS
                if self.latido_idx in self.latido_qrs:
                    threading.Thread(target=self.sonar_beep, args=('pip',), daemon=True).start()
                    self.qrs_flash = True
                    self.qrs_flash_time = time.time()

            else:
                self.last_fc = fc  # actualizar la FC para el siguiente ciclo

            # Avance dinámico: depende de la FC, pero con límites para que siempre sea visible
            min_points = 5  # Avance más rápido
            # Limita el avance máximo a 1/10 del buffer, para que la onda avance más rápido
            max_points = max(1, int(self.buffer_len / 10))
            base_points = self.fs * 0.008  # base: 8 ms a FC=75 (más rápido que antes)
            points_per_frame = int(base_points * (fc / 75))
            points_per_frame = min(max_points, max(min_points, points_per_frame))

            # Extrae nuevos puntos del latido base
            nuevos = np.zeros(points_per_frame)
            qrs_detectados = []
            prev_idx = self.latido_idx
            for i in range(points_per_frame):
                nuevos[i] = self.latido[self.latido_idx]
                # Detecta QRS (pip y flash FC) aunque se salte el índice exacto, considerando avance cíclico
                for qrs_pos in self.last_qrs_pos:
                    if prev_idx <= qrs_pos < self.latido_idx or \
                       (self.latido_idx < prev_idx and (qrs_pos > prev_idx or qrs_pos < self.latido_idx)):
                        if self.last_qrs_idx != qrs_pos:
                            print(f"[DEBUG][ECG] Detectado QRS en qrs_pos={qrs_pos}, last_qrs_idx={self.last_qrs_idx}")
                            qrs_detectados.append(qrs_pos)
                prev_idx = self.latido_idx
                self.latido_idx += 1
                if self.latido_idx >= len(self.latido):
                    self.latido_idx = 0
                    self.last_qrs_idx = -1  # <-- Reinicia para detectar QRS en cada ciclo
                    # --- Solo aquí actualizamos los signos vitales si hay pendientes ---
                    if self._signos_pendientes is not None:
                        self.fc_var.set(self._signos_pendientes['fc'])

            # --- BEEP SOLO UNA VEZ POR CICLO ---
            if qrs_detectados:
                threading.Thread(target=self.sonar_beep, args=('pip',), daemon=True).start()
                self.qrs_flash = True
                self.qrs_flash_time = time.time()
                # Ahora sí, actualiza last_qrs_idx para evitar múltiples beeps por el mismo QRS
                self.last_qrs_idx = qrs_detectados[-1]


            # Parpadeo FC digital
            if self.qrs_flash and (time.time() - self.qrs_flash_time < 0.12):
                self.fc_display.config(text=f'FC: {int(fc)}', foreground='red')
            else:
                self.fc_display.config(text=f'FC: {int(fc)}', foreground='green')
                self.qrs_flash = False

            # Actualiza la temperatura digital siempre redondeada y con formato xx,x
            self.temp_display.config(text=f'Temp: {temp:.1f}°C')

            # Alarma persistente/intermitente en ritmos críticos
            critico = (estado in ('asistolia', 'fv', 'tv') or fc < 35 or fc > 170 or spo2 < 80)
            # --- FIX: Si la alarma está silenciada, nunca la actives automáticamente ---
            if self.alarma_silenciada:
                if self.alarma_activa:
                    self.alarma_stop_event.set()
                    self.alarma_activa = False
            else:
                if critico and not self.alarma_activa:
                    self.alarma_stop_event.clear()
                    self.alarma_thread = threading.Thread(target=self.sonar_alarma, daemon=True)
                    self.alarma_thread.start()
                    self.alarma_activa = True
                elif not critico and self.alarma_activa:
                    self.alarma_stop_event.set()
                    self.alarma_activa = False

            # Actualiza el buffer (simula desplazamiento)
            self.signal_buffer = np.roll(self.signal_buffer, -points_per_frame)
            self.signal_buffer[-points_per_frame:] = nuevos
            self.line.set_ydata(self.signal_buffer)
            self.ax.figure.canvas.draw_idle()

            # Refresca cada 10 ms para simular la velocidad real de un monitor
            self.root.after(20, self.actualizar_ecg)
            del nuevos  # libera memoria
        except Exception as e:
            import traceback
            print(f"[ERROR][ECG] Excepción no capturada:")
            traceback.print_exc()
            try:
                import tkinter.messagebox as msg
                msg.showerror("Error en ECG", f"{type(e).__name__}: {e}")
            except Exception:
                pass
            # Intenta continuar el ciclo aunque haya error
            self.root.after(1000, self.actualizar_ecg)

    def sonar_beep(self, tipo='pip'):
        # Si la alarma está silenciada, no sonar beep
        if getattr(self, 'alarma_silenciada', False):
            print('[DEBUG][ECG] Beep bloqueado por alarma silenciada')
            return
        if not hasattr(self, '_beep_lock'):
            self._beep_lock = threading.Lock()
        # Llama a simpleaudio.play() directamente, sin threading, y maneja errores
        try:
            beep_path = os.path.join(os.path.dirname(__file__), 'sounds', 'ecg-beep.wav')
            print(f"[DEBUG][ECG] Buscando beep en: {beep_path}")
            if sys.platform == 'win32' and os.path.exists(beep_path):
                print("[DEBUG][ECG] Reproduciendo ecg-beep.wav con winsound.PlaySound")
                winsound.PlaySound(beep_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            elif sa and os.path.exists(beep_path):
                print("[DEBUG][ECG] Reproduciendo ecg-beep.wav con simpleaudio")
                play_obj = sa.WaveObject.from_wave_file(beep_path).play()
                if not hasattr(self, '_beep_refs'):
                    self._beep_refs = []
                self._beep_refs.append(play_obj)
                self._beep_refs = [obj for obj in self._beep_refs if obj.is_playing()]
            else:
                print("[DEBUG][ECG] No se encontró ecg-beep.wav o no hay método compatible disponible")
        except Exception as e:
            print(f"[DEBUG][ECG] Error al reproducir ecg-beep.wav: {e}")
            traceback.print_exc()
            try:
                import tkinter.messagebox as msg
                msg.showerror("Error de audio", f"No se pudo reproducir el beep: {e}")
            except Exception:
                pass





    def sonar_alarma(self, tipo='critico'):
        while not self.alarma_stop_event.is_set():
            if self.alarma_silenciada:
                # INTERRUMPE cualquier sonido en curso
                if sa and hasattr(sa, 'stop_all'):  # Para simpleaudio (si soporta stop_all)
                    try:
                        sa.stop_all()
                    except Exception:
                        pass
                if sys.platform == 'win32':
                    try:
                        winsound.PlaySound(None, winsound.SND_PURGE)
                    except Exception:
                        pass
                break
            if sa:
                try:
                    if tipo == 'desconexion':
                        sa.WaveObject.from_wave_file('desconexion.wav').play()
                    else:
                        sa.WaveObject.from_wave_file('alarm.wav').play()
                except Exception as e:
                    print(f"[DEBUG][ECG] Error al reproducir alarma: {e}")
            elif sys.platform == 'win32':
                winsound.Beep(1000, 300)
            # Espera entre alarmas
            time.sleep(1 if tipo == 'critico' else 2)

        self.qrs_flash = False

        # INTERRUMPE cualquier sonido en curso al salir
        if sa and hasattr(sa, 'stop_all'):
            try:
                sa.stop_all()
            except Exception:
                pass
        if sys.platform == 'win32':
            try:
                winsound.PlaySound(None, winsound.SND_PURGE)
            except Exception:
                pass

        self.alarma_stop_event.set()
        self.alarma_activa = False

    def toggle_alarma(self):
        '''
        Activa o silencia la alarma manualmente.
        '''
        self.alarma_silenciada = not self.alarma_silenciada
        def update_btn():
            if self.alarma_silenciada:
                self.alarma_stop_event.set()
                self.alarma_activa = False
                self.silenciar_btn.config(style='AlarmaOff.TButton', text='Activar alarma')
            else:
                self.alarma_stop_event.clear()
                if not self.alarma_activa:
                    self.alarma_thread = threading.Thread(target=self.sonar_alarma, daemon=True)
                    self.alarma_thread.start()
                    self.alarma_activa = True
                self.silenciar_btn.config(style='AlarmaOn.TButton', text='Silenciar alarma')
            print(f"[DEBUG][ECG][ALARMA] Silenciada: {self.alarma_silenciada}")
        self.root.after_idle(update_btn)


import sys
import traceback

def global_exception_handler(exc_type, exc_value, exc_traceback):
    print("\n[ERROR][ECG] Excepción no capturada:")
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    try:
        import tkinter.messagebox as msg
        msg.showerror("Error crítico", f"{exc_type.__name__}: {exc_value}")
    except Exception:
        pass

sys.excepthook = global_exception_handler

if __name__ == '__main__':
    root = tk.Tk()
    app = ECGRealtimeApp(root)
    app.alarma_silenciada = False
    root.mainloop()
