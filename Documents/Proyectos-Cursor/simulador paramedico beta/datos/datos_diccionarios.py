# Archivo centralizado de diccionarios clínicos y de simulación
# Aquí se definen los signos vitales, medicamentos, procedimientos y condiciones
# Incluye lógica básica de evolución y activación cruzada

# --- SIGNOS VITALES ---
# Cada entrada: nombre, descripción, unidad, valor normal, límites fisiológicos, etc.
SIGNOS_VITALES = {
    'frecuencia_cardiaca': {
        'descripcion': 'Latidos por minuto',
        'unidad': 'lpm',
        'normal': (60, 100),
        'min': 0, 'max': 250
    },
    'frecuencia_respiratoria': {
        'descripcion': 'Respiraciones por minuto',
        'unidad': 'rpm',
        'normal': (12, 20),
        'min': 5, 'max': 60
    },
    'presion_arterial_sistolica': {
        'descripcion': 'Presión arterial sistólica',
        'unidad': 'mmHg',
        'normal': (90, 120),
        'min': 40, 'max': 250
    },
    'presion_arterial_diastolica': {
        'descripcion': 'Presión arterial diastólica',
        'unidad': 'mmHg',
        'normal': (60, 80),
        'min': 20, 'max': 150
    },
    'spo2': {
        'descripcion': 'Saturación de oxígeno',
        'unidad': '%',
        'normal': (95, 100),
        'min': 70, 'max': 100
    },
    'temperatura': {
        'descripcion': 'Temperatura corporal',
        'unidad': '°C',
        'normal': (36.0, 37.5),
        'min': 25.0, 'max': 43.0
    },
    'volumen_sanguineo': {
        'descripcion': 'Volumen sanguíneo total',
        'unidad': 'mL',
        'normal': None,
        'min': 0, 'max': 8000
    },
    'dolor': {
        'descripcion': 'Escala de dolor subjetiva',
        'unidad': '0-10',
        'normal': (0, 2),
        'min': 0, 'max': 10
    },
}

