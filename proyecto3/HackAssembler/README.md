# Proyecto 3 – Hack Assembler & DisAssembler

Implementación de un **Assembler y DisAssembler para la arquitectura Hack** 

Permite la conversión bidireccional entre:

- .asm → .hack
- .hack → .asm

---

##  Ejecución

Desde la carpeta del proyecto:

```bash
python Controlador.py
```

El sistema detecta automáticamente el tipo de archivo y ejecuta el modo correspondiente.

---

## Estructura

- Controlador.py → Punto de entrada  
- Assembler.py → Traducción ASM → HACK  
- DisAssembler.py → Traducción HACK → ASM  
- ManejadorArchivos.py → Manejo de archivos  
- docs/ → Documentación completa  

---

## Documentación

- docs/DESIGN.md → Diagrama de clases  
- docs/API.md → Documentación de clases  
- docs/USER_GUIDE.md → Guía de uso  

---

## Características

- Soporte completo de instrucciones Hack  
- Manejo de labels y variables  
- Símbolos predefinidos  
- Reconstrucción de etiquetas en el DisAssembler  
- Soporte para instrucciones shift (<<, >>)  

---

## Tests

El proyecto incluye casos de prueba en la carpeta `tests/` para validar el funcionamiento del Assembler y DisAssembler.

### Estructura

- tests/asm/ → Archivos de entrada en ensamblador  
- tests/hack/ → Archivos de entrada en binario  

### Cómo probar

1. Ejecuta el programa:
   ```bash
   python Controlador.py
   ```

2. Selecciona un archivo de la carpeta tests/asm/ o tests/hack/

---

### Casos incluidos

- Programa simple sin etiquetas  
- Programa con loop  
- Secuencia Fibonacci

Estos casos permiten validar tanto la traducción ASM → HACK como HACK → ASM.

---

## Autores

- Andres David Osorio Moreno
- Daniel Mauricio Giraldo Moreno