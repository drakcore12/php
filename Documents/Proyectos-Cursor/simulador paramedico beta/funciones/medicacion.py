import re
from datos.datos_diccionarios import medicamentos_als

def calcular_dosis_ideal(medicamento, peso):
    """
    Calcula la dosis ideal para el medicamento y peso dado.
    Devuelve (dosis_ideal, unidad, rango, motivo)
    """
    info = medicamentos_als.get(medicamento)
    if not info:
        return None, None, None, "Medicamento no encontrado"
    formula = info['formula']
    unidad = info['unidad']
    rango = info['rango']
    # Fórmulas típicas: 'peso * 0.01', 'peso * 5', 'fija', 'peso * 0.5-1'
    if 'peso' in formula:
        # Soporta rangos tipo 'peso * 0.5-1'
        m = re.match(r"peso \* ([0-9.]+)(?:-([0-9.]+))?", formula)
        if m:
            minf = float(m.group(1))
            maxf = float(m.group(2)) if m.group(2) else minf
            min_dosis = peso * minf
            max_dosis = peso * maxf
            return (min_dosis, max_dosis, unidad, rango, "Dosis calculada por peso")
    if formula == 'fija':
        return (None, None, unidad, rango, "Dosis fija, ver rango")
    return (None, None, unidad, rango, "Fórmula no reconocida")

def administrar_medicamento(paciente, medicamento, dosis, via, procedimientos_realizados):
    """
    Simula la administración de un medicamento y evalúa si es correcto según vía y dosis.
    Devuelve un dict con resultado, motivo, efectos y advertencias.
    """
    info = medicamentos_als.get(medicamento)
    if not info:
        return {'ok': False, 'motivo': 'Medicamento no encontrado'}
    # Vías IV/IO requieren procedimiento previo
    if via.lower() in ['iv', 'io'] and via.lower() not in procedimientos_realizados:
        return {'ok': False, 'motivo': f"No hay acceso {via.upper()} disponible"}
    # Calcula dosis ideal
    peso = getattr(paciente, 'peso_kg', 70) if hasattr(paciente, 'peso_kg') else paciente.get('peso_kg', 70)
    min_dosis, max_dosis, unidad, rango, motivo = calcular_dosis_ideal(medicamento, peso)
    # Verifica dosis
    if min_dosis is not None and max_dosis is not None:
        if min_dosis <= dosis <= max_dosis:
            resultado = 'Dosis correcta'
            ok = True
        elif dosis < min_dosis:
            resultado = 'Subdosificación'
            ok = False
        else:
            resultado = 'Sobredosificación'
            ok = False
    else:
        resultado = 'Dosis fuera de fórmula, revisar rango'
        ok = False
    return {
        'ok': ok,
        'motivo': resultado,
        'dosis_ideal': (min_dosis, max_dosis, unidad),
        'rango': rango,
        'efectos_secundarios': info['efectos_secundarios'] if not ok else [],
        'info': motivo
    }

def menu_medicacion(paciente, procedimientos_realizados):
    print("\n--- Administración de Medicamentos ALS ---")
    from datos.datos_diccionarios import medicamentos_als
    meds = list(medicamentos_als.keys())
    for i, m in enumerate(meds, 1):
        print(f"  {i}. {medicamentos_als[m]['nombre']}")
    print("  0. Salir")
    op = int(input("Seleccione medicamento: "))
    if op == 0:
        return
    if not (1 <= op <= len(meds)):
        print("Opción inválida.")
        return
    med = meds[op-1]
    via = input("Ingrese vía de administración (IV/IO/IM/SC/SL/IN/inhalatoria/oral): ").strip().lower()
    peso = getattr(paciente, 'peso_kg', 70) if hasattr(paciente, 'peso_kg') else paciente.get('peso_kg', 70)
    min_dosis, max_dosis, unidad, rango, motivo = calcular_dosis_ideal(med, peso)
    print(f"\nPeso paciente: {peso} kg")
    print(f"Dosis recomendada: {min_dosis:.2f} - {max_dosis:.2f} {unidad} (rango: {rango})")
    dosis = float(input(f"Ingrese dosis a administrar ({unidad}): "))
    resultado = administrar_medicamento(paciente, med, dosis, via, procedimientos_realizados)
    print(f"\nResultado: {resultado['motivo']}")
    if not resultado['ok']:
        print(f"Advertencia/efectos secundarios: {resultado['efectos_secundarios']}")
    else:
        print("Administración exitosa.")
    print()
