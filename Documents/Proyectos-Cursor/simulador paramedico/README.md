# Simulador de Paciente para Paramédicos

Este proyecto es un simulador de paciente para entrenamiento de paramédicos, desarrollado con React y TypeScript.

## Características

- Simulación de signos vitales en tiempo real
- Diferentes condiciones médicas y tratamientos
- Interfaz intuitiva para aplicar tratamientos
- Posibilidad de realizar exámenes
- Visualización de signos vitales actualizados

## Requisitos previos

- Node.js (versión 14 o superior)
- npm o yarn

## Instalación

1. Clona este repositorio o descarga los archivos del proyecto
2. Navega al directorio del proyecto
3. Instala las dependencias:

```bash
npm install
# o
yarn install
```

## Ejecución

Para iniciar el servidor de desarrollo:

```bash
npm run dev
# o
yarn dev
```

La aplicación estará disponible en [http://localhost:5173](http://localhost:5173).

## Personalización

El simulador puede ser personalizado de diversas maneras:

- **Más condiciones médicas**: Expande la clase `Paciente` con condiciones adicionales.
- **Tratamientos adicionales**: Añade más opciones de tratamiento y sus efectos correspondientes.
- **Exámenes especializados**: Implementa exámenes médicos específicos.

## Estructura del Proyecto

```
simulador-paramedico/
├─ src/
│  ├─ simulacion/
│  │  └─ Paciente.ts      # Clase principal de simulación
│  ├─ components/
│  │  ├─ VitalSigns.tsx   # Componente de signos vitales
│  │  ├─ Controls.tsx     # Controles para tratamientos
│  │  └─ ExamsModal.tsx   # Modal para exámenes
│  ├─ styles/
│  │  └─ index.css        # Estilos globales
│  ├─ App.tsx             # Componente principal
│  └─ main.tsx            # Punto de entrada
├─ index.html             # HTML base
└─ package.json           # Dependencias y scripts
```

## Licencia

Este proyecto es software de código abierto bajo la licencia MIT. 