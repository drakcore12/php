"""
Módulo de simulación de signos vitales para el simulador paramédico.
Gestiona la evolución de los signos vitales de un paciente en función de condiciones,
medicamentos, procedimientos y factores ambientales/fisiológicos.
"""
import threading
import time
import copy
import random

# --- INTEGRACIÓN DE DICCIONARIOS CENTRALIZADOS ---
from datos.datos_diccionarios import (
    SIGNOS_VITALES, PROCEDIMIENTOS, CONDICIONES,
    obtener_condiciones_activables_por_procedimiento,
    obtener_evolucion_condicion
)

import threading
import time
import copy
import random
import queue

from funciones.evaluador_clinico import evaluador_clinico

class MotorSimulacion(threading.Thread):
    """
    Motor de simulación en tiempo real basado en eventos y colas.
    Ejecuta cálculos cada segundo, publica resultados y escucha eventos externos.
    """
    def detener(self):
        """Detiene el hilo de simulación de manera segura."""
        self._stop_event.set()
        if self.is_alive():
            self.join(timeout=2)
    def __init__(self, paciente, colas_salida, cola_entrada, evaluador_reglas=None, intervalo=1, duracion=240):
        super().__init__()
        self.paciente = paciente
        # Permitir una lista de colas de salida
        if isinstance(colas_salida, list):
            self.colas_salida = colas_salida
        else:
            self.colas_salida = [colas_salida]
        self.cola_entrada = cola_entrada
        self.evaluador_reglas = evaluador_reglas
        self.intervalo = intervalo
        self.duracion = duracion
        self.modificadores = []
        self._stop_event = threading.Event()
        self.historial_meds = []  # Historial de medicamentos administrados
        self.historial_procs = []  # Historial de procedimientos

    def run(self):
        print("[DEBUG][MOTOR] Hilo de simulación INICIADO")
        try:
            # --- Inicializar volumen sanguíneo fisiológico si no está ---
            if 'volumen_sanguineo' not in self.paciente.signos_vitales:
                self.paciente.signos_vitales['volumen_sanguineo'] = estimar_volumen_sanguineo(self.paciente)
            signos_base = copy.deepcopy(self.paciente.signos_vitales)
            # Si por error viene anidado, extrae el subdiccionario fisiológico
            if 'signos_vitales' in signos_base:
                signos_base = signos_base['signos_vitales']
            self.signos_base = copy.deepcopy(self.paciente.signos_vitales)
            if 'signos_vitales' in self.signos_base:
                self.signos_base = self.signos_base['signos_vitales']
            if self.duracion is None:
                segundo = 0
                while not self._stop_event.is_set():
                    print(f"[DEBUG][MOTOR] Tick {segundo}")
                    self._simulacion_tick()
                    segundo += 1
                    time.sleep(self.intervalo)
            else:
                for segundo in range(self.duracion):
                    if self._stop_event.is_set():
                        break
                    print(f"[DEBUG][MOTOR] Tick {segundo}")
                    self._simulacion_tick()
                    time.sleep(self.intervalo)
        except Exception as e:
            import traceback
            print("[ERROR][MOTOR] Excepción en el hilo de simulación:")
            traceback.print_exc()

    def _simulacion_tick(self):
        try:
            print('[DEBUG][MOTOR] Entrando a _simulacion_tick')
            print(f'[DEBUG][MOTOR] colas_salida: {self.colas_salida} (type={type(self.colas_salida)}, len={len(self.colas_salida) if hasattr(self.colas_salida, "__len__") else "N/A"})')
            # Procesar nuevos eventos
            while not self.cola_entrada.empty():
                evento = self.cola_entrada.get()
                # Guardar en historial si es medicamento o procedimiento
                if evento.get('tipo') == 'medicamento':
                    self.historial_meds.append(evento)
                if evento.get('tipo') == 'procedimiento':
                    self.historial_procs.append(evento)
        except Exception as e:
            import traceback
            print("[ERROR][MOTOR] Excepción en _simulacion_tick:")
            traceback.print_exc()
            self.modificadores.append(evento)

            # Aplicar efectos de modificadores activos
            signos_base = self.signos_base
            signos_actuales = copy.deepcopy(signos_base)
            # Aplicar modificadores activos SOLO sobre signos vitales
            for mod in self.modificadores:
                if 'efecto' in mod and isinstance(mod['efecto'], dict):
                    for k, v in mod['efecto'].items():
                        if k == 'volumen_sanguineo':
                            continue  # Solo el bloque progresivo de hemorragia puede modificar el volumen sanguíneo
                        if k in signos_actuales:
                            signos_actuales[k] += v

            # --- EFECTO PROGRESIVO DE HEMORRAGIA ---
            hemorragias_activas = [m for m in self.modificadores if m.get('nombre') == 'hemorragia']
            if hemorragias_activas:
                perdida_total = 0
                for mod in hemorragias_activas:
                    efecto = mod.get('efecto', {})
                    perdida = abs(efecto.get('volumen_sanguineo', 0))  # Siempre positiva
                    perdida_total += perdida
                if 'volumen_sanguineo' in signos_actuales:
                    antes = signos_actuales['volumen_sanguineo']
                    signos_actuales['volumen_sanguineo'] -= perdida_total  # Siempre resta sangre
                    # Limitar a [0, volumen_total]
                    volumen_total = estimar_volumen_sanguineo(self.paciente)
                    if signos_actuales['volumen_sanguineo'] < 0:
                        signos_actuales['volumen_sanguineo'] = 0
                    if signos_actuales['volumen_sanguineo'] > volumen_total:
                        signos_actuales['volumen_sanguineo'] = volumen_total
                    despues = signos_actuales['volumen_sanguineo']
                    print(f"[DEBUG][HEMORRAGIA] Volumen sanguíneo: {antes} -> {despues} (-{perdida_total})")

            # --- EVOLUCIÓN AUTOMÁTICA DE SEVERIDAD DE CONDICIONES ---
            from funciones.evolucion_condiciones import evolucionar_condiciones_activas
            self.modificadores = evolucionar_condiciones_activas(self.modificadores, signos_actuales)

            # --- FORZAR PARO SI FV/PARO CARDIACO ---
            condiciones_nombres = [m.get('nombre') for m in self.modificadores if m.get('tipo') == 'condicion']
            # --- Progresión fisiológica: FV crítica progresa a asistolia ---
            if 'paro_cardiaco' in condiciones_nombres:
                signos_actuales['frecuencia_cardiaca'] = 0
                signos_actuales['presion_arterial_sistolica'] = 0
                signos_actuales['presion_arterial_diastolica'] = 0
                # Contador de tiempo en paro
                if not hasattr(self, '_tiempo_fv_paro'):
                    self._tiempo_fv_paro = 1
                else:
                    self._tiempo_fv_paro += 1
                if self._tiempo_fv_paro >= 240:
                    self.paciente.estado_critico = True
                    self.paciente.estado_conciencia = 'inconsciente'
            elif any('fibrilacion' in n for n in condiciones_nombres):
                fc = signos_actuales.get('frecuencia_cardiaca', 20)
                if fc < 30:
                    # Si cualquier tipo de fibrilación persiste con FC < 30 durante 3 ciclos, progresa a paro/asistolia
                    if not hasattr(self, '_fibrilacion_asistolia_count'):
                        self._fibrilacion_asistolia_count = 1
                    else:
                        self._fibrilacion_asistolia_count += 1
                    if self._fibrilacion_asistolia_count >= 3 and 'paro_cardiaco' not in condiciones_nombres:
                        cinfo = CONDICIONES['paro_cardiaco']
                        self.modificadores.append({
                            'tipo': 'condicion',
                            'nombre': 'paro_cardiaco',
                            'efecto': cinfo['afecta'],
                            'duracion_restante': cinfo['duracion']
                        })
                else:
                    self._fibrilacion_asistolia_count = 0
            else:
                self._tiempo_fv_paro = 0
                self._fibrilacion_asistolia_count = 0

            # Al final del tick, guarda los signos actuales como base para el siguiente ciclo
            self.signos_base = copy.deepcopy(signos_actuales)

            # --- LÓGICA DE CONDICIONES FISIOLÓGICAS CRÍTICAS AUTOMÁTICAS ---
            # 1. Shock hipovolémico por bajo volumen sanguíneo
            volumen_total = estimar_volumen_sanguineo(self.paciente)
            if 'volumen_sanguineo' in signos_actuales:
                if signos_actuales['volumen_sanguineo'] < volumen_total * 0.7 and 'shock_hipovolemico' not in [m.get('nombre') for m in self.modificadores]:
                    cinfo = CONDICIONES['shock_hipovolemico']
                    self.modificadores.append({
                        'tipo': 'condicion',
                        'nombre': 'shock_hipovolemico',
                        'efecto': cinfo['afecta'],
                        'duracion_restante': cinfo['duracion']
                    })
            # 2. Paro cardíaco por fibrilación ventricular persistente y FC fuera de rango crítico
            # Usamos un contador simple en el objeto MotorSimulacion
            if not hasattr(self, '_fibrilacion_critica_count'):
                self._fibrilacion_critica_count = 0
            arritmias_activas = [m.get('nombre') for m in self.modificadores if 'fibrilacion' in m.get('nombre','')]
            if arritmias_activas:
                fc = signos_actuales.get('frecuencia_cardiaca', 80)
                if fc < 30 or fc > 200:
                    self._fibrilacion_critica_count += 1
                else:
                    self._fibrilacion_critica_count = 0
                if self._fibrilacion_critica_count >= 3 and 'paro_cardiaco' not in [m.get('nombre') for m in self.modificadores]:
                    cinfo = CONDICIONES['paro_cardiaco']
                    self.modificadores.append({
                        'tipo': 'condicion',
                        'nombre': 'paro_cardiaco',
                        'efecto': cinfo['afecta'],
                        'duracion_restante': cinfo['duracion']
                    })
                else:
                    self._fibrilacion_critica_count = 0
                # Variación fisiológica aleatoria (ruido realista)
                for k in signos_actuales:
                    if k == 'volumen_sanguineo':
                        continue  # No aplicar ruido fisiológico al volumen sanguíneo
                    if k in ['frecuencia_cardiaca', 'frecuencia_respiratoria']:
                        signos_actuales[k] += random.randint(-2, 2)
                    elif k in ['presion_arterial_sistolica', 'presion_arterial_diastolica']:
                        signos_actuales[k] += random.randint(-3, 3)
                    elif k == 'spo2':
                        signos_actuales[k] += random.randint(-1, 1)
                    elif k == 'temperatura':
                        signos_actuales[k] += round(random.uniform(-0.05, 0.05), 2)

                # --- Limitar signos vitales a rangos fisiológicos personalizados por paciente ---

                def get_limite(k, tipo):
                    # Si el paciente tiene límites personalizados, usarlos
                    if hasattr(self.paciente, 'limites_signos') and k in self.paciente.limites_signos:
                        return self.paciente.limites_signos[k][tipo]
                    return SIGNOS_VITALES[k][tipo] if k in SIGNOS_VITALES else None
                for k in signos_actuales:
                    minv = get_limite(k, 'min')
                    maxv = get_limite(k, 'max')
                    if minv is not None:
                        signos_actuales[k] = max(minv, signos_actuales[k])
                    if maxv is not None:
                        signos_actuales[k] = min(maxv, signos_actuales[k])

                # --- Activar condiciones secundarias si se sobrepasan límites fisiológicos ---
                nuevas_condiciones = []
                # Ejemplo: FC > max fisiológico → arritmia_taquicardia, luego fibrilación, luego paro
                fc = signos_actuales.get('frecuencia_cardiaca', 100)
                pa_sys = signos_actuales.get('presion_arterial_sistolica', 120)
                spo2 = signos_actuales.get('spo2', 98)
                temp = signos_actuales.get('temperatura', 36.5)
                condiciones_activas = [m for m in self.modificadores if m.get('tipo') == 'condicion']
                nombres_activas = [c.get('nombre') for c in condiciones_activas]
                # Progresión de arritmias MEJORADA
                # Persistencia mínima para cada arritmia
                if not hasattr(self, '_taquicardia_count'):
                    self._taquicardia_count = 0
                if not hasattr(self, '_fibrilacion_count'):
                    self._fibrilacion_count = 0
                if not hasattr(self, '_fc_normal_count'):
                    self._fc_normal_count = 0
                # TAQUICARDIA: FC alta mantenida
                if fc >= get_limite('frecuencia_cardiaca', 'max'):
                    self._taquicardia_count += 1
                else:
                    self._taquicardia_count = 0
                # FIBRILACIÓN: FC muy alta mantenida tras taquicardia
                if 'arritmia_taquicardia' in nombres_activas and fc > 180:
                    self._fibrilacion_count += 1
                else:
                    self._fibrilacion_count = 0
                # PROGRESIÓN
                if self._taquicardia_count >= 10 and 'arritmia_taquicardia' not in nombres_activas:
                    # 10 ciclos ≈ 10s (ajustable)

                    cinfo = CONDICIONES['arritmia_taquicardia']
                    nuevas_condiciones.append({'tipo': 'condicion', 'nombre': 'arritmia_taquicardia', 'efecto': cinfo['afecta'], 'duracion_restante': cinfo['duracion'], 'ecg': cinfo['ecg']})
                if self._fibrilacion_count >= 10 and 'arritmia_fibrilacion' not in [c['nombre'] for c in nuevas_condiciones]:
                    # 10 ciclos ≈ 10s

                    cinfo = CONDICIONES['arritmia_fibrilacion']
                    nuevas_condiciones.append({'tipo': 'condicion', 'nombre': 'arritmia_fibrilacion', 'efecto': cinfo['afecta'], 'duracion_restante': cinfo['duracion'], 'ecg': cinfo['ecg']})
                # PARO: fibrilación mantenida y FC > 200 por 10s
                if 'arritmia_fibrilacion' in nombres_activas and fc > 200:
                    if not hasattr(self, '_paro_count'):
                        self._paro_count = 0
                    self._paro_count += 1
                    if self._paro_count >= 10 and 'paro_cardiaco' not in nombres_activas:
                        cinfo = CONDICIONES['paro_cardiaco']
                        nuevas_condiciones.append({'tipo': 'condicion', 'nombre': 'paro_cardiaco', 'efecto': cinfo['afecta'], 'duracion_restante': cinfo['duracion']})
            else:
                self._paro_count = 0
            # REVERSIÓN de arritmias si FC normal por 20s
            if fc < get_limite('frecuencia_cardiaca', 'max'):
                self._fc_normal_count += 1
            else:
                self._fc_normal_count = 0
            if self._fc_normal_count >= 20:
                # Revertir todas las arritmias si el paciente está estable por 20s
                self.modificadores = [m for m in self.modificadores if not (m.get('nombre','').startswith('arritmia') or m.get('nombre') == 'paro_cardiaco')]
                self._taquicardia_count = 0
                self._fibrilacion_count = 0
                self._paro_count = 0

            # Solo permitir paro/asistolia si hay contexto clínico o fibrilación severa mantenida, no solo por FC alta momentánea.
            # Lo mismo para otros signos vitales (ejemplo: PA muy baja → shock)
            if pa_sys < get_limite('presion_arterial_sistolica', 'min') and 'shock_hipovolemico' not in nombres_activas:

                cinfo = CONDICIONES['shock_hipovolemico']
                nuevas_condiciones.append({'tipo': 'condicion', 'nombre': 'shock_hipovolemico', 'efecto': cinfo['afecta'], 'duracion_restante': cinfo['duracion']})
            # Agregar nuevas condiciones
            for cond in nuevas_condiciones:
                self.modificadores.append(cond)
            # Desactivar condiciones previas si corresponde (progresión)
            # (ya está gestionado por la reversión arriba, pero se mantiene para compatibilidad)
            if 'arritmia_taquicardia' in nombres_activas and 'arritmia_fibrilacion' in [c['nombre'] for c in nuevas_condiciones]:
                self.modificadores = [m for m in self.modificadores if m.get('nombre') != 'arritmia_taquicardia']
            if 'arritmia_fibrilacion' in nombres_activas and 'paro_cardiaco' in [c['nombre'] for c in nuevas_condiciones]:
                self.modificadores = [m for m in self.modificadores if m.get('nombre') != 'arritmia_fibrilacion']

            # Evaluador clínico centralizado: activa condiciones según reglas
            from funciones.evaluador_clinico import evaluador_clinico, evaluador_resolucion_clinica
            nuevas_condiciones2 = evaluador_clinico(
                signos_actuales,
                self.historial_meds,
                self.historial_procs,
                self.modificadores,
                paciente=self.paciente
            )
            for cond in nuevas_condiciones2:
                self.modificadores.append(cond)
            # Evaluador de resolución clínica: desactiva condiciones si se resuelven
            condiciones_a_desactivar = evaluador_resolucion_clinica(
                signos_actuales,
                self.historial_meds,
                self.historial_procs,
                self.modificadores,
                paciente=self.paciente
            )
            if condiciones_a_desactivar:
                self.modificadores = [m for m in self.modificadores if m.get('nombre') not in condiciones_a_desactivar]

            # Evaluar reglas de negocio
            if self.evaluador_reglas:
                nuevas_condiciones3 = self.evaluador_reglas(signos_actuales)
                for cond in nuevas_condiciones3:
                    self.modificadores.append(cond)
            # Debug profundo: muestra tipo y contenido antes de publicar
            print("[DEBUG][MOTOR][TIPO]", type(signos_actuales), signos_actuales)
            # Asegurar que volumen_sanguineo esté en signos_actuales
            if 'volumen_sanguineo' not in signos_actuales:
                # Buscar en self.paciente.signos_vitales o en paciente directamente
                vsang_paciente = getattr(self.paciente, 'volumen_sanguineo', None)
                if vsang_paciente is None:
                    vsang_paciente = self.paciente.signos_vitales.get('volumen_sanguineo', 'N/A')
                signos_actuales['volumen_sanguineo'] = vsang_paciente
            # Log detallado del volumen sanguíneo y modificadores activos
            vsang = signos_actuales.get('volumen_sanguineo', 'N/A')
            print(f"[DEBUG][MOTOR] Volumen sanguíneo: {vsang}")
            print(f"[DEBUG][MOTOR] Modificadores activos: {[m.get('nombre') for m in self.modificadores]}")
            print("[DEBUG][MOTOR] Publicando en colas_salida:", {'signos_vitales': signos_actuales})
            # Buscar arritmia activa
            arritmia_ecg = None
            for mod in self.modificadores:
                if mod.get('nombre', '').startswith('arritmia') and 'ecg' in mod:
                    arritmia_ecg = mod['ecg']
                    break
            # Si no hay arritmia activa, el ECG refleja el ritmo fisiológico según signos
            if not arritmia_ecg:
                fc = signos_actuales.get('frecuencia_cardiaca', 75)
                if fc == 0:
                    arritmia_ecg = 'asistolia'
                elif fc > 150:
                    arritmia_ecg = 'taquicardia'
                elif fc < 50:
                    arritmia_ecg = 'bradicardia'
                else:
                    arritmia_ecg = 'normal'
            print(f'[DEBUG][MOTOR][FLOW] Publicando en {len(self.colas_salida)} colas.')
            print('[DEBUG][MOTOR][FLOW] Justo antes del for cola in self.colas_salida', flush=True)
            for cola in self.colas_salida:
                print(f'[DEBUG][MOTOR][FLOW] Dentro del for, cola id={id(cola)}')
                # Asegurar que signos_vitales sea un diccionario plano (no anidado)
                campos_gui = [
                    'frecuencia_cardiaca', 'frecuencia_respiratoria',
                    'presion_arterial_sistolica', 'presion_arterial_diastolica',
                    'spo2', 'temperatura', 'volumen_sanguineo'
                ]
                print(f"[DEBUG][MOTOR] Publicando directamente signos_actuales (sin buscar clave 'signos_vitales'): {list(signos_actuales.keys())}")
                signos_planos = signos_actuales.copy()
                # Asegurar que todos los campos estén presentes
                for campo in campos_gui:
                    if campo not in signos_planos:
                        signos_planos[campo] = '-'
                print(f"[DEBUG][MOTOR] Justo antes de publicar en cola {id(cola)}: {{'signos_vitales': signos_planos, 'arritmia_ecg': arritmia_ecg}}")
                cola.put({'signos_vitales': signos_planos, 'arritmia_ecg': arritmia_ecg})
            print('[DEBUG][MOTOR][FLOW] Después del for cola in self.colas_salida')
            print('[DEBUG][MOTOR] Saliendo de _simulacion_tick')
            # Actualizar tiempos de vida y eliminar modificadores expirados
            for mod in self.modificadores:
                # Solo restar duración si es un número (ignorar None)
                if 'duracion_restante' in mod and isinstance(mod['duracion_restante'], (int, float)):
                    mod['duracion_restante'] -= self.intervalo
            # Acumular el estado fisiológico para el siguiente ciclo
            self.signos_base = copy.deepcopy(signos_actuales)

