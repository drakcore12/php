# Diccionario de escenarios de emergencia
ESCENARIOS = {
    'disparo': {
        'descripcion': 'Herida por arma de fuego en el tórax',
        'condiciones_posibles': ['hemorragia', 'dolor', 'perdida_conciencia'],
        'probabilidades': {'hemorragia': 0.9, 'dolor': 1.0, 'perdida_conciencia': 0.3}
    },
    'accidente_auto': {
        'descripcion': 'Accidente vehicular con politraumatismo',
        'condiciones_posibles': ['fractura', 'hemorragia', 'dolor', 'shock_hipovolemico'],
        'probabilidades': {'fractura': 0.8, 'hemorragia': 0.7, 'dolor': 1.0, 'shock_hipovolemico': 0.2}
    },
    'quemadura': {
        'descripcion': 'Quemadura extensa en extremidad superior',
        'condiciones_posibles': ['dolor', 'shock_hipovolemico'],
        'probabilidades': {'dolor': 1.0, 'shock_hipovolemico': 0.5}
    }
}

import random
from datos.datos_diccionarios import CONDICIONES

def generar_condiciones_escenario(nombre_escenario=None):
    escenario = random.choice(list(ESCENARIOS.keys())) if not nombre_escenario else nombre_escenario
    info = ESCENARIOS[escenario]
    posibles = info['condiciones_posibles'][:]
    n_condiciones = random.randint(1, len(posibles))
    seleccionadas = random.sample(posibles, n_condiciones)
    condiciones = []
    for cond in seleccionadas:
        prob = info['probabilidades'].get(cond, 1.0)
        if random.random() < prob:
            cinfo = CONDICIONES.get(cond)
            if cinfo:
                # Manejar condiciones con niveles (ej: hemorragia)
                efecto = cinfo.get('afecta')
                duracion = cinfo.get('duracion')
                if (efecto is None or duracion is None) and 'niveles' in cinfo:
                    nivel = cinfo.get('nivel_inicial', 'leve')
                    efecto = cinfo['niveles'][nivel]['afecta']
                    duracion = cinfo['niveles'][nivel]['duracion']
                if efecto is not None and duracion is not None:
                    condiciones.append({
                        'tipo': 'condicion',
                        'nombre': cond,
                        'efecto': efecto,
                        'duracion_restante': duracion
                    })
                else:
                    print(f"[ADVERTENCIA] La condición '{cond}' no tiene 'afecta' ni 'niveles' definidos en CONDICIONES.")
    return escenario, info['descripcion'], condiciones
