from datos.datos_diccionarios import CONDICIONES

def evolucionar_nivel_condicion(condicion, signos):
    """
    Recibe un dict de condicion activa (con nivel) y signos actuales.
    Devuelve una nueva condicion con el siguiente nivel si corresponde, o None si ya está en el máximo.
    """
    nombre = condicion['nombre']
    if nombre not in CONDICIONES:
        return None
    info = CONDICIONES[nombre]
    niveles = info.get('niveles')
    if not niveles:
        return None  # No tiene niveles
    niveles_orden = list(niveles.keys())
    nivel_actual = condicion.get('nivel', info.get('nivel_inicial', niveles_orden[0]))
    idx = niveles_orden.index(nivel_actual)
    if idx+1 >= len(niveles_orden):
        return None  # Ya está en el máximo
    nivel_siguiente = niveles_orden[idx+1]
    # Criterio de progresión: por defecto, si la condición persiste toda la duración de su nivel actual
    duracion = condicion.get('duracion_restante', 0)
    # Solo progresar si la duración es un número y llegó a cero
    if isinstance(duracion, (int, float)) and duracion <= 0:
        nueva = condicion.copy()
        nueva['nivel'] = nivel_siguiente
        nueva['efecto'] = niveles[nivel_siguiente]['afecta']
        nueva['duracion_restante'] = niveles[nivel_siguiente]['duracion']
        return nueva
    return None


def evolucionar_condiciones_activas(condiciones, signos):
    """
    Itera sobre todas las condiciones activas y aplica evolución de nivel si corresponde.
    Devuelve una nueva lista de condiciones activas (algunas pueden cambiar de nivel).
    """
    nuevas = []
    for cond in condiciones:
        evolucionada = evolucionar_nivel_condicion(cond, signos)
        if evolucionada:
            nuevas.append(evolucionada)
        else:
            nuevas.append(cond)
    return nuevas