def test_paciente_escenario_motor():
    from clases.paciente import Paciente
    from datos_escenarios import generar_condiciones_escenario
    import queue
    print("\n--- INICIO DE PRUEBA PACIENTE + ESCENARIO + MOTOR ---")
    paciente = Paciente.generar_aleatorio()
    print(f"Paciente generado: {paciente.nombre}, Edad: {paciente.edad}, Sexo: {paciente.sexo}")
    print(f"Signos vitales iniciales: {paciente.signos_vitales}")
    escenario, descripcion, condiciones_iniciales = generar_condiciones_escenario()
    print(f"Escenario: {escenario} - {descripcion}")
    print("Condiciones iniciales:")
    for cond in condiciones_iniciales:
        print(f"  - {cond['nombre']} (efecto: {cond['efecto']}, duración: {cond['duracion_restante']})")
    cola_salida = queue.Queue()
    cola_entrada = queue.Queue()
    # Cargar condiciones iniciales al motor antes de iniciar
    for cond in condiciones_iniciales:
        cola_entrada.put(cond)
    motor = MotorSimulacion(paciente, cola_salida, cola_entrada, intervalo=1, duracion=10)
    motor.start()
    for segundo in range(10):
        if not cola_salida.empty():
            signos = cola_salida.get()
            print(f"[t={segundo}s] Signos vitales: {signos}")
            print(f"[t={segundo}s] Modificadores activos: {[m['nombre'] for m in motor.modificadores]}")
        time.sleep(1)
    motor.detener()
    print("--- FIN DE LA PRUEBA PACIENTE + ESCENARIO + MOTOR ---\n")

    print("\n--- INICIO DE PRUEBA DEL MOTOR DE SIMULACIÓN ---")
    cola_salida = queue.Queue()
    cola_entrada = queue.Queue()
    paciente = Paciente.generar_aleatorio()
    volumen_total = estimar_volumen_sanguineo(paciente)
    sangre_actual = volumen_total
    print("\n--- DATOS COMPLETOS DEL PACIENTE GENERADO ---")
    print("Nombre:", paciente.nombre)
    print("Edad:", paciente.edad)
    print("Sexo:", paciente.sexo)
    print("Peso (kg):", paciente.peso_kg)
    print("Altura (cm):", paciente.altura_cm)
    print("Actividad física:", paciente.actividad_fisica)
    print("Estado nutricional:", paciente.estado_nutricional)
    print("Composición corporal:", paciente.composicion_corporal)
    print("Condición:", paciente.condicion)
    print("Grupo etario:", paciente.grupo_etario)
    print("Factores ambientales:", paciente.factores_ambientales)
    print("Signos vitales base:", paciente.signos_vitales)
    print(f"Volumen sanguíneo estimado: {volumen_total} mL")
    print("--------------------------------------------\n")
    # Evaluador: activa shock hipovolémico si volumen sanguíneo < 70% del total
    shock_activo = False
    def evaluador(signos):
        condiciones = []
        nonlocal sangre_actual, shock_activo
        # Simular pérdida de sangre de 10% cada 2 segundos
        if evaluador.tiempo % 2 == 0 and evaluador.tiempo > 0:
            sangre_actual -= volumen_total * 0.1
            print(f"[t={evaluador.tiempo}s] Pérdida de sangre. Volumen actual: {round(sangre_actual,1)} mL ({round(100*sangre_actual/volumen_total,1)}%)")
        signos['volumen_sanguineo'] = round(sangre_actual, 1)
        if sangre_actual < volumen_total * 0.7 and not shock_activo:
            info = CONDICIONES['shock_hipovolemico']
            condiciones.append({
                'tipo': 'condicion',
                'nombre': 'shock_hipovolemico',
                'efecto': info['afecta'],
                'duracion_restante': info['duracion']
            })
            shock_activo = True
            print(f"[t={evaluador.tiempo}s] ¡Shock hipovolémico ACTIVADO!")
        elif sangre_actual >= volumen_total * 0.7 and shock_activo:
            print(f"[t={evaluador.tiempo}s] Shock hipovolémico DESACTIVADO.")
            shock_activo = False
        evaluador.tiempo += 1
        return condiciones
    evaluador.tiempo = 0
    motor = MotorSimulacion(paciente, cola_salida, cola_entrada, evaluador_reglas=evaluador, intervalo=1, duracion=12)
    motor.start()
    for segundo in range(12):
        # Administrar medicamento a los 3 segundos
        if segundo == 3:
            evento = {
                'tipo': 'medicamento',
                'nombre': 'vasopresores',
                'efecto': MEDICAMENTOS['vasopresores']['afecta'],
                'duracion_restante': MEDICAMENTOS['vasopresores']['duracion']
            }
            cola_entrada.put(evento)
            print(f"[t={segundo}s] Evento: Administración de vasopresores")
        # Mostrar signos vitales y modificadores activos
        if not cola_salida.empty():
            signos = cola_salida.get()
            print(f"[t={segundo}s] Signos vitales: {signos}")
            print(f"[t={segundo}s] Modificadores activos: {motor.modificadores}")
        time.sleep(1)
    motor.detener()
    print("--- FIN DE LA PRUEBA DEL MOTOR ---\n")

