# Documentacion de Clases
## Descripción General

Este proyecto implementa un **Assembler y DisAssembler para la arquitectura Hack**, permitiendo la conversión bidireccional entre:

- Código ensamblador (.asm)
- Código binario (.hack)

El sistema está compuesto por cuatro clases principales:

- Controlador → Orquestación del flujo  
- ManejadorArchivos → Entrada/Salida  
- Assembler → Traducción ASM → HACK  
- DisAssembler → Traducción HACK → ASM  

---

# Clase: Controlador

## Descripción
Clase principal del sistema. Actúa como punto de entrada, detecta el tipo de archivo y delega el proceso de traducción.

### ejecutar() → void

Ejecuta el flujo completo del programa:

1. Lee el archivo de entrada  
2. Detecta su extensión  
3. Ejecuta el assembler o disassembler  
4. Guarda el resultado  

**Excepciones:**
- ValueError: Si la extensión no es válida  
- FileNotFoundError: Si no se selecciona archivo  

---

# Clase: ManejadorArchivos

## Descripción
Encapsula la interacción con el sistema de archivos, incluyendo selección, lectura y escritura.

### leer_archivo() → (list, str, str)

Lee un archivo .asm o .hack.

**Retorna:**
- list: Líneas limpias del archivo  
- str: Ruta del archivo  
- str: Extensión del archivo  

**Procesamiento:**
- Elimina comentarios (//)  
- Ignora líneas vacías  

**Excepciones:**
- FileNotFoundError: Si no se selecciona archivo  

---

### escribir_archivo(nombre: str, extension: str, lineas: list) → str

Escribe el archivo traducido.

**Parámetros:**
- nombre: Nombre base del archivo  
- extension: Extensión de salida  
- lineas: Contenido a escribir  

**Retorna:**
- str: Ruta completa del archivo generado  

---

### _seleccionar_ruta(titulo: str, tipos: list) → str

Selecciona un archivo mediante interfaz gráfica o consola.

**Retorna:**
- str: Ruta del archivo  

---

### _seleccionar_carpeta(titulo: str) → str

Selecciona una carpeta destino.

**Retorna:**
- str: Ruta de la carpeta  

---

# Clase: Assembler

## Descripción
Traduce código ensamblador Hack a binario de 16 bits.

Implementa:
- Resolución de símbolos  
- Manejo de variables  
- Traducción de instrucciones tipo A y C  
- Soporte para operaciones shift (<<, >>)  

---

### ensamblar(lineas: list) → list

Convierte instrucciones ASM a binario HACK.

**Proceso:**
1. Primera pasada → etiquetas  
2. Segunda pasada → traducción  

**Retorna:**
- list: Instrucciones binarias de 16 bits  

---

### _primera_pasada(lineas: list, tabla: dict) → list

Registra etiquetas en la tabla de símbolos.

**Retorna:**
- list: Líneas sin etiquetas  

**Excepciones:**
- SyntaxError: Etiqueta inválida o duplicada  

---

### _traducir_a(instr: str, tabla: dict, dir_var: int) → (str, int)

Traduce instrucciones tipo A (@valor).

**Retorna:**
- str: Binario de 16 bits  
- int: Nueva dirección de variable  

**Excepciones:**
- ValueError: Número fuera de rango  
- SyntaxError: Símbolo inválido  

---

### _traducir_c(instr: str) → str

Traduce instrucciones tipo C.

**Retorna:**
- str: Binario de 16 bits  

---

### _separar_c(instr: str) → (str, str, str)

Divide instrucción en:
- dest  
- comp  
- jump  

---

### _depurar_c(campo: str, valor: str, diccionario: dict) → str

Valida componentes de instrucción C.

**Retorna:**
- str: Bits correspondientes  

**Excepciones:**
- ValueError: Campo inválido con sugerencias  

---

# Clase: DisAssembler

## Descripción
Traduce código binario Hack a ensamblador.

Incluye:
- Traducción de instrucciones A y C  
- Reconstrucción de etiquetas  
- Detección de saltos  

---

### desensamblar(lineas: list) → list

Convierte binario a ASM.

**Proceso:**
1. Validación de binarios  
2. Traducción A/C  
3. Inserción de etiquetas  

**Retorna:**
- list: Código ASM  

---

### _traducir_a(binario: str, tabla: dict, destinos: dict, idx: int, lineas: list) → str

Traduce instrucciones tipo A.

**Características:**
- Detecta uso de labels  
- Prioriza símbolos predefinidos  

---

### _traducir_c(binario: str) → str

Traduce instrucciones tipo C.

**Excepciones:**
- ValueError: Bits inválidos  

---

### _detectar_destinos(lineas: list) → dict

Identifica direcciones de salto.

**Retorna:**
- dict: Direcciones → etiquetas generadas  

---

### _insertar_etiquetas(lineas: list, destinos: dict) → list

Inserta etiquetas en el código ASM.

**Retorna:**
- list: Código con labels  

---

# Notas de Diseño

- Arquitectura modular con separación de responsabilidades  
- Assembler basado en algoritmo de dos pasadas  
- Reutilización de tablas en DisAssembler para consistencia  
- Soporte extendido para instrucciones shift (<<, >>)  
- Manejo robusto de errores con mensajes claros  