# --- MEDICAMENTOS ALS (detallado, para calculadora de dosis) ---
# Cada entrada: nombre, fórmula, unidad, rango, presentación, efectos secundarios
medicamentos_als = {
    "adrenalina": {
        "nombre": "Adrenalina (Epinefrina)",
        "formula": "peso * 0.01",
        "unidad": "mg",
        "rango": "0.01 mg/kg (máx 1 mg)",
        "adulto": "1 mg IV/IO c/3-5 min",
        "presentacion": "1 mg/10 mL (1:10 000)",
        "efectos_secundarios": ["Taquicardia", "Hipertensión arterial", "Arritmias ventriculares", "Aumento consumo O2"],
        "efectos_secundarios_sobredosis": ["Arritmias ventriculares", "Crisis hipertensiva", "Isquemia miocárdica"],
        "efectos_secundarios_subdosis": ["Ineficacia terapéutica", "No respuesta clínica"]
    },
    "amiodarona": {
        "nombre": "Amiodarona",
        "formula": "peso * 5",
        "unidad": "mg",
        "rango": "5 mg/kg (máx 300 mg)",
        "adulto": "Carga 5 mg/kg, mantenimiento 1 mg/min",
        "presentacion": "50 mg/mL",
        "efectos_secundarios": ["Bradicardia", "Bloqueo AV", "Hipotensión", "Fibrosis pulmonar"],
        "efectos_secundarios_sobredosis": ["Bradicardia severa", "Bloqueo AV completo", "Paro cardíaco"],
        "efectos_secundarios_subdosis": ["Arritmia persistente", "Falta de control de ritmo"]
    },
    "atropina": {
        "nombre": "Atropina",
        "formula": "peso * 0.02",
        "unidad": "mg",
        "rango": "0.02 mg/kg (máx 0.5 mg/dosis, hasta 3 mg total)",
        "adulto": "0.5 mg IV c/3-5 min (máx 3 mg)",
        "presentacion": "1 mg/10 mL",
        "efectos_secundarios": ["Taquicardia marcada", "Xerostomía", "Midriasis", "Retención urinaria", "Constipación"],
        "efectos_secundarios_sobredosis": ["Taquiarritmias", "Delirio", "Fiebre"],
        "efectos_secundarios_subdosis": ["Bradicardia persistente", "No reversión de bradicardia"]
    },
    "adenosina": {
        "nombre": "Adenosina",
        "formula": "fija",
        "unidad": "mg",
        "rango": "6 mg, luego 12 mg x2 si no resuelve",
        "presentacion": "6 mg/2 mL",
        "efectos_secundarios": ["Opresión torácica", "Bradicardia transitoria", "Enrojecimiento facial", "Broncoespasmo"],
        "efectos_secundarios_sobredosis": ["Asistolia", "Bloqueo AV completo", "Broncoespasmo severo"],
        "efectos_secundarios_subdosis": ["Persistencia de taquicardia"]
    },
    "lidocaina": {
        "nombre": "Lidocaína",
        "formula": "peso * 1",
        "unidad": "mg",
        "rango": "1 mg/kg (máx 100 mg)",
        "presentacion": "100 mg/5 mL (2%)",
        "efectos_secundarios": ["Mareo", "Tinnitus", "Visión borrosa", "Convulsiones", "Bradicardia", "Hipotensión"],
        "efectos_secundarios_sobredosis": ["Convulsiones", "Paro cardíaco", "Depresión respiratoria"],
        "efectos_secundarios_subdosis": ["Ineficacia antiarrítmica"]
    },
    "nitroglicerina": {
        "nombre": "Nitroglicerina",
        "formula": "peso * 0.5-5",
        "unidad": "µg/min",
        "rango": "Sublingual 0.3-0.6 mg c/5 min (hasta 3)",
        "presentacion": "0.4 mg/dosis (spray), 5 mg/mL perfusión",
        "efectos_secundarios": ["Cefalea", "Taquicardia refleja", "Hipotensión", "Enrojecimiento"],
        "efectos_secundarios_sobredosis": ["Hipotensión severa", "Síncope", "Taquicardia intensa"],
        "efectos_secundarios_subdosis": ["Dolor torácico persistente"]
    },
    "furosemida": {
        "nombre": "Furosemida",
        "formula": "peso * 0.5-1",
        "unidad": "mg",
        "rango": "0.5-1 mg/kg (máx 40-80 mg)",
        "presentacion": "10 mg/mL",
        "efectos_secundarios": ["Hipotensión", "Deshidratación", "Hipokalemia", "Hiponatremia", "Ototoxicidad"],
        "efectos_secundarios_sobredosis": ["Shock hipovolémico", "Arritmia por hipokalemia", "Insuficiencia renal"],
        "efectos_secundarios_subdosis": ["Edema persistente", "Falta de diuresis"]
    },
    "morfina": {
        "nombre": "Morfina",
        "formula": "peso * 0.1",
        "unidad": "mg",
        "rango": "0.05-0.1 mg/kg (máx 10 mg/dosis)",
        "presentacion": "10 mg/1 mL",
        "efectos_secundarios": ["Depresión respiratoria", "Náuseas", "Bradicardia", "Hipotensión"],
        "efectos_secundarios_sobredosis": ["Paro respiratorio", "Bradicardia severa", "Coma"],
        "efectos_secundarios_subdosis": ["Dolor persistente", "Ineficacia analgésica"]
    },
    "fentanilo": {
        "nombre": "Fentanilo",
        "formula": "peso * 1-2",
        "unidad": "µg",
        "rango": "1-2 µg/kg (máx 100 µg/dosis)",
        "presentacion": "50 µg/mL",
        "efectos_secundarios": ["Depresión respiratoria intensa", "Rigidez torácica", "Náuseas", "Bradicardia"],
        "efectos_secundarios_sobredosis": ["Paro respiratorio", "Rigidez muscular severa", "Coma"],
        "efectos_secundarios_subdosis": ["Dolor persistente", "Ineficacia analgésica"]
    },
    "salbutamol": {
        "nombre": "Salbutamol (Albuterol)",
        "formula": "fija",
        "unidad": "mg o µg",
        "rango": "2.5 mg nebulizado o 100-200 µg inhalado",
        "presentacion": "2.5 mg/2.5 mL",
        "efectos_secundarios": ["Temblor", "Nerviosismo", "Taquicardia", "Hipopotasemia"],
        "efectos_secundarios_sobredosis": ["Taquiarritmias", "Hipopotasemia severa", "Crisis hipertensiva"],
        "efectos_secundarios_subdosis": ["Broncoespasmo persistente"]
    },
    "ipratropio": {
        "nombre": "Ipratropio",
        "formula": "fija",
        "unidad": "mg",
        "rango": "0.5 mg nebulización c/6-8 h",
        "presentacion": "0.5 mg/2.5 mL",
        "efectos_secundarios": ["Boca seca", "Taquicardia leve", "Glaucoma agudo"],
        "efectos_secundarios_sobredosis": ["Delirio", "Retención urinaria severa", "Visión borrosa intensa"],
        "efectos_secundarios_subdosis": ["Broncoespasmo persistente"]
    },
    "dextrosa": {
        "nombre": "Dextrosa",
        "formula": "peso * 0.5-1",
        "unidad": "g",
        "rango": "0.5-1 g/kg",
        "presentacion": "Dextrosa 10%, 50%",
        "efectos_secundarios": ["Hiperglucemia", "Flebitis", "Extravasación"],
        "efectos_secundarios_sobredosis": ["Hiperglucemia severa", "Deshidratación", "Alteración del sensorio"],
        "efectos_secundarios_subdosis": ["Hipoglucemia persistente"]
    },
    "naloxona": {
        "nombre": "Naloxona",
        "formula": "peso * 0.1",
        "unidad": "mg",
        "rango": "0.01-0.02 mg/kg (máx 2 mg/dosis)",
        "presentacion": "0.4 mg/mL",
        "efectos_secundarios": ["Ansiedad", "Agitación", "Taquicardia", "Hipertensión", "Síndrome de abstinencia"],
        "efectos_secundarios_sobredosis": ["Convulsiones", "Arritmias", "HTA severa"],
        "efectos_secundarios_subdosis": ["Persistencia de depresión respiratoria"]
    },
    "midazolam": {
        "nombre": "Midazolam",
        "formula": "peso * 0.1-0.2",
        "unidad": "mg",
        "rango": "0.05-0.1 mg/kg (máx 2.5-5 mg/dosis)",
        "presentacion": "5 mg/mL",
        "efectos_secundarios": ["Depresión respiratoria", "Amnesia", "Bradicardia", "Hipotensión"],
        "efectos_secundarios_sobredosis": ["Coma", "Paro respiratorio", "Bradicardia severa"],
        "efectos_secundarios_subdosis": ["Convulsiones persistentes", "Ansiedad"]
    },
    "diazepam": {
        "nombre": "Diazepam",
        "formula": "peso * 0.2",
        "unidad": "mg",
        "rango": "0.1-0.2 mg/kg (máx 5-10 mg/dosis)",
        "presentacion": "5 mg/mL",
        "efectos_secundarios": ["Sedación profunda", "Depresión respiratoria", "Tolerancia", "Dependencia"],
        "efectos_secundarios_sobredosis": ["Coma", "Paro respiratorio", "Hipotensión severa"],
        "efectos_secundarios_subdosis": ["Convulsiones persistentes", "Ansiedad"]
    },
    "ondansetron": {
        "nombre": "Ondansetrón",
        "formula": "fija",
        "unidad": "mg",
        "rango": "4 mg IV lento (máx 8 mg)",
        "presentacion": "2 mg/2 mL",
        "efectos_secundarios": ["Cefalea", "Estreñimiento", "Diarrea", "QT largo"],
        "efectos_secundarios_sobredosis": ["Arritmia ventricular", "Bloqueo AV", "QT muy prolongado"],
        "efectos_secundarios_subdosis": ["Persistencia de náusea"]
    },
    "difenhidramina": {
        "nombre": "Difenhidramina",
        "formula": "peso * 1",
        "unidad": "mg",
        "rango": "1-2 mg/kg (máx 50 mg)",
        "presentacion": "50 mg/mL",
        "efectos_secundarios": ["Somnolencia", "Boca seca", "Visión borrosa", "Retención urinaria"],
        "efectos_secundarios_sobredosis": ["Coma", "Delirio", "Alucinaciones"],
        "efectos_secundarios_subdosis": ["Alergia persistente"]
    },
    "metilprednisolona": {
        "nombre": "Metilprednisolona / Hidrocortisona",
        "formula": "fija",
        "unidad": "mg",
        "rango": "Metilprednisolona: 1 mg/kg (máx 125 mg), Hidrocortisona: 4 mg/kg (máx 100 mg)",
        "presentacion": "vial",
        "efectos_secundarios": ["Hiperglucemia", "Retención de líquidos", "Inmunosupresión"],
        "efectos_secundarios_sobredosis": ["Hiperglucemia severa", "Infección grave", "Miopatía"],
        "efectos_secundarios_subdosis": ["Falta de respuesta clínica"]
    },
    "glucagon": {
        "nombre": "Glucagón",
        "formula": "peso * 0.1",
        "unidad": "mg",
        "rango": "0.1 mg/kg (máx 1 mg)",
        "presentacion": "1 mg/vial reconstituido",
        "efectos_secundarios": ["Náuseas", "Vómitos", "Hiperglucemia transitoria"],
        "efectos_secundarios_sobredosis": ["Hiperglucemia severa", "Confusión", "Hipotensión"],
        "efectos_secundarios_subdosis": ["Hipoglucemia persistente"]
    },
}

