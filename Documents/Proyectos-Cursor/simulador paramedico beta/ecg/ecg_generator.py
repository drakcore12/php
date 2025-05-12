import numpy as np

def generar_ecg_waveform(estado_ecg, frecuencia_cardiaca=75, duracion=2, fs=100, arritmia=None):
    """
    Genera una señal sintética de ECG realista y soporta múltiples arritmias.
    Devuelve: t, señal, qrs_pos, interpretacion
    """
    t = np.linspace(0, duracion, int(fs*duracion), endpoint=False)
    señal = np.zeros_like(t)
    qrs_pos = []
    interpretacion = "Ritmo sinusal normal"

    # Prioridad: arritmia explícita > estado_ecg
    ritmo = arritmia if arritmia and arritmia != 'auto' else estado_ecg
    ritmo = ritmo.lower()

    bpm = max(30, min(220, frecuencia_cardiaca))
    rr_mean = 60.0 / bpm if bpm > 0 else duracion
    latidos = int(duracion / rr_mean) + 2 if bpm > 0 else 1

    if ritmo in ['normal', 'sinusal']:
        interpretacion = "Ritmo sinusal normal"
        # Parámetros fisiológicos
        P_dur = 0.09   # s
        P_amp = 0.18   # mV
        PR_int = 0.16  # s (inicio P a inicio QRS)
        QRS_dur = 0.09 # s
        Q_amp = -0.15  # mV
        R_amp = 1.0    # mV
        S_amp = -0.25  # mV
        ST_dur = 0.10  # s
        T_dur = 0.16   # s
        T_amp = 0.35   # mV
        QT_int = 0.36  # s (inicio QRS a fin T)
        U_dur = 0.08   # s
        U_amp = 0.05   # mV
        rr_intervals = np.random.normal(loc=rr_mean, scale=0.04*rr_mean, size=latidos)
        centros = np.cumsum(rr_intervals)
        centros = centros[centros < duracion]
        for centro in centros:
            # Onda P
            P_center = centro - PR_int + P_dur/2
            señal += P_amp * np.exp(-((t - P_center)**2) / (2*(P_dur/2.5)**2))
            # Complejo QRS
            Q_center = centro - QRS_dur/3
            R_center = centro
            S_center = centro + QRS_dur/3
            señal += Q_amp * np.exp(-((t - Q_center)**2) / (2*(QRS_dur/7)**2))
            señal += R_amp * np.exp(-((t - R_center)**2) / (2*(QRS_dur/9)**2))
            señal += S_amp * np.exp(-((t - S_center)**2) / (2*(QRS_dur/7)**2))
            # Segmento ST (isoeléctrico): no suma nada, solo mantiene línea base
            # Onda T
            T_center = centro + QRS_dur/2 + ST_dur + T_dur/2
            señal += T_amp * np.exp(-((t - T_center)**2) / (2*(T_dur/2.5)**2))
            # Onda U (opcional, pequeña)
            U_center = T_center + T_dur/2 + U_dur/2
            señal += U_amp * np.exp(-((t - U_center)**2) / (2*(U_dur/2.5)**2))
            # QRS index para marcadores
            qrs_idx = np.argmin(np.abs(t-centro))
            qrs_pos.append(qrs_idx)
    elif ritmo == 'taquicardia':
        interpretacion = "Taquicardia sinusal"
        rr_intervals = np.random.normal(loc=rr_mean*0.9, scale=0.06*rr_mean, size=latidos)
        centros = np.cumsum(rr_intervals)
        centros = centros[centros < duracion]
        for centro in centros:
            señal += 0.1 * np.exp(-((t - centro + 0.10)**2) / (2*0.012))
            qrs = 1.2 * np.exp(-((t - centro)**2) / (2*0.002))
            señal += qrs
            señal += 0.25 * np.exp(-((t - centro - 0.18)**2) / (2*0.018))
            qrs_idx = np.argmin(np.abs(t-centro))
            qrs_pos.append(qrs_idx)
    elif ritmo == 'bradicardia':
        interpretacion = "Bradicardia sinusal"
        rr_intervals = np.random.normal(loc=rr_mean*1.1, scale=0.05*rr_mean, size=latidos)
        centros = np.cumsum(rr_intervals)
        centros = centros[centros < duracion]
        for centro in centros:
            señal += 0.18 * np.exp(-((t - centro + 0.13)**2) / (2*0.016))
            qrs = 1.0 * np.exp(-((t - centro)**2) / (2*0.0025))
            señal += qrs
            señal += 0.30 * np.exp(-((t - centro - 0.21)**2) / (2*0.03))
            qrs_idx = np.argmin(np.abs(t-centro))
            qrs_pos.append(qrs_idx)
    elif ritmo == 'asistolia':
        interpretacion = "Asistolia (línea plana)"
        señal[:] = 0
    elif ritmo == 'fv':
        interpretacion = "Fibrilación ventricular"
        señal = 0.5 * np.sin(30 * t + np.cumsum(np.random.randn(len(t))*0.2))
        señal += 0.15 * np.random.randn(len(t))
        qrs_pos = []
    elif ritmo == 'tv':
        interpretacion = "Taquicardia ventricular"
        centros = np.arange(0, duracion, rr_mean*0.6)
        for centro in centros:
            qrs = 1.0 * np.exp(-((t - centro)**2) / (2*0.01))
            señal += qrs
            qrs_idx = np.argmin(np.abs(t-centro))
            qrs_pos.append(qrs_idx)
        señal += 0.07 * np.random.randn(len(t))
    elif ritmo == 'flutter':
        interpretacion = "Flutter auricular"
        # Ondas flutter (3-4 por QRS)
        rr_intervals = np.random.normal(loc=rr_mean, scale=0.03*rr_mean, size=latidos)
        centros = np.cumsum(rr_intervals)
        centros = centros[centros < duracion]
        for centro in centros:
            for f in range(3):
                señal += 0.12 * np.exp(-((t - centro + 0.14 - 0.06*f)**2) / (2*0.005))
            qrs = 1.0 * np.exp(-((t - centro)**2) / (2*0.002))
            señal += qrs
            señal += 0.2 * np.exp(-((t - centro - 0.18)**2) / (2*0.018))
            qrs_idx = np.argmin(np.abs(t-centro))
            qrs_pos.append(qrs_idx)
    elif ritmo == 'fa':
        interpretacion = "Fibrilación auricular"
        # Ondas P irregulares, RR muy variable
        rr_intervals = np.random.normal(loc=rr_mean, scale=0.18*rr_mean, size=latidos)
        centros = np.cumsum(rr_intervals)
        centros = centros[centros < duracion]
        for centro in centros:
            señal += 0.07 * np.random.randn(len(t))
            qrs = 1.0 * np.exp(-((t - centro)**2) / (2*0.002))
            señal += qrs
            qrs_idx = np.argmin(np.abs(t-centro))
            qrs_pos.append(qrs_idx)
    elif ritmo == 'extrasistole':
        interpretacion = "Extrasístole ventricular"
        # Un QRS prematuro
        rr_intervals = np.ones(latidos) * rr_mean
        if latidos > 2:
            rr_intervals[1] = rr_mean * 0.5  # extrasístole temprana
        centros = np.cumsum(rr_intervals)
        centros = centros[centros < duracion]
        for centro in centros:
            señal += 0.15 * np.exp(-((t - centro + 0.12)**2) / (2*0.012))
            qrs = 1.2 * np.exp(-((t - centro)**2) / (2*0.002))
            señal += qrs
            señal += 0.35 * np.exp(-((t - centro - 0.22)**2) / (2*0.025))
            qrs_idx = np.argmin(np.abs(t-centro))
            qrs_pos.append(qrs_idx)
    elif ritmo == 'bloqueo':
        interpretacion = "Bloqueo AV completo"
        # QRS y P disociados
        rr_intervals = np.ones(latidos) * rr_mean
        centros_qrs = np.cumsum(rr_intervals)
        centros_qrs = centros_qrs[centros_qrs < duracion]
        centros_p = np.cumsum(np.ones(latidos)*rr_mean*0.8)
        centros_p = centros_p[centros_p < duracion]
        for centro in centros_p:
            señal += 0.15 * np.exp(-((t - centro + 0.12)**2) / (2*0.012))
        for centro in centros_qrs:
            qrs = 1.2 * np.exp(-((t - centro)**2) / (2*0.002))
            señal += qrs
            qrs_idx = np.argmin(np.abs(t-centro))
            qrs_pos.append(qrs_idx)
    else:
        raise ValueError(f"Ritmo/Arritmia no reconocida: {ritmo}")

    # Ruido fisiológico y artefactos
    if ritmo not in ["asistolia"]:
        señal += 0.04 * np.sin(2*np.pi*0.25*t)  # Respiración
        señal += 0.02 * np.random.randn(len(t)) # Ruido blanco
        if np.random.rand() < 0.3:
            señal += 0.03 * np.sin(2*np.pi*np.random.uniform(1,3)*t)
    señal = señal / np.max(np.abs(señal)) if np.max(np.abs(señal)) > 0 else señal
    return t, señal, qrs_pos, interpretacion
