import random
from funciones.signos_vitales import generar_signos_vitales_aleatorios_ambulancia

class Paciente:
    def __init__(self, nombre, edad, sexo, peso, altura, actividad_fisica, estado_nutricional, composicion, condicion, grupo_etario, factores_ambientales, signos_vitales):
        self.nombre = nombre
        self.edad = edad
        self.sexo = sexo
        self.peso_kg = peso
        self.altura_cm = altura
        self.actividad_fisica = actividad_fisica
        self.estado_nutricional = estado_nutricional
        self.composicion_corporal = composicion
        self.condicion = condicion
        self.grupo_etario = grupo_etario
        self.factores_ambientales = factores_ambientales
        self.signos_vitales = signos_vitales

    def __repr__(self) -> str:
        """
        Representación profesional del paciente para debug y logs.
        Incluye nombre, edad, sexo, peso, altura y signos vitales.
        """
        return (f"Paciente({self.nombre}, {self.edad}a, {self.sexo}, {self.peso_kg}kg, {self.altura_cm}cm, Signos: {self.signos_vitales})")
    @staticmethod
    def generar_nombre_aleatorio(sexo):
        """
        Devuelve un nombre aleatorio según el sexo.
        """
        nombres_hombre = [
            "Juan", "Carlos", "Miguel", "Andrés", "Luis", "Javier", "Pedro", "Santiago", "Alejandro", "Fernando",
            "José", "Ricardo", "Manuel", "Felipe", "Héctor", "Raúl", "Eduardo", "Roberto", "Diego", "Álvaro"
        ]
        nombres_mujer = [
            "María", "Ana", "Laura", "Lucía", "Carmen", "Sofía", "Paula", "Elena", "Isabel", "Gabriela",
            "Patricia", "Verónica", "Daniela", "Claudia", "Sandra", "Rosa", "Beatriz", "Teresa", "Patricia", "Valeria"
        ]
        if sexo.upper() == 'M':
            return random.choice(nombres_hombre)
        else:
            return random.choice(nombres_mujer)

    @classmethod
    def generar_aleatorio(cls):
        """
        Genera un paciente completamente aleatorio y coherente.
        """
        # 1. Edad y grupo etario
        grupos = [
            ("recién_nacido", 0, 0.99),
            ("lactante", 1, 1.99),
            ("niño", 2, 11),
            ("adolescente", 12, 17),
            ("adulto", 18, 64),
            ("adulto_mayor", 65, 90)
        ]
        pesos_grupo = [1, 2, 6, 5, 25, 6]  # Más adultos, menos extremos
        grupo = random.choices(grupos, weights=pesos_grupo)[0]
        edad = round(random.uniform(grupo[1], grupo[2]), 2) if grupo[0] in ["recién_nacido", "lactante"] else random.randint(grupo[1], grupo[2])
        # 2. Sexo
        sexo = random.choice(['M', 'F'])
        # 3. Peso y altura según grupo etario y sexo
        if grupo[0] == "recién_nacido":
            peso = round(random.uniform(2.5, 4.5), 2)
            altura = round(random.uniform(46, 54), 1)
        elif grupo[0] == "lactante":
            peso = round(random.uniform(4, 12), 1)
            altura = round(random.uniform(55, 85), 1)
        elif grupo[0] == "niño":
            peso = round(random.uniform(13, 35), 1)
            altura = round(random.uniform(86, 140), 1)
        elif grupo[0] == "adolescente":
            peso = round(random.uniform(36, 65), 1) if sexo == 'F' else round(random.uniform(38, 75), 1)
            altura = round(random.uniform(141, 170), 1) if sexo == 'F' else round(random.uniform(145, 180), 1)
        elif grupo[0] == "adulto":
            peso = round(random.uniform(45, 80), 1) if sexo == 'F' else round(random.uniform(55, 95), 1)
            altura = round(random.uniform(150, 175), 1) if sexo == 'F' else round(random.uniform(160, 190), 1)
        else:  # adulto mayor
            peso = round(random.uniform(45, 78), 1) if sexo == 'F' else round(random.uniform(50, 85), 1)
            altura = round(random.uniform(145, 170), 1) if sexo == 'F' else round(random.uniform(150, 180), 1)
        # 4. Actividad física
        actividad_fisica = random.choices(['alta', 'media', 'baja'], weights=[2, 5, 3])[0]
        # 5. Estado nutricional (puede depender del BMI)
        bmi = peso / ((altura / 100) ** 2)
        if bmi < 18.5:
            estado_nutricional = 'desnutrido'
        elif bmi < 25:
            estado_nutricional = 'normal'
        elif bmi < 30:
            estado_nutricional = 'sobrepeso'
        else:
            estado_nutricional = 'obeso'
        # 6. Composición corporal según edad, sexo y actividad física
        # Rango base % grasa
        if grupo[0] in ["recién_nacido", "lactante"]:
            grasa = round(random.uniform(13, 20), 1)
            musculo = round(random.uniform(20, 30), 1)
        elif grupo[0] == "niño":
            grasa = round(random.uniform(14, 22), 1)
            musculo = round(random.uniform(22, 35), 1)
        elif grupo[0] == "adolescente":
            if sexo == 'F':
                grasa = round(random.uniform(18, 28), 1)
                musculo = round(random.uniform(28, 38), 1)
            else:
                grasa = round(random.uniform(12, 22), 1)
                musculo = round(random.uniform(32, 44), 1)
        elif grupo[0] == "adulto":
            if actividad_fisica == 'alta':
                grasa = round(random.uniform(15, 22), 1) if sexo == 'M' else round(random.uniform(20, 27), 1)
                musculo = round(random.uniform(38, 46), 1) if sexo == 'M' else round(random.uniform(32, 39), 1)
            elif actividad_fisica == 'media':
                grasa = round(random.uniform(18, 25), 1) if sexo == 'M' else round(random.uniform(23, 31), 1)
                musculo = round(random.uniform(34, 42), 1) if sexo == 'M' else round(random.uniform(29, 36), 1)
            else:  # baja
                grasa = round(random.uniform(22, 30), 1) if sexo == 'M' else round(random.uniform(28, 38), 1)
                musculo = round(random.uniform(30, 38), 1) if sexo == 'M' else round(random.uniform(25, 33), 1)
        else:  # adulto mayor
            grasa = round(random.uniform(22, 32), 1) if sexo == 'M' else round(random.uniform(28, 38), 1)
            musculo = round(random.uniform(26, 36), 1) if sexo == 'M' else round(random.uniform(22, 30), 1)
        # % agua corporal
        if grupo[0] in ["recién_nacido", "lactante"]:
            agua = round(random.uniform(70, 78), 1)
        elif grupo[0] == "niño":
            agua = round(random.uniform(60, 68), 1)
        elif grupo[0] == "adolescente":
            agua = round(random.uniform(55, 65), 1)
        elif grupo[0] == "adulto":
            agua = round(random.uniform(50, 62), 1)
        else:
            agua = round(random.uniform(48, 58), 1)
        composicion = {"grasa": grasa, "musculo": musculo, "agua": agua}
        # 7. Nombre
        nombre = cls.generar_nombre_aleatorio(sexo)
        # 8. Factores ambientales por defecto
        factores_env = {
            'postura': 'supino',
            'iluminacion': 'media'
        }
        # 7. Volumen sanguíneo (signo vital)
        # Rangos por edad y sexo
        if grupo[0] == 'recién_nacido':
            ml_kg = random.randint(80, 90)
        elif grupo[0] == 'lactante':
            ml_kg = random.randint(75, 80)
        elif grupo[0] == 'niño':
            ml_kg = random.randint(70, 75)
        elif grupo[0] == 'adolescente':
            ml_kg = random.randint(70, 75) if sexo == 'M' else random.randint(65, 70)
        elif grupo[0] == 'adulto':
            ml_kg = random.randint(70, 75) if sexo == 'M' else random.randint(65, 70)
        else:  # adulto mayor
            ml_kg = random.randint(68, 73) if sexo == 'M' else random.randint(63, 68)
        hidratacion = 'normal'
        if 'hidratacion' in factores_env:
            hidratacion = factores_env['hidratacion']
        if hidratacion == 'baja':
            ml_kg = round(ml_kg * random.uniform(0.93, 0.97), 2)
        elif hidratacion == 'alta':
            ml_kg = round(ml_kg * random.uniform(1.03, 1.07), 2)
        volumen_sanguineo = round(peso * ml_kg, 1)
        # 9. Condición
        condicion = None
        # 8. Signos vitales aleatorios
        signos_vitales = generar_signos_vitales_aleatorios_ambulancia(
            edad=edad,
            sexo=sexo,
            peso=peso,
            altura=altura,
            actividad_fisica=actividad_fisica,
            estado_nutricional=estado_nutricional,
            composicion=composicion
        )
        signos_vitales['volumen_sanguineo'] = volumen_sanguineo
        # Instanciar paciente
        return cls(
            nombre=nombre,
            edad=edad,
            sexo=sexo,
            peso=peso,
            altura=altura,
            actividad_fisica=actividad_fisica,
            estado_nutricional=estado_nutricional,
            composicion=composicion,
            condicion=condicion,
            grupo_etario=grupo[0],
            factores_ambientales=factores_env,
            signos_vitales=signos_vitales
        )



