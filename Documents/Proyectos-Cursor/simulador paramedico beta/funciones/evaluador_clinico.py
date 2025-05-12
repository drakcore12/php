from datos.datos_diccionarios import CONDICIONES, medicamentos_als

def evaluador_clinico(signos, historial_meds, historial_procs, condiciones_activas, paciente=None, efecto_a_condicion=None):
    """
    Observa signos vitales, historial de medicamentos, procedimientos y condiciones activas.
    Activa condiciones clínicas según reglas y el diccionario CONDICIONES.
    Retorna una lista de nuevas condiciones a activar.
    Permite inyectar el mapeo efecto→condición para máxima testabilidad.
    """
    condiciones_nuevas = []
    # --- Reacciones adversas por combinaciones peligrosas de medicamentos ---
    if efecto_a_condicion is None:
        efecto_a_condicion = {
            'Taquicardia': 'arritmia_taquicardia',
            'Arritmias ventriculares': 'arritmia_taquicardia',
            'Bradicardia': 'arritmia_bradicardia',
            'Bradicardia transitoria': 'arritmia_bradicardia',
            'Bloqueo AV': 'bloqueo_av',
            'Hipotensión': 'hipotension',
            'Hipertensión arterial': 'hipertension',
            'Dolor': 'dolor',
            'Fibrosis pulmonar': 'fibrosis_pulmonar',
            'Opresión torácica': 'opresion_toracica',
            'Enrojecimiento facial': 'enrojecimiento_facial',
            'Broncoespasmo': 'broncoespasmo',
            'Depresión respiratoria': 'depresion_respiratoria',
            'QT largo': 'qt_largo',
            # Agrega más mapeos según tus condiciones definidas
        }

    # Ahora cada combinación puede activar una o varias condiciones adversas
    combinaciones_peligrosas = [
        (['amiodarona', 'fentanilo'], ['qt_largo']),
        (['amiodarona', 'ondansetron'], ['qt_largo']),
        (['morfina', 'midazolam'], ['depresion_respiratoria', 'hipotension']),
        (['morfina', 'diazepam'], ['depresion_respiratoria']),
        (['adrenalina', 'furosemida'], ['hipopotasemia']),
        (['furosemida', 'salbutamol'], ['hipopotasemia']),
        # Puedes añadir más combinaciones y efectos adversos
    ]
    nombres_meds = [m['nombre'].lower() for m in historial_meds[-3:]]
    for combinacion, condiciones in combinaciones_peligrosas:
        if all(med in nombres_meds for med in combinacion):
            for condicion in (condiciones if isinstance(condiciones, list) else [condiciones]):
                if condicion in CONDICIONES and condicion not in [c['nombre'] for c in condiciones_activas]:
                    condiciones_nuevas.append(crear_condicion_con_nivel(condicion))

    # --- Ejemplo: arritmia por sobredosis de adrenalina ---
    for med in historial_meds[-3:]:  # últimos 3 eventos
        nombre = med['nombre'].lower()
        info = medicamentos_als.get(nombre)
        if not info:
            continue
        if nombre == 'adrenalina':
            peso = paciente.peso_kg if paciente and hasattr(paciente, 'peso_kg') else 70
            try:
                dosis_recomendada = eval(info['formula'], {}, {'peso': peso})
            except Exception:
                dosis_recomendada = 1
            if float(med['dosis']) > dosis_recomendada * 1.5:
                condiciones_nuevas.append({
                    'tipo': 'condicion',
                    'nombre': 'arritmia_taquicardia',
                    'efecto': CONDICIONES['arritmia_taquicardia']['afecta'],
                    'duracion_restante': CONDICIONES['arritmia_taquicardia']['duracion'],
                    'ecg': CONDICIONES['arritmia_taquicardia']['ecg']
                })
        # Activar condiciones por efectos secundarios diferenciando tipo de error
        if not med.get('ok', True):
            motivo = med.get('motivo', '').lower()
            # Busca efectos secundarios diferenciados
            if 'subdosis' in motivo or 'subdosificación' in motivo:
                efectos = info.get('efectos_secundarios_subdosis', info.get('efectos_secundarios', []))
            elif 'sobredosis' in motivo or 'sobredosificación' in motivo:
                efectos = info.get('efectos_secundarios_sobredosis', info.get('efectos_secundarios', []))
            else:
                efectos = info.get('efectos_secundarios', [])
            for efecto in efectos:
                clave_cond = efecto_a_condicion.get(efecto)
                if clave_cond and clave_cond in CONDICIONES and clave_cond not in [c['nombre'] for c in condiciones_activas]:
                    condiciones_nuevas.append(crear_condicion_con_nivel(clave_cond))
        # Puedes agregar más reglas para otros medicamentos aquí
    # --- Ejemplo: shock si PA sistólica < 70 y no está activo ---
    if signos.get('presion_arterial_sistolica', 100) < 70 and 'shock_hipovolemico' not in [c['nombre'] for c in condiciones_activas]:
        condiciones_nuevas.append({
            'tipo': 'condicion',
            'nombre': 'shock_hipovolemico',
            'efecto': CONDICIONES['shock_hipovolemico']['afecta'],
            'duracion_restante': CONDICIONES['shock_hipovolemico']['duracion']
        })
    # --- Ejemplo: dolor si se realiza un procedimiento invasivo ---
    for proc in historial_procs[-2:]:
        if proc['nombre'] == 'intubacion' and 'dolor' not in [c['nombre'] for c in condiciones_activas]:
            condiciones_nuevas.append({
                'tipo': 'condicion',
                'nombre': 'dolor',
                'efecto': CONDICIONES['dolor']['afecta'],
                'duracion_restante': CONDICIONES['dolor']['duracion']
            })
    # Puedes agregar más reglas clínicas aquí
    return condiciones_nuevas

