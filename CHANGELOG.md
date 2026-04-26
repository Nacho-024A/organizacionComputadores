# Historial de cambios

## [1.0.0] - 2026-04-25
### Agregado
- Estructura inicial del repositorio
- Carpetas proyecto2 y proyecto3

## [2.0.0] - 2026-04-25

### Agregado
- Implementación completa del Assembler (ASM → HACK)
- Implementación completa del DisAssembler (HACK → ASM)
- Soporte para instrucciones tipo A y C
- Manejo de etiquetas (labels) en ROM
- Manejo de variables en RAM
- Soporte para símbolos predefinidos (SP, LCL, ARG, THIS, THAT, SCREEN, KBD, R0–R15`)
- Soporte para operaciones de desplazamiento (<<, >>)
- Reconstrucción automática de etiquetas en el DisAssembler
- Detección de destinos de salto

### Mejorado
- Separación de responsabilidades en clases (Controlador, Assembler, DisAssembler, ManejadorArchivos)
- Reutilización de tablas de traducción en el DisAssembler
- Manejo de errores con mensajes descriptivos
- Validación de instrucciones y formatos

### Documentación
- Creación de DESIGN.md con diagrama de clases en Mermaid
- Creación de API.md con documentación de clases y métodos
- Creación de USER_GUIDE.md con guía de uso
- Creación de README.md como punto de entrada del proyecto

## [2.0.1] - 2026-04-25

### Agregado
- Carpeta de pruebas (tests/) con casos de prueba para ASM y HACK
- Casos de prueba adicionales (incluyendo Fibonacci)
- Carpeta outputs/ con resultados generados por el programa
- Estructura organizada para validación de resultados (asm/, hack/, expected/, outputs/)

### Mejorado
- Organización del repositorio para facilitar pruebas y validación
- Documentación del uso de tests y outputs en README

### Corregido
- Eliminación de archivos temporales (__pycache__, .pyc) del repositorio
- Limpieza de archivos innecesarios (.gitkeep en carpetas con contenido)