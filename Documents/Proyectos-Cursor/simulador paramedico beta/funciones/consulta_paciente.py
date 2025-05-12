import random

import time

def consulta_paciente(paciente, tipo_consulta, metodo="interrogatorio", tiempo_espera=0):
    """
    Simula una consulta clínica al paciente con mecánica de condiciones y probabilidad de error.
    metodo: 'interrogatorio' (requiere despierto), 'herramienta' (estetoscopio, monitor, etc)
    Retorna: (respuesta_simulada, motivo, tiempo_real_espera)
    """
    despierto = getattr(paciente, 'estado_conciencia', 'despierto') == "despierto"
    consciente = getattr(paciente, 'estado_conciencia', 'consciente') == "consciente"
    dolor = getattr(paciente, 'dolor', 0)
    critico = getattr(paciente, 'estado_critico', False)
    edad_real = getattr(paciente, 'edad', 30)

    # --- Menores de edad: siempre respuesta exacta (adulto a cargo) ---
    if edad_real < 18:
        if tipo_consulta in ["peso", "talla", "edad", "estado_fisico", "frecuencia_cardiaca", "presion_arterial", "spo2", "temperatura", "glucosa", "volumen_sanguineo", "dolor", "bmi"]:
            # Simula tiempo de espera según método
            tiempo = 2 if metodo == "interrogatorio" else 6
            time.sleep(tiempo)
            valor = obtener_valor_real(paciente, tipo_consulta)
            return valor, "Respuesta exacta (adulto a cargo)", tiempo

    # --- Adultos: lógica según método ---
    if metodo == "interrogatorio":
        if not despierto:
            return None, "Paciente no responde (no despierto)", 1
        # Simula tiempo breve
        tiempo = 2
        time.sleep(tiempo)
        error = 0
        # Variaciones y errores posibles
        if not consciente or dolor > 7 or critico:
            if random.random() < 0.5:
                return None, "Paciente no responde por dolor/estado crítico", tiempo
            else:
                error = random.randint(-2, 2)
        # Mentira o error por variables clínicas
        if tipo_consulta == "peso":
            peso = getattr(paciente, 'peso_kg', 70)
            if getattr(paciente, 'estado_nutricional', None) == "obeso" and dolor < 5:
                peso -= 10
                return peso, "Paciente miente por sobrepeso (-10 kg)", tiempo
            return peso + error, "Respuesta con pequeña variación", tiempo
        elif tipo_consulta == "edad":
            edad = edad_real
            if getattr(paciente, 'sexo', 'M') == "F" and edad > 30:
                edad -= 8
                return edad, "Paciente reduce edad (-8 años)", tiempo
            return edad + error, "Respuesta con pequeña variación", tiempo
        elif tipo_consulta == "estado_fisico":
            if dolor > 7 or critico:
                return "Mal, mucho dolor", "Paciente responde con queja por dolor", tiempo
            return getattr(paciente, 'estado_fisico', 'normal'), "Respuesta directa", tiempo
        elif tipo_consulta == "talla":
            talla = getattr(paciente, 'altura_cm', 170)
            return talla + error, "Respuesta con pequeña variación", tiempo
        # Consultas fisiológicas por interrogatorio (pueden fallar)
        elif tipo_consulta in ["frecuencia_cardiaca", "presion_arterial", "spo2", "temperatura", "glucosa"]:
            if random.random() < 0.4:
                return None, "Paciente no sabe responder esta consulta", tiempo
            valor = obtener_valor_real(paciente, tipo_consulta)
            variacion = random.randint(-5, 5)
            return valor + variacion, "Respuesta estimada por paciente", tiempo
        else:
            return None, "Consulta no implementada", tiempo

    elif metodo == "herramienta":
        # Simula tiempo mayor de espera
        tiempo = 6
        time.sleep(tiempo)
        valor = obtener_valor_real(paciente, tipo_consulta)
        if valor is not None:
            return valor, "Respuesta exacta por herramienta", tiempo
        else:
            return None, "Consulta no implementada", tiempo

    return None, "Consulta no implementada", 0