def evaluador_resolucion_clinica(signos, historial_meds, historial_procs, condiciones_activas, paciente=None):
    """
    Observa signos vitales, historial y condiciones activas.
    Devuelve una lista de nombres de condiciones que deben desactivarse si se cumplen parámetros de resolución clínica.
    """
    condiciones_a_desactivar = []
    # Ejemplo: resolver arritmia si FC vuelve a rango normal
    for cond in condiciones_activas:
        if cond['nombre'] == 'arritmia_taquicardia':
            fc = signos.get('frecuencia_cardiaca', 100)
            if 60 <= fc <= 110:
                condiciones_a_desactivar.append('arritmia_taquicardia')
        if cond['nombre'] == 'arritmia_bradicardia':
            fc = signos.get('frecuencia_cardiaca', 100)
            if 60 <= fc <= 110:
                condiciones_a_desactivar.append('arritmia_bradicardia')
        if cond['nombre'] == 'shock_hipovolemico':
            pas = signos.get('presion_arterial_sistolica', 100)
            if pas > 90:
                condiciones_a_desactivar.append('shock_hipovolemico')
        if cond['nombre'] == 'dolor':
            # Ejemplo: dolor se resuelve si FC baja a normal
            fc = signos.get('frecuencia_cardiaca', 100)
            if 60 <= fc <= 100:
                condiciones_a_desactivar.append('dolor')
    # Puedes agregar más reglas de resolución aquí
    return condiciones_a_desactivar

    """
    Observa signos vitales, historial de medicamentos, procedimientos y condiciones activas.
    Activa condiciones clínicas según reglas y el diccionario CONDICIONES.
    Retorna una lista de nuevas condiciones a activar.
    """
    condiciones_nuevas = []
    # --- Reacciones adversas por combinaciones peligrosas de medicamentos ---
    # Ahora cada combinación puede activar una o varias condiciones adversas
    combinaciones_peligrosas = [
        (['amiodarona', 'fentanilo'], ['qt_largo']),
        (['amiodarona', 'ondansetron'], ['qt_largo']),
        (['morfina', 'midazolam'], ['depresion_respiratoria', 'hipotension']),
        (['morfina', 'diazepam'], ['depresion_respiratoria']),
        (['adrenalina', 'furosemida'], ['hipopotasemia']),
        (['furosemida', 'salbutamol'], ['hipopotasemia']),
        # Puedes añadir más combinaciones y efectos adversos
    ]
    nombres_meds = [m['nombre'].lower() for m in historial_meds[-3:]]
    for combinacion, condiciones in combinaciones_peligrosas:
        if all(med in nombres_meds for med in combinacion):
            for condicion in (condiciones if isinstance(condiciones, list) else [condiciones]):
                if condicion in CONDICIONES and condicion not in [c['nombre'] for c in condiciones_activas]:
                    condiciones_nuevas.append(crear_condicion_con_nivel(condicion))

    # --- Ejemplo: arritmia por sobredosis de adrenalina ---
    for med in historial_meds[-3:]:  # últimos 3 eventos
        nombre = med['nombre'].lower()
        info = medicamentos_als.get(nombre)
        if not info:
            continue
        if nombre == 'adrenalina':
            peso = paciente.peso_kg if paciente and hasattr(paciente, 'peso_kg') else 70
            try:
                dosis_recomendada = eval(info['formula'], {}, {'peso': peso})
            except Exception:
                dosis_recomendada = 1
            if float(med['dosis']) > dosis_recomendada * 1.5:
                condiciones_nuevas.append({
                    'tipo': 'condicion',
                    'nombre': 'arritmia_taquicardia',
                    'efecto': CONDICIONES['arritmia_taquicardia']['afecta'],
                    'duracion_restante': CONDICIONES['arritmia_taquicardia']['duracion'],
                    'ecg': CONDICIONES['arritmia_taquicardia']['ecg']
                })
        # Activar condiciones por efectos secundarios diferenciando tipo de error
        if not med.get('ok', True):
            motivo = med.get('motivo', '').lower()
            # Busca efectos secundarios diferenciados
            if 'subdosis' in motivo or 'subdosificación' in motivo:
                efectos = info.get('efectos_secundarios_subdosis', info.get('efectos_secundarios', []))
            elif 'sobredosis' in motivo or 'sobredosificación' in motivo:
                efectos = info.get('efectos_secundarios_sobredosis', info.get('efectos_secundarios', []))
            else:
                efectos = info.get('efectos_secundarios', [])
            for efecto in efectos:
                clave_cond = efecto_a_condicion.get(efecto)
                if clave_cond and clave_cond in CONDICIONES and clave_cond not in [c['nombre'] for c in condiciones_activas]:
                    condiciones_nuevas.append(crear_condicion_con_nivel(clave_cond))
        # Puedes agregar más reglas para otros medicamentos aquí
    # --- Ejemplo: shock si PA sistólica < 70 y no está activo ---
    if signos.get('presion_arterial_sistolica', 100) < 70 and 'shock_hipovolemico' not in [c['nombre'] for c in condiciones_activas]:
        condiciones_nuevas.append({
            'tipo': 'condicion',
            'nombre': 'shock_hipovolemico',
            'efecto': CONDICIONES['shock_hipovolemico']['afecta'],
            'duracion_restante': CONDICIONES['shock_hipovolemico']['duracion']
        })
    # --- Ejemplo: dolor si se realiza un procedimiento invasivo ---
    for proc in historial_procs[-2:]:
        if proc['nombre'] == 'intubacion' and 'dolor' not in [c['nombre'] for c in condiciones_activas]:
            condiciones_nuevas.append({
                'tipo': 'condicion',
                'nombre': 'dolor',
                'efecto': CONDICIONES['dolor']['afecta'],
                'duracion_restante': CONDICIONES['dolor']['duracion']
            })
    # Puedes agregar más reglas clínicas aquí
    return condiciones_nuevas
