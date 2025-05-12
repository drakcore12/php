import random
from datetime import datetime

def clasificar_edad(edad):
    if edad < 1:
        return "recién_nacido"
    elif edad < 2:
        return "lactante"
    elif edad < 12:
        return "niño"
    elif edad < 18:
        return "adolescente"
    elif edad < 65:
        return "adulto"
    else:
        return "adulto_mayor"

def calcular_bmi(peso, altura_cm):
    if altura_cm <= 0:
        return 0
    return round(peso / ((altura_cm / 100) ** 2), 2)

def obtener_factores_ambientales():
    altitud = random.choice([5, 1500, 2600, 3100])
    temperatura = round(random.uniform(10, 35), 1)
    hora = random.randint(0, 23)
    return altitud, temperatura, hora

def obtener_iluminacion_aleatoria():
    return random.choice(["alta", "media", "baja"])

def obtener_postura_aleatoria():
    return random.choice(["supino", "semisentado"])

def obtener_hidratacion_aleatoria():
    return random.choices(["baja", "normal", "alta"], weights=[0.3, 0.5, 0.2])[0]

def generar_signos_vitales_aleatorios_ambulancia(edad, sexo, peso, altura, actividad_fisica, estado_nutricional, composicion):
    grupo_etario = clasificar_edad(edad)
    bmi = calcular_bmi(peso, altura)
    altitud, temperatura_ambiente, hora = obtener_factores_ambientales()
    iluminacion = obtener_iluminacion_aleatoria()
    postura = obtener_postura_aleatoria()
    hidratacion = obtener_hidratacion_aleatoria()
    rangos_base = {
        "recién_nacido": {"fc": (120, 170), "fr": (30, 80),  "pa_sys": (60, 90),  "pa_dia": (30, 62),
                          "spo2": (95, 100), "temp": (36.1, 37.7)},
        "lactante":      {"fc": (120, 160), "fr": (30, 60),  "pa_sys": (70, 105), "pa_dia": (40, 70),
                          "spo2": (95, 100), "temp": (36.1, 37.5)},
        "niño":          {"fc": (95, 115),  "fr": (20, 30),  "pa_sys": (90, 115), "pa_dia": (50, 80),
                          "spo2": (95, 100), "temp": (36.0, 37.2)},
        "adolescente":   {"fc": (60, 100),  "fr": (12, 20),  "pa_sys": (100, 120),"pa_dia": (60, 80),
                          "spo2": (95, 100), "temp": (36.0, 37.2)},
        "adulto":        {"fc": (60, 100),  "fr": (12, 20),  "pa_sys": (90, 129), "pa_dia": (60, 84),
                          "spo2": (95, 100), "temp": (36.0, 37.0)},
        "adulto_mayor":  {"fc": (55, 90),   "fr": (12, 24),  "pa_sys": (120,140), "pa_dia": (70, 90),
                          "spo2": (92, 98),  "temp": (35.8, 36.8)}
    }
    ajuste_fisico = {
        "alta":  {"fc": (-15, -5), "fr": (-3, -1),  "pa_sys": (-10, -5), "spo2": (0, +1)},
        "media": {"fc": (-5, 0),   "fr": (0, 0),    "pa_sys": (-5, 0),   "spo2": (0, 0)},
        "baja":  {"fc": (+5, +15), "fr": (+2, +5),  "pa_sys": (+5, +10), "spo2": (-3, -1)}
    }
    ajuste_sexo = {
        "M": {"fc": (-3, 0), "pa_sys": (+2, +5)},
        "F": {"fc": (+2, +5), "pa_sys": (-2, 0)}
    }
    ajuste_nutricional = {
        "desnutrido":  {"fc": (+3, +7),  "fr": (+1, +2),  "pa_sys": (-5, 0),  "spo2": (-2, -1)},
        "normal":      {"fc": (0, 0),    "fr": (0, 0),    "pa_sys": (0, 0),   "spo2": (0, 0)},
        "sobrepeso":   {"fc": (+3, +7),  "fr": (0, +2),   "pa_sys": (+2, +6), "spo2": (-1, 0)},
        "obeso":       {"fc": (+5, +10), "fr": (+2, +4),  "pa_sys": (+5, +10),"spo2": (-2, 0)}
    }
    ajuste_iluminacion = {
        "alta":  {"fc": (+3, +5), "pa_sys": (+2, +4)},
        "media": {"fc": (0, 0),   "pa_sys": (0, 0)},
        "baja":  {"fc": (-3, -1), "pa_sys": (-2, -1)}
    }
    ajuste_postura = {
        "supino":      {"fc": (0, 0),   "pa_sys": (0, 0),    "pa_dia": (0, 0)},
        "semisentado": {"fc": (+2, +4), "pa_sys": (-2, 0),   "pa_dia": (-3, 0)}
    }
    ajuste_hidratacion = {
        "baja":   {"fc": (+5, +10), "pa_sys": (-5, 0)},
        "normal": {"fc": (0, 0),    "pa_sys": (0, 0)},
        "alta":   {"fc": (-2, 0),   "pa_sys": (+0, +2)}
    }
    def calc_ajuste_grasa(grasa):
        return (int((grasa - 20) / 2), int((grasa - 20) / 1))
    def calc_ajuste_musculo(musculo):
        return (-int((musculo - 30) / 2), -int((musculo - 30) / 1))
    def calc_ajuste_agua(agua):
        if agua >= 50:
            return (0, 0)
        else:
            return (-int((50 - agua) / 2), -int((50 - agua) / 1))
    def ajuste_ambiental(alt, temp, hora):
        if alt > 1000:
            alt_spo2 = (-int((alt - 1000) / 400), -int((alt - 1000) / 300))
            alt_fr   = (+1, +3)
        else:
            alt_spo2 = (0, 0)
            alt_fr   = (0, 0)
        if temp > 30:
            temp_fc = (+2, +5)
            temp_fr = (+2, +4)
        elif temp < 15:
            temp_fc = (-2, -1)
            temp_fr = (-1, 0)
        else:
            temp_fc = (0, 0)
            temp_fr = (0, 0)
        if 6 <= hora <= 10:
            circ_pa = (+3, +6)
        elif hora >= 22 or hora <= 5:
            circ_pa = (-3, -1)
        else:
            circ_pa = (0, 0)
        if 16 <= hora <= 20:
            circ_temp = (+0.2, +0.4)
        elif 2 <= hora <= 6:
            circ_temp = (-0.3, -0.1)
        else:
            circ_temp = (0, 0)
        return alt_spo2, alt_fr, temp_fc, temp_fr, circ_pa, circ_temp
    base = rangos_base[grupo_etario]
    af  = ajuste_fisico.get(actividad_fisica, {"fc": (0,0), "fr": (0,0), "pa_sys": (0,0), "spo2": (0,0)})
    sx  = ajuste_sexo.get(sexo.upper(), {"fc": (0,0), "pa_sys": (0,0)})
    nut = ajuste_nutricional.get(estado_nutricional, {"fc": (0,0), "fr": (0,0), "pa_sys": (0,0), "spo2": (0,0)})
    alt_spo2, alt_fr, temp_fc, temp_fr, circ_pa, circ_temp = ajuste_ambiental(altitud, temperatura_ambiente, hora)
    ajuste_ilum = ajuste_iluminacion[iluminacion]
    ajuste_post = ajuste_postura[postura]
    ajuste_hidr = ajuste_hidratacion[hidratacion]
    def combinar(r, *ajustes):
        return (
            r[0] + sum(a[0] for a in ajustes),
            r[1] + sum(a[1] for a in ajustes)
        )
    ac_fc = combinar(
        base["fc"],
        af["fc"],
        sx["fc"],
        nut["fc"],
        calc_ajuste_grasa(composicion["grasa"]),
        calc_ajuste_musculo(composicion["musculo"]),
        temp_fc,
        ajuste_ilum["fc"],
        ajuste_hidr["fc"],
        ajuste_post["fc"]
    )
    ac_fr = combinar(
        base["fr"],
        af["fr"],
        nut["fr"],
        alt_fr,
        temp_fr
    )
    ac_sys = combinar(
        base["pa_sys"],
        af["pa_sys"],
        sx["pa_sys"],
        nut["pa_sys"],
        calc_ajuste_grasa(composicion["grasa"]),
        circ_pa,
        ajuste_ilum["pa_sys"],
        ajuste_hidr["pa_sys"],
        ajuste_post["pa_sys"]
    )
    ac_dia = combinar(
        base["pa_dia"],
        ajuste_post.get("pa_dia", (0,0))
    )
    ac_spo2 = combinar(
        base["spo2"],
        af["spo2"],
        calc_ajuste_agua(composicion["agua"]),
        alt_spo2,
        nut["spo2"]
    )
    temp_ajustada = (
        base["temp"][0] + circ_temp[0],
        base["temp"][1] + circ_temp[1]
    )
    def variacion_random(r):
        min_val, max_val = r
        porcentaje = random.uniform(0.01, 0.03)
        delta = int((max_val - min_val) * porcentaje)
        return (min_val - delta, max_val + delta)
    ac_fc   = variacion_random(ac_fc)
    ac_fr   = variacion_random(ac_fr)
    ac_sys  = variacion_random(ac_sys)
    ac_spo2 = variacion_random(ac_spo2)
    temp_ajustada = (round(temp_ajustada[0] - 0.2, 1), round(temp_ajustada[1] + 0.2, 1))
    signos = {
        "frecuencia_cardiaca":          random.randint(*ac_fc),
        "frecuencia_respiratoria":      random.randint(*ac_fr),
        "presion_arterial_sistolica":   random.randint(*ac_sys),
        "presion_arterial_diastolica":  random.randint(*ac_dia),
        "spo2":                         random.randint(*ac_spo2),
        "temperatura":                  round(random.uniform(*temp_ajustada), 1)
    }
    paciente = {
        "edad":                edad,
        "sexo":                sexo,
        "peso_kg":             peso,
        "altura_cm":           altura,
        "bmi":                 bmi,
        "estado_fisico":       actividad_fisica,
        "estado_nutricional":  estado_nutricional,
        "composicion_corporal": composicion,
        "grupo_etario":        grupo_etario,
        "altitud_msnm":        altitud,
        "temperatura_ambiente": temperatura_ambiente,
        "hora_dia":            hora,
        "iluminacion":         iluminacion,
        "postura":             postura,
        "hidratacion":         hidratacion,
        "signos_vitales":      signos
    }
    return paciente
