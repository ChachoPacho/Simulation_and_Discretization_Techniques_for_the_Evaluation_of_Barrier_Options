# Tesis: Valoración de Opciones Barrera

Este repositorio contiene el código LaTeX y el material de referencia para el Trabajo Final de Carrera (TFC) sobre la valoración de opciones financieras del tipo barrera.

## Estructura del Proyecto

- `code/`: Contiene los archivos fuente de LaTeX para la tesis.
  - `main.tex`: Archivo principal del documento.
  - `03_intro/`: Introducción y objetivos.
  - `04_antecedentes/`: Marco teórico y antecedentes.
  - `tesis.bib`: Bibliografía en formato BibTeX.
- `Material/`: Documentación y papers de referencia utilizados en la investigación.
- `out/`: Directorio de salida para los archivos compilados.

## Compilación

Para compilar el documento principal, se recomienda el uso de `latexmk` desde el directorio `code/`:

```bash
cd code
latexmk -pdf main.tex
```

Asegúrate de tener instaladas las dependencias necesarias de LaTeX (TeX Live o MikTeX) y los paquetes especificados en `main.tex` y `conf.tex`.

## Contenidos Principales

La tesis aborda tres casos de estudio fundamentales:
1. **Modelo Continuo de Black-Scholes**: Soluciones cerradas para opciones europeas y bases para simulaciones Monte Carlo.
2. **Modelos Discretos (Binomial y Trinomial)**: Uso de mallas adaptativas para mejorar la precisión en la valoración cerca de la barrera.
3. **Replicación Estática**: Cobertura de opciones barrera mediante portafolios de opciones vanilla.
