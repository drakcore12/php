# Simulador Paramédico

Simulador interactivo para entrenamiento paramédico, con módulos de simulación de paciente, administración de medicamentos, monitoreo de ECG y más. Incluye interfaz gráfica, lógica de simulación y pruebas automáticas.

---

## Estructura del Proyecto

```
├── main_tkinter.py        # Ventana principal y lógica de simulación
├── ventana_dosis_medicamento.py
├── ventana_hoja_clinica.py
├── ventana_manual_medicamento.py
├── utils.py               # Utilidades y manejo de mensajes
├── resources.py           # Textos y recursos centralizados
├── test_ecg.py            # Pruebas de lógica ECG
├── test_ventanas.py       # Pruebas automáticas de UI
├── clases/                # Modelos y lógica de dominio
├── datos/                 # Diccionarios y recursos médicos
├── ecg/                   # Procesamiento y visualización de ECG
├── funciones/             # Funciones de simulación médica
├── simulacion/            # Lógica de simulación de paciente
├── requirements.txt
├── README.md
```

---

## Instalación

1. Clona el repositorio y entra al directorio del proyecto.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## Uso

Ejecuta la aplicación principal:
```bash
python main_tkinter.py
```

---

## Testing y Cobertura

Ejecuta todas las pruebas automáticas:
```bash
python -m unittest discover
```

Cobertura de código (opcional):
```bash
pip install coverage
coverage run -m unittest discover
coverage report -m
```

---

## Contribución

- Sigue PEP8 y documenta tus funciones y clases con docstrings.
- Agrega o actualiza pruebas automáticas para cada nuevo feature o bugfix.
- Usa ramas para nuevas funcionalidades.
- Ejecuta los tests y linting antes de hacer push.

---

## Integración Continua (CI)

Puedes usar GitHub Actions para ejecutar los tests automáticamente en cada push. Ejemplo de workflow (`.github/workflows/python-app.yml`):
```yaml
name: Python application
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install coverage flake8
    - name: Lint with flake8
      run: |
        flake8 .
    - name: Run tests
      run: |
        coverage run -m unittest discover
        coverage report -m
```

---

## Ejemplo de Uso

1. Inicia la simulación desde la ventana principal.
2. Solicita exámenes y administra medicamentos.
3. Observa los cambios en la hoja clínica y el monitoreo ECG.

---

## Buenas Prácticas y Documentación

- Todos los módulos están documentados con docstrings.
- Los textos de la UI están centralizados en `resources.py`.
- Los mensajes al usuario y logs se gestionan desde `utils.py`.
- Para dudas o mejoras, abre un issue o pull request.

---

¡Contribuye y ayuda a mejorar el simulador paramédico!
MIT