# --- PROCEDIMIENTOS ---
# Cada entrada: efectos, duración, condiciones que puede activar por repetición
PROCEDIMIENTOS = {
    'rcp': {
        'afecta': {'fc': 30, 'dolor': 2},
        'duracion': 1,
        'puede_activar': lambda repeticiones: ['dolor'] if repeticiones > 3 else []
    },
    'intubacion': {
        'afecta': {'spo2': 5, 'dolor': 3},
        'duracion': 1,
        'puede_activar': lambda repeticiones: ['lesion_via_aerea'] if repeticiones > 2 else []
    }
}

# --- CONDICIONES ---
# Cada entrada: efectos, duración, evolución a otras condiciones
CONDICIONES = {
    'arritmia_taquicardia': {
        # Niveles de severidad para mayor realismo
        'niveles': {
            'leve': {
                'afecta': {'frecuencia_cardiaca': 0.3, 'spo2': -0.02}, 'duracion': 12
            },
            'moderado': {
                'afecta': {'frecuencia_cardiaca': 0.6, 'spo2': -0.05}, 'duracion': 8
            },
            'grave': {
                'afecta': {'frecuencia_cardiaca': 1.2, 'spo2': -0.1}, 'duracion': 4
            }
        },
        'nivel_inicial': 'leve',
        'ecg': 'taquicardia',
        # La evolución puede depender del nivel y signos vitales
        'evoluciona_a': lambda signos, nivel: ['fibrilacion_ventricular'] if nivel == 'grave' and signos.get('frecuencia_cardiaca', 100) > 180 else []
    },
    'arritmia_bradicardia': {
        'afecta': {'frecuencia_cardiaca': -0.6, 'spo2': -0.05},  # por segundo
        'duracion': 8,
        'ecg': 'bradicardia',
        'evoluciona_a': lambda signos: ['paro_cardiaco'] if signos.get('frecuencia_cardiaca', 100) < 30 else []
    },
    'arritmia_fibrilacion': {
        'afecta': {'frecuencia_cardiaca': -0.17, 'spo2': -0.17},  # por segundo
        'duracion': 6,
        'ecg': 'fibrilacion',
        'evoluciona_a': lambda signos: ['paro_cardiaco'] if signos.get('spo2', 100) < 80 else []
    },
    'shock_hipovolemico': {
        'afecta': {'frecuencia_cardiaca': 0.1, 'presion_arterial_sistolica': -0.2},  # igual que 'leve'
        'duracion': 10,  # igual que 'leve'
        'niveles': {
            'leve': {
                'afecta': {'frecuencia_cardiaca': 0.1, 'presion_arterial_sistolica': -0.2}, 'duracion': 10
            },
            'moderado': {
                'afecta': {'frecuencia_cardiaca': 0.25, 'presion_arterial_sistolica': -0.5}, 'duracion': 6
            },
            'grave': {
                'afecta': {'frecuencia_cardiaca': 0.5, 'presion_arterial_sistolica': -1.0}, 'duracion': 3
            }
        },
        'nivel_inicial': 'leve',
        'evoluciona_a': lambda signos, nivel: ['paro_cardiaco'] if nivel == 'grave' and signos.get('presion_arterial_sistolica', 80) < 50 else []
    },
    'hipertension': {
        'afecta': {'presion_arterial_sistolica': 0.33},  # por segundo
        'duracion': 10,
        'evoluciona_a': lambda signos: ['acv'] if signos.get('pa_sys', 0) > 200 else []
    },
    'dolor': {
        'niveles': {
            'leve': {
                'afecta': {'frecuencia_cardiaca': 0.03}, 'duracion': 6
            },
            'moderado': {
                'afecta': {'frecuencia_cardiaca': 0.08}, 'duracion': 3
            },
            'grave': {
                'afecta': {'frecuencia_cardiaca': 0.15}, 'duracion': 1
            }
        },
        'nivel_inicial': 'leve',
        'evoluciona_a': lambda signos, nivel: []
    },
    'paro_cardiaco': {
        'afecta': {
            'frecuencia_cardiaca': -9999,
            'presion_arterial_sistolica': -9999,
            'presion_arterial_diastolica': -9999,
            'spo2': -9999
        },
        'duracion': 999,
        'evoluciona_a': lambda signos: []
    },
    'hemorragia': {
        # Pérdida progresiva de volumen sanguíneo (por segundo)
        'afecta': {'volumen_sanguineo': -100},  # valor por defecto: moderado
        'duracion': 20,
        'niveles': {
            'leve': {'afecta': {'volumen_sanguineo': -50}, 'duracion': 30},
            'moderado': {'afecta': {'volumen_sanguineo': -100}, 'duracion': 20},
            'grave': {'afecta': {'volumen_sanguineo': -250}, 'duracion': 10}
        },
        'nivel_inicial': 'moderado',
        'evoluciona_a': lambda signos, nivel: ['shock_hipovolemico'] if signos.get('volumen_sanguineo', 5000) < 0.7 * signos.get('volumen_sanguineo_total', 5000) else []
    },
    'agresividad': {
        'afecta': {'frecuencia_cardiaca': 0.13},  # por segundo
        'duracion': 5,
        'evoluciona_a': lambda signos: []
    },
    'lesion_via_aerea': {
        'afecta': {'spo2': -0.17},  # por segundo
        'duracion': 8,
        'evoluciona_a': lambda signos: []
    },
    'acv': {
        'afecta': {'frecuencia_cardiaca': -0.17, 'spo2': -0.17},  # por segundo
        'duracion': 30,
        'evoluciona_a': lambda signos: []
    }
}

# --- UTILIDAD ---

def obtener_condiciones_activables_por_procedimiento(nombre, repeticiones):
    proc = PROCEDIMIENTOS.get(nombre, {})
    if 'puede_activar' in proc and callable(proc['puede_activar']):
        return proc['puede_activar'](repeticiones)
    return []

def obtener_evolucion_condicion(nombre, signos):
    cond = CONDICIONES.get(nombre, {})
    if 'evoluciona_a' in cond and callable(cond['evoluciona_a']):
        return cond['evoluciona_a'](signos)
    return []