# --- FUNCIÓN TEMPORAL MOTOR + CONDICIONES ACTIVAS ---
def test_motor_condiciones_activas():
    from clases.paciente import Paciente
    import time
    paciente = Paciente.generar_aleatorio()
    volumen_total = paciente.signos_vitales['volumen_sanguineo']
    sangre_actual = volumen_total
    modificadores_activos = []
    print(f"\nPaciente generado: {paciente.nombre} | Volumen sanguíneo inicial: {volumen_total} mL")

    def evaluador(signos, shock_activo):
        condiciones = []
        if signos['volumen_sanguineo'] < volumen_total * 0.7 and not shock_activo:
            info = CONDICIONES['shock_hipovolemico']
            condiciones.append({
                'tipo': 'condicion',
                'nombre': 'shock_hipovolemico',
                'efecto': info['afecta'],
                'duracion_restante': info['duracion']
            })
        return condiciones

    shock_activo = False
    for t in range(15):
        # Simular pérdida de sangre
        if t > 0:
            sangre_actual -= volumen_total * 0.08
            sangre_actual = max(sangre_actual, 0)
        signos = paciente.signos_vitales.copy()
        signos['volumen_sanguineo'] = sangre_actual
        # Llamar evaluador y recibir condiciones
        nuevas_condiciones = evaluador(signos, shock_activo)
        # Registrar nuevas condiciones
        for cond in nuevas_condiciones:
            modificadores_activos.append(cond)
            print(f"[t={t}s] Condición ACTIVADA: {cond['nombre']} ({cond['efecto']})")
            if cond['nombre'] == 'shock_hipovolemico':
                shock_activo = True
        # Actualizar duración y eliminar condiciones expiradas
        for mod in list(modificadores_activos):
            if 'duracion_restante' in mod:
                mod['duracion_restante'] -= 1
                if mod['duracion_restante'] <= 0:
                    print(f"[t={t}s] Condición DESACTIVADA: {mod['nombre']}")
                    modificadores_activos.remove(mod)
                    if mod['nombre'] == 'shock_hipovolemico':
                        shock_activo = False
        print(f"[t={t}s] Volumen sanguíneo: {round(sangre_actual,1)} mL | Modificadores activos: {[m['nombre'] for m in modificadores_activos]}")
        time.sleep(1)
    print("--- FIN DE LA PRUEBA MOTOR + CONDICIONES ACTIVAS ---\n")

# --- BLOQUE DE PRUEBA INDEPENDIENTE ---
if __name__ == "__main__":
    test_motor_condiciones_activas()