def obtener_valor_real(paciente, tipo_consulta):
    if tipo_consulta == "peso":
        return getattr(paciente, 'peso_kg', 70)
    elif tipo_consulta == "talla":
        return getattr(paciente, 'altura_cm', 170)
    elif tipo_consulta == "edad":
        return getattr(paciente, 'edad', 30)
    elif tipo_consulta == "estado_fisico":
        return getattr(paciente, 'estado_fisico', 'normal')
    elif tipo_consulta == "frecuencia_cardiaca":
        return getattr(paciente, 'signos_vitales', {}).get('frecuencia_cardiaca', 70)
    elif tipo_consulta == "presion_arterial":
        sv = getattr(paciente, 'signos_vitales', {})
        return f"{sv.get('presion_arterial_sistolica', 120)}/{sv.get('presion_arterial_diastolica', 80)}"
    elif tipo_consulta == "spo2":
        return getattr(paciente, 'signos_vitales', {}).get('spo2', 98)
    elif tipo_consulta == "temperatura":
        return getattr(paciente, 'signos_vitales', {}).get('temperatura', 36.5)
    elif tipo_consulta == "glucosa":
        return getattr(paciente, 'glucosa', 90)
    elif tipo_consulta == "volumen_sanguineo":
        return getattr(paciente, 'signos_vitales', {}).get('volumen_sanguineo', 5000)
    elif tipo_consulta == "dolor":
        return getattr(paciente, 'dolor', 0)
    elif tipo_consulta == "bmi":
        peso = getattr(paciente, 'peso_kg', 70)
        altura = getattr(paciente, 'altura_cm', 170)
        if altura > 0:
            return round(peso / ((altura / 100) ** 2), 2)
        else:
            return None
    return None

# --- FUNCIÓN DE PRUEBA ---
def test_consulta_paciente():
    import sys, os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from clases.paciente import Paciente
    p = Paciente.generar_aleatorio()
    print(f"Paciente generado: {p.nombre}, edad: {p.edad}, sexo: {p.sexo}, peso: {p.peso_kg}, talla: {p.altura_cm}, estado nutricional: {p.estado_nutricional}")

    # Ejemplo de consultas individuales (simulación de botones en la GUI)
    print("\n--- Consulta individual: Edad (interrogatorio) ---")
    resp, motivo, t = consulta_paciente(p, "edad", metodo="interrogatorio")
    print(f"Respuesta: {resp} | Motivo: {motivo} | Tiempo: {t}s")

    print("\n--- Consulta individual: Peso (interrogatorio) ---")
    resp, motivo, t = consulta_paciente(p, "peso", metodo="interrogatorio")
    print(f"Respuesta: {resp} | Motivo: {motivo} | Tiempo: {t}s")

    print("\n--- Consulta individual: Frecuencia cardíaca (herramienta) ---")
    resp, motivo, t = consulta_paciente(p, "frecuencia_cardiaca", metodo="herramienta")
    print(f"Respuesta: {resp} | Motivo: {motivo} | Tiempo: {t}s")

    print("\n--- Consulta individual: Presión arterial (herramienta) ---")
    resp, motivo, t = consulta_paciente(p, "presion_arterial", metodo="herramienta")
    print(f"Respuesta: {resp} | Motivo: {motivo} | Tiempo: {t}s")

    print("\n--- Consulta individual: Estado físico (interrogatorio) ---")
    resp, motivo, t = consulta_paciente(p, "estado_fisico", metodo="interrogatorio")
    print(f"Respuesta: {resp} | Motivo: {motivo} | Tiempo: {t}s")

    print("\n--- Consulta individual: Temperatura (herramienta) ---")
    resp, motivo, t = consulta_paciente(p, "temperatura", metodo="herramienta")
    print(f"Respuesta: {resp} | Motivo: {motivo} | Tiempo: {t}s")

def menu_consultas():
    import sys, os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from clases.paciente import Paciente
    p = Paciente.generar_aleatorio()
    print(f"\nPaciente generado: {p.nombre}, edad: {p.edad}, sexo: {p.sexo}, peso: {p.peso_kg}, talla: {p.altura_cm}, estado nutricional: {p.estado_nutricional}\n")
    tipos_consulta = [
        "edad", "peso", "talla", "estado_fisico",
        "frecuencia_cardiaca", "presion_arterial", "spo2", "temperatura", "glucosa"
    ]
    metodos = ["interrogatorio", "herramienta"]
    while True:
        print("\n--- Menú de Consultas Clínicas ---")
        for i, t in enumerate(tipos_consulta, 1):
            print(f"  {i}. {t}")
        print("  0. Salir")
        try:
            op = int(input("Seleccione el número de la consulta: "))
        except ValueError:
            print("Opción inválida.")
            continue
        if op == 0:
            print("Saliendo del menú de consultas.")
            break
        if not (1 <= op <= len(tipos_consulta)):
            print("Opción inválida.")
            continue
        tipo = tipos_consulta[op-1]
        print("Método de consulta:")
        for j, m in enumerate(metodos, 1):
            print(f"  {j}. {m}")
        try:
            mop = int(input("Seleccione el método (1 o 2): "))
        except ValueError:
            print("Opción inválida.")
            continue
        if not (1 <= mop <= len(metodos)):
            print("Opción inválida.")
            continue
        metodo = metodos[mop-1]
        print(f"\nConsultando '{tipo}' por '{metodo}'...")
        resp, motivo, t = consulta_paciente(p, tipo, metodo=metodo)
        print(f"Respuesta: {resp} | Motivo: {motivo} | Tiempo: {t}s\n")

if __name__ == "__main__":
    menu_consultas()
