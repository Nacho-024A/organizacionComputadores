# Guía de Usuario

## Descripción

Este programa permite convertir entre:

- Archivos .asm (ensamblador Hack)
- Archivos .hack (binario Hack)

Soporta traducción en ambos sentidos:

- **Assembler:** .asm → .hack
- **DisAssembler:** .hack` → .asm

---

## Requisitos

- Python 3.x instalado
- Sistema operativo con acceso a archivos (Windows, Linux o Mac)

---

## Ejecución del programa

Ejecuta el archivo principal:

```bash
python Controlador.py
```

---

## Flujo de uso

### 1. Selección de archivo

Al ejecutar el programa:

- Se abrirá un selector de archivos (o consola en caso de no ser posible abrir la interfaz)
- Debes elegir un archivo con extensión:
  - .asm → para ensamblar
  - .hack → para desensamblar

---

### 2. Detección automática de modo

El programa detecta automáticamente el tipo de archivo:

- Si es .asm:
  → Se ejecuta el **Assembler**
  → Salida: archivo .hack

- Si es .hack:
  → Se ejecuta el **DisAssembler**
  → Salida: archivo .asm

---

### 3. Generación de salida

El archivo generado se guarda con:

- Mismo nombre base
- Diferente extensión

**Ejemplos:**

| Entrada        | Salida            |
|---------------|--------------------|
| Prog.asm      | Prog.hack          |
| Prog.hack     | ProgDis.asm        |

---

##  Características principales

###  Assembler

- Traducción de instrucciones tipo A (@valor)
- Traducción de instrucciones tipo C (dest=comp;jump)
- Resolución de etiquetas (LABEL)
- Manejo de variables en RAM
- Soporte de símbolos predefinidos:
  - SP, LCL, ARG, THIS, THAT
  - R0 – R15
  - SCREEN, KBD
- Soporte para operaciones:
  -  Shift left (<<)
  -  Shift right (>>)
### Nota:
Las únicas instrucciones de desplazamiento (shift) soportadas se aplican sobre los registros D y M.  
El registro A no se incluye, ya que, según la codificación binaria de la arquitectura Hack, las operaciones como `D<<1` y `A<<1` generan la misma traducción (1110000001000000), lo que produce ambigüedad en el proceso de desensamblado.
Por esta razón, se restringe el uso de instrucciones shift a D y M, garantizando una correspondencia unívoca entre código ensamblador y binario.

---

### DisAssembler

- Traducción de binario a ensamblador
- Reconstrucción de instrucciones A y C
- Detección de saltos
- Inserción automática de etiquetas (LABEL)
- Prioridad de símbolos predefinidos

---

## Manejo de errores

El sistema realiza validaciones en diferentes etapas del proceso para garantizar la correcta traducción:

- Extensión de archivo no válida  
- Archivo no seleccionado o inexistente  
- Instrucciones mal formadas  
- Valores numéricos fuera de rango  
- Campos inválidos en instrucciones tipo C  

En todos los casos, el sistema genera mensajes de error claros y descriptivos, incluyendo sugerencias cuando es posible, con el fin de facilitar la identificación y corrección del problema.

---

## Recomendaciones de uso

- Usar archivos de prueba simples primero
- Verificar que las instrucciones ASM estén bien formadas
- Evitar caracteres inválidos en etiquetas o variables
- Validar que los archivos .hack contengan solo 0 y 1

---

## Ejemplo de uso

### Entrada (.asm)

```asm
@2
D=A
@3
D=D+A
@0
M=D
```

### Salida (.hack)

```hack
0000000000000010
1110110000010000
0000000000000011
1110000010010000
0000000000000000
1110001100001000
```

---

##  Notas finales

- El sistema está diseñado con arquitectura modular
- Permite fácil extensión y mantenimiento
- Ideal para pruebas del computador Hack
