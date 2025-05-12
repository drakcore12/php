import tkinter as tk
from tkinter import ttk
import threading
import queue
import time
from funciones.consulta_paciente import consulta_paciente
from clases.paciente import Paciente
from simulacion.simulador_signos import MotorSimulacion
from resources import TEXTOS_UI
from utils import mostrar_error, mostrar_info, mostrar_advertencia, setup_logger

setup_logger()

def formatear_signos(signos):
    return (f"FC: {signos.get('frecuencia_cardiaca', '-')}, "
            f"FR: {signos.get('frecuencia_respiratoria', '-')}, "
            f"PA: {signos.get('presion_arterial_sistolica', '-')}/"
            f"{signos.get('presion_arterial_diastolica', '-')}, "
            f"SpO2: {signos.get('spo2', '-')}, "
            f"Temp: {signos.get('temperatura', '-')}")

class AppSimulador(tk.Tk):
    """
    Ventana principal del simulador paramédico. Gestiona la UI, los eventos principales y la integración con el motor de simulación.
    """
    def __init__(self):
        """
        Inicializa la ventana principal y todos los widgets de la interfaz.
        """
        super().__init__()
        self.title(TEXTOS_UI.get("titulo_dashboard", "Simulador Paramedico - Dashboard Clínico"))
        self.geometry("1100x600")
        self.configure(bg="#222")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # --- TOP: Contexto del Escenario + Botón ---
        self.frame_top = ttk.Frame(self)
        self.frame_top.pack(side=tk.TOP, fill=tk.X, pady=(10,0))
        self.label_escenario = ttk.Label(self.frame_top, text=TEXTOS_UI.get("contexto_escenario", "[Contexto del Escenario]"), font=("Arial", 20, "bold"), anchor="center")
        self.label_escenario.pack(fill=tk.X, padx=10)
        # Label de tiempo de simulación
        self.var_tiempo = tk.StringVar(value="0:00")
        self.label_tiempo = ttk.Label(self.frame_top, textvariable=self.var_tiempo, font=("Arial", 16, "bold"), foreground="#0a0")
        self.label_tiempo.pack(pady=(0,5))
        self.btn_iniciar = ttk.Button(self.frame_top, text=TEXTOS_UI.get("btn_iniciar", "Iniciar Simulación"), command=self.iniciar_simulacion)
        self.btn_iniciar.pack(pady=8)

        # --- LEFT: Signos Vitales ---
        self.frame_left = ttk.Frame(self)
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=(15,5), pady=10)
        ttk.Label(self.frame_left, text="Signos Vitales", font=("Arial", 16, "bold")).pack(pady=(0,15))
        self.vars_signos = {}
        for nombre in ["FC", "FR", "PA Sistólica", "PA Diastólica", "SpO₂", "Temperatura"]:
            f = ttk.Frame(self.frame_left)
            f.pack(anchor="w", pady=4)
            ttk.Label(f, text=nombre+":", font=("Arial", 13)).pack(side=tk.LEFT)
            var = tk.StringVar(value="-")
            self.vars_signos[nombre] = var
            ttk.Label(f, textvariable=var, font=("Arial", 13, "bold")).pack(side=tk.LEFT, padx=8)

        # --- CENTER: Indicador gráfico de volumen sanguíneo ---
        self.frame_center = ttk.Frame(self, relief=tk.RIDGE)
        self.frame_center.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        ttk.Label(self.frame_center, text="Volumen Sanguíneo", font=("Arial", 15, "bold")).pack(pady=(10,0))
        self.canvas_vol = tk.Canvas(self.frame_center, width=120, height=270, bg='white', highlightthickness=0)
        self.canvas_vol.pack(pady=18)
        # Dibuja el glow (resplandor) detrás del tubo
        self.vol_glow = self.canvas_vol.create_rectangle(32, 25, 88, 245, fill='', outline='', width=0)
        # Dibuja el tubo
        self.tubo_rect = self.canvas_vol.create_rectangle(35, 28, 85, 242, outline='black', width=4)
        self.vol_fill = self.canvas_vol.create_rectangle(37, 240, 83, 240, fill='#c62828', width=0)
        self.vol_text = self.canvas_vol.create_text(60, 250, text='', font=("Arial", 13, "bold"), anchor='n')
        # Inicializa valores
        self.volumen_total = None
        self.volumen_actual = None
        self.volumen_pct = None
        self.volumen_anim = None  # Para animación suave
        self.actualizar_tubo_volumen(5000, 5000)  # Valor inicial

    def actualizar_tubo_volumen(self, volumen_actual, volumen_total):
        # Calcula porcentaje
        pct = max(0, min(1, volumen_actual / volumen_total)) if volumen_total > 0 else 0
        # Animación suave: si cambia mucho, interpolar
        if self.volumen_anim is None:
            self.volumen_anim = pct
        else:
            if abs(self.volumen_anim - pct) > 0.01:
                paso = (pct - self.volumen_anim) * 0.2
                self.volumen_anim += paso
                self.after(30, lambda: self.actualizar_tubo_volumen(self.volumen_anim * volumen_total, volumen_total))
                return
            else:
                self.volumen_anim = pct
        # Coordenadas visuales
        y_top = 30 + (1 - self.volumen_anim) * 210
        y_bot = 240
        # Color gradiente sangre
        if self.volumen_anim > 0.2:
            color = '#c62828'
        elif self.volumen_anim > 0.05:
            color = '#ff9800'
        else:
            color = '#bdbdbd'
        # Glow crítico
        if self.volumen_anim <= 0.05:
            self.canvas_vol.itemconfig(self.vol_glow, fill='#ff1744', stipple='gray25')
        elif self.volumen_anim <= 0.2:
            self.canvas_vol.itemconfig(self.vol_glow, fill='#ff9800', stipple='gray50')
        else:
            self.canvas_vol.itemconfig(self.vol_glow, fill='', stipple='')
        # Actualiza el fill
        self.canvas_vol.coords(self.vol_fill, 37, y_top, 83, y_bot)
        self.canvas_vol.itemconfig(self.vol_fill, fill=color)
        # Texto destacado y claro
        self.canvas_vol.itemconfig(self.vol_text, text=f"{int(volumen_actual)} mL\n({int(100*self.volumen_anim)}%)", fill='#222' if self.volumen_anim > 0.2 else '#fff')
        # Limitar el volumen_actual al máximo del volumen_total inicial
        if self.volumen_total is not None and volumen_actual > self.volumen_total:
            volumen_actual = self.volumen_total
        self.volumen_total = volumen_total
        self.volumen_actual = volumen_actual
        self.volumen_pct = self.volumen_anim


        # --- RIGHT: Pestañas ---
        self.frame_right = ttk.Frame(self)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.Y, padx=(5,15), pady=10)
        self.notebook = ttk.Notebook(self.frame_right)
        self.notebook.pack(expand=True, fill=tk.BOTH)
        # Medicamentos
        # Evitar duplicación de la sección de medicamentos
        if not hasattr(self, 'tab_meds'):
            self.tab_meds = ttk.Frame(self.notebook)
            self.notebook.add(self.tab_meds, text="Medicamentos")
            ttk.Label(self.tab_meds, text="Lista de medicamentos", font=("Arial", 13)).pack(pady=8)
            # --- Scrollable Frame para medicamentos ---
            meds_canvas = tk.Canvas(self.tab_meds, height=360)
            meds_scrollbar = ttk.Scrollbar(self.tab_meds, orient="vertical", command=meds_canvas.yview)
            meds_scrollable_frame = ttk.Frame(meds_canvas)
            meds_scrollable_frame.bind(
                "<Configure>", lambda e: meds_canvas.configure(scrollregion=meds_canvas.bbox("all"))
            )
            meds_canvas.create_window((0, 0), window=meds_scrollable_frame, anchor="nw")
            meds_canvas.configure(yscrollcommand=meds_scrollbar.set)
            meds_canvas.pack(side="left", fill="both", expand=True, padx=(0,0), pady=(0,10))
            meds_scrollbar.pack(side="right", fill="y", pady=(0,10))
            # Botones de todos los medicamentos ALS
            from datos.datos_diccionarios import medicamentos_als
            self.btn_meds = []
            for clave, info in medicamentos_als.items():
                frame_med = ttk.Frame(meds_scrollable_frame)
                frame_med.pack(fill=tk.X, padx=10, pady=2)
                btn_dosis = ttk.Button(frame_med, text=f"Aplicar {info['nombre']}", width=22, command=lambda k=clave: self.abrir_ventana_dosis(k))
                btn_dosis.pack(side=tk.LEFT)
                btn_manual = ttk.Button(frame_med, text="Manual", width=8, command=lambda k=clave: self.abrir_ventana_manual(k))
                btn_manual.pack(side=tk.LEFT, padx=8)
                self.btn_meds.append((btn_dosis, btn_manual))
        # Procedimientos
        self.tab_proc = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_proc, text="Procedimientos")
        ttk.Label(self.tab_proc, text="Lista de procedimientos", font=("Arial", 13)).pack(pady=8)
        ttk.Checkbutton(self.tab_proc, text="Canalización").pack(anchor="w", padx=10)
        ttk.Checkbutton(self.tab_proc, text="Vendaje compresivo").pack(anchor="w", padx=10)
        ttk.Button(self.tab_proc, text="Aplicar").pack(pady=12)
        # Exámenes
        self.tab_exam = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_exam, text="Exámenes")
        ttk.Label(self.tab_exam, text="Lista de exámenes", font=("Arial", 13)).pack(pady=8)
        ttk.Label(self.tab_exam, text="Haz clic en un examen para consultar el resultado clínico del paciente.", font=("Arial", 10, "italic"), foreground="#0077b6").pack(pady=(0,8))
        # --- Scrollable Frame para exámenes ---
        exam_canvas = tk.Canvas(self.tab_exam, bg="#222", highlightthickness=0, borderwidth=0, height=340)
        exam_scrollbar = ttk.Scrollbar(self.tab_exam, orient="vertical", command=exam_canvas.yview)
        exam_scrollable_frame = ttk.Frame(exam_canvas)
        exam_scrollable_frame.bind(
            "<Configure>", lambda e: exam_canvas.configure(scrollregion=exam_canvas.bbox("all"))
        )
        exam_canvas.create_window((0, 0), window=exam_scrollable_frame, anchor="nw")
        exam_canvas.configure(yscrollcommand=exam_scrollbar.set)
        exam_canvas.pack(side="left", fill="both", expand=True, padx=(0,0), pady=(0,10))
        exam_scrollbar.pack(side="right", fill="y", pady=(0,10))
        # --- Botones de exámenes ---
        self.examenes_disponibles = [
            ("🩸 Glucosa capilar", "glucosa"),
            ("🫁 Gasometría arterial", "gasometria"),
            ("❤️ Frecuencia cardíaca", "frecuencia_cardiaca"),
            ("🩺 Presión arterial", "presion_arterial"),
            ("🌡️ Temperatura", "temperatura"),
            ("🫀 SpO₂", "spo2"),
            ("⚖️ Peso", "peso"),
            ("📏 Talla", "talla"),
            ("🎂 Edad", "edad"),
            ("🏃 Estado físico", "estado_fisico"),
        ]
        self.datos_hoja_clinica = {}
        for nombre, clave in self.examenes_disponibles:
            btn = ttk.Button(exam_scrollable_frame, text=nombre, width=28, command=lambda c=clave, n=nombre: self.solicitar_examen(c, n), style="Examen.TButton")
            btn.pack(anchor="w", padx=16, pady=4)
        # --- Botón ECG ---
        btn_ecg = ttk.Button(exam_scrollable_frame, text="🩺 ECG en tiempo real", width=28, command=self.abrir_ventana_ecg, style="Examen.TButton")
        btn_ecg.pack(anchor="w", padx=16, pady=14)
        # --- Estilo personalizado para los botones de examen ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Examen.TButton", font=("Arial", 13, "bold"), foreground="#ffffff", background="#1565c0", padding=6)
        style.map("Examen.TButton",
                  foreground=[('active', '#ffffff')],
                  background=[('active', '#1976d2')])
        exam_canvas.configure(bg="#222")

        # --- Estado de simulación (inicialmente vacío) ---
        self.cola_salida_dashboard = queue.Queue()
        self.cola_salida_ecg = None
        self.cola_entrada = None
        self.tiempo_simulacion = 0  # segundos transcurridos
        self.actualizando_tiempo = False
        self.paciente = None
        self.motor = None

        self.after(1000, self.actualizar_signos)

    def actualizar_signos(self):
        print("[DEBUG][GUI] Tick de actualización de signos")
        if self.cola_salida_dashboard:
            print(f"[DEBUG][GUI] Leyendo cola_salida_dashboard id={id(self.cola_salida_dashboard)}")
            while not self.cola_salida_dashboard.empty():
                signos = self.cola_salida_dashboard.get()
                print(f"[DEBUG][GUI] Recibido desde cola_salida_dashboard id={id(self.cola_salida_dashboard)}: {signos}")
                # Extraer el subdiccionario de signos vitales
                signos_vitales = signos.get("signos_vitales", {})
                # Si hay un segundo nivel de 'signos_vitales', extraerlo
                if 'signos_vitales' in signos_vitales:
                    signos_vitales = signos_vitales['signos_vitales']
                self.vars_signos["FC"].set(signos_vitales.get("frecuencia_cardiaca", "-"))
                self.vars_signos["FR"].set(signos_vitales.get("frecuencia_respiratoria", "-"))
                self.vars_signos["PA Sistólica"].set(signos_vitales.get("presion_arterial_sistolica", "-"))
                self.vars_signos["PA Diastólica"].set(signos_vitales.get("presion_arterial_diastolica", "-"))
                self.vars_signos["SpO₂"].set(signos_vitales.get("spo2", "-"))
                temp = signos_vitales.get("temperatura", "-")
                if isinstance(temp, (float, int)):
                    temp_str = f"{temp:.1f}".replace('.', ',')
                else:
                    temp_str = temp
                self.vars_signos["Temperatura"].set(temp_str)

                # Actualizar indicador gráfico de volumen sanguíneo
                volumen_actual = signos_vitales.get('volumen_sanguineo', None)
                if volumen_actual is not None:
                    # Intentar estimar volumen total del paciente si aún no está
                    if self.volumen_total is None or self.volumen_total < volumen_actual:
                        peso = getattr(self.paciente, 'peso_kg', 70) if self.paciente else 70
                        edad = getattr(self.paciente, 'edad', 30) if self.paciente else 30
                        sexo = getattr(self.paciente, 'sexo', 'M') if self.paciente else 'M'
                        # Fórmula simple: adulto ~70 mL/kg, niños ~75 mL/kg
                        if edad < 1:
                            ml_kg = 85
                        elif edad < 2:
                            ml_kg = 78
                        elif edad < 12:
                            ml_kg = 73
                        elif edad < 18:
                            ml_kg = 72 if sexo == 'M' else 68
                        else:
                            ml_kg = 72 if sexo == 'M' else 68
                        self.volumen_total = round(peso * ml_kg, 1)
                    self.actualizar_tubo_volumen(volumen_actual, self.volumen_total)
                # --- Si la ventana de ECG está abierta, pasarle los valores ---
                if getattr(self, 'ventana_ecg', None) is not None and self.ventana_ecg.winfo_exists() and hasattr(self, 'ecg_app') and self.ecg_app is not None:
                    try:
                        self.ecg_app.actualizar_signos_vitales_externos(
                            signos_vitales.get("frecuencia_cardiaca", 75),
                            signos_vitales.get("spo2", 98),
                            signos_vitales.get("presion_arterial_sistolica", 120),
                            signos_vitales.get("temperatura", 36.5)
                        )
                    except Exception as e:
                        print("[DEBUG][ECG] No se pudo actualizar ECG:", e)
        # Actualizar tiempo de simulación si está corriendo
        if self.actualizando_tiempo:
            self.tiempo_simulacion += 1
            minutos = self.tiempo_simulacion // 60
            segundos = self.tiempo_simulacion % 60
            self.var_tiempo.set(f"{minutos}:{segundos:02d}")
            # Actualiza el temporizador en la hoja clínica si está abierta

        self.after(1000, self.actualizar_signos)

    def admin_medicamento(self):
        evento = {
            'tipo': 'medicamento',
            'nombre': 'vasopresores',
            'efecto': {'fc': 3, 'pa_sys': 5, 'pa_dia': 3},
            'duracion_restante': 30
        }
        self.cola_entrada.put(evento)
        self.btn_medicamento.config(state=tk.DISABLED)
        self.after(35000, lambda: self.btn_medicamento.config(state=tk.NORMAL))

    def on_close(self):
        if self.motor:
            self.motor.detener()
        self.destroy()

    def iniciar_simulacion(self):
        from datos.datos_escenarios import generar_condiciones_escenario
        import queue
        # Detener motor previo si existe
        if self.motor:
            self.motor.detener()
        # Limpiar la cola si ya existe, pero nunca la recrees (para mantener la instancia compartida)
        if self.cola_salida_dashboard is not None:
            while not self.cola_salida_dashboard.empty():
                self.cola_salida_dashboard.get()
        # Nunca la recrees aquí, así el motor y la GUI usan la misma
        self.cola_salida_ecg = queue.Queue()
        self.cola_entrada = queue.Queue()
        self.paciente = Paciente.generar_aleatorio()
        escenario, descripcion, condiciones_iniciales = generar_condiciones_escenario()
        # Mostrar contexto
        self.label_escenario.config(text=f"Escenario: {escenario.capitalize()} | {descripcion}")
        # Limpiar signos
        for var in self.vars_signos.values():
            var.set("-")
        # Reiniciar tiempo
        self.tiempo_simulacion = 0
        self.var_tiempo.set("0:00")
        self.actualizando_tiempo = True
        # Cargar condiciones iniciales al motor
        # Eliminar cualquier hemorragia de las condiciones iniciales para evitar duplicados
        condiciones_iniciales = [c for c in condiciones_iniciales if c.get('nombre') != 'hemorragia']
        for cond in condiciones_iniciales:
            self.cola_entrada.put(cond)
        # --- FORZAR HEMORRAGIA MODERADA PARA PRUEBA ---
        cond_hemorragia = {
            'tipo': 'condicion',
            'nombre': 'hemorragia',
            'efecto': {'volumen_sanguineo': -100},  # moderado
            'duracion_restante': None,  # hemorragia indefinida para pruebas
            'nivel': 'moderado'
        }
        self.cola_entrada.put(cond_hemorragia)
        print('[DEBUG][TEST] Hemorragia moderada forzada al inicio de la simulación.')
        # Ya no mostrar signos iniciales aquí; solo se mostrarán cuando el motor publique en la cola_salida
        signos = self.paciente.signos_vitales
        print("[DEBUG] Signos vitales generados:", signos)
        # (No actualizar los labels aquí)
        # Iniciar motor de simulación por 4 minutos (240s)
        from simulacion.simulador_signos import MotorSimulacion
        self.motor = MotorSimulacion(self.paciente, [self.cola_salida_dashboard, self.cola_salida_ecg], self.cola_entrada, intervalo=1, duracion=None)
        self.motor.start()
        # Deshabilitar botón
        self.btn_iniciar.config(state=tk.DISABLED)

    def abrir_ventana_dosis(self, clave_medicamento):
        from ventana_dosis_medicamento import VentanaDosisMedicamento
        from datos.datos_diccionarios import medicamentos_als
        info = medicamentos_als.get(clave_medicamento, {})
        nombre = info.get('nombre', clave_medicamento)
        def callback_aplicar(nombre, dosis, unidad, via):
            from funciones.medicacion import administrar_medicamento
            # Convertir dosis a float (por seguridad)
            try:
                dosis_float = float(dosis)
            except Exception:
                mostrar_error("La dosis debe ser un número válido.", "Error de dosis")
                return
            # Buscar la clave interna del medicamento (por ejemplo, 'adrenalina')
            from datos.datos_diccionarios import medicamentos_als
            clave_medicamento = None
            for clave, datos in medicamentos_als.items():
                if datos.get('nombre', '').lower() == nombre.lower():
                    clave_medicamento = clave
                    break
            if clave_medicamento is None:
                mostrar_error(f"No se encontró el medicamento '{nombre}' en la base de datos.", "Medicamento no encontrado")
                return
            resultado = administrar_medicamento(self.paciente, clave_medicamento, dosis_float, unidad, via, self.procedimientos_realizados)
            efecto = resultado.get('efecto', {})
            duracion = resultado.get('duracion_restante', 0)
            evento = {
                'tipo': 'medicamento',
                'nombre': nombre,
                'dosis': dosis_float,
                'unidad': unidad,
                'via': via,
                'efecto': efecto,
                'duracion_restante': duracion
            }
            if self.cola_entrada:
                self.cola_entrada.put(evento)
            if not resultado.get('ok', False):
                mostrar_advertencia(f"{resultado.get('motivo', 'Dosis fuera de rango')}.\nEfectos secundarios: {resultado.get('efectos_secundarios', [])}", "Advertencia de dosis")
            else:
                mostrar_info(f"{resultado.get('motivo', 'Dosis correcta')}", "Administración exitosa")
        VentanaDosisMedicamento(self, nombre, callback_aplicar)

    def abrir_ventana_manual(self, clave_medicamento):
        from ventana_manual_medicamento import VentanaManualMedicamento
        from datos.datos_diccionarios import medicamentos_als
        info = medicamentos_als.get(clave_medicamento, {})
        nombre = info.get('nombre', clave_medicamento)
        VentanaManualMedicamento(self, nombre, info)



    def solicitar_examen(self, clave, nombre):
        if not self.paciente:
            mostrar_advertencia("Primero inicia la simulación para solicitar exámenes.", "Simulación no iniciada")
            return
        def consulta_thread():
            # Determina el tiempo de espera según el método
            metodo = "herramienta"  # O ajusta según lógica si hay otras opciones
            if metodo == "herramienta":
                tiempo_espera = 6
            else:
                tiempo_espera = 2
            # Abre hoja clínica y arranca temporizador SIN bloquear el hilo
            tiempo = tiempo_espera
            motivo = "Consulta automatizada"
            resultado = consulta_paciente(self.paciente, clave)
            def actualizar_resultado():
                self.datos_hoja_clinica[nombre] = resultado
                self.datos_hoja_clinica[nombre + '_tiempo'] = tiempo
                # Mostrar hoja clínica automáticamente (abrir o actualizar) y detener temporizador
                if getattr(self, 'ventana_hoja_clinica', None) is not None and self.ventana_hoja_clinica.winfo_exists():
                    self.ventana_hoja_clinica.lift()
                    # Detener el temporizador visual si la consulta terminó antes de tiempo
                    if hasattr(self.ventana_hoja_clinica, 'detener_temporizador'):
                        self.ventana_hoja_clinica.detener_temporizador()
                    self.ventana_hoja_clinica.actualizar(self.datos_hoja_clinica, tiempo_ultima_consulta=tiempo)
                else:
                    self.ventana_hoja_clinica = None
                    self.abrir_hoja_clinica()
                mostrar_info(f"{nombre}: {resultado}\n({motivo}, {tiempo}s)", f"Resultado de {nombre}")
            self.after(0, actualizar_resultado)
        threading.Thread(target=consulta_thread, daemon=True).start()

    def abrir_ventana_ecg(self):
        import tkinter as tk
        from ecg.ecg_realtime_gui import ECGRealtimeApp
        if getattr(self, 'ventana_ecg', None) is not None and self.ventana_ecg.winfo_exists():
            self.ventana_ecg.deiconify()
            self.ventana_ecg.lift()
            self.ventana_ecg.focus_force()
        else:
            self.ventana_ecg = tk.Toplevel(self)
            self.ventana_ecg.title("ECG en tiempo real")
            self.ventana_ecg.geometry("950x650")
            # Pasar la cola dedicada al ECG
            self.ecg_app = ECGRealtimeApp(self.ventana_ecg, cola_salida=self.cola_salida_ecg)
            def cerrar_ecg():
                if hasattr(self, 'ecg_app'):
                    self.ecg_app = None
                if hasattr(self, 'ventana_ecg') and self.ventana_ecg is not None:
                    self.ventana_ecg.withdraw()
            self.ventana_ecg.protocol("WM_DELETE_WINDOW", cerrar_ecg)

    def abrir_hoja_clinica(self):
        from ventana_hoja_clinica import VentanaHojaClinica
        if getattr(self, 'ventana_hoja_clinica', None) is not None and self.ventana_hoja_clinica.winfo_exists():
            self.ventana_hoja_clinica.deiconify()
            self.ventana_hoja_clinica.lift()
            self.ventana_hoja_clinica.focus_force()
            tiempos = [v for k,v in self.datos_hoja_clinica.items() if k.endswith('_tiempo')]
            tiempo_ultima = tiempos[-1] if tiempos else None
            self.ventana_hoja_clinica.actualizar(self.datos_hoja_clinica, tiempo_ultima_consulta=tiempo_ultima)
        else:
            tiempos = [v for k,v in self.datos_hoja_clinica.items() if k.endswith('_tiempo')]
            tiempo_ultima = tiempos[-1] if tiempos else None
            self.ventana_hoja_clinica = VentanaHojaClinica(self, self.datos_hoja_clinica)
            self.ventana_hoja_clinica.deiconify()
            self.ventana_hoja_clinica.lift()
            self.ventana_hoja_clinica.focus_force()
            self.ventana_hoja_clinica.actualizar(self.datos_hoja_clinica, tiempo_ultima_consulta=tiempo_ultima)

    def _iniciar_temporizador_hoja_clinica(self, clave, nombre, tiempo_objetivo):
        # Inicia el temporizador regresivo con el tiempo real de la consulta
        if getattr(self, 'ventana_hoja_clinica', None) is not None and self.ventana_hoja_clinica.winfo_exists():
            self.ventana_hoja_clinica.lift()
            self.ventana_hoja_clinica.actualizar(self.datos_hoja_clinica, iniciar_temporizador=tiempo_objetivo)
        else:
            self.ventana_hoja_clinica = None
            self.abrir_hoja_clinica()
            if getattr(self, 'ventana_hoja_clinica', None) is not None and self.ventana_hoja_clinica.winfo_exists():
                self.ventana_hoja_clinica.actualizar(self.datos_hoja_clinica, iniciar_temporizador=tiempo_objetivo)


if __name__ == "__main__":
    app = AppSimulador()
    app.mainloop()
