"""
Assembler.py - Implementa el traductor de código ASM a binario Hack.
Gestiona la tabla de símbolos, procesa etiquetas en una primera pasada
y traduce instrucciones tipo A y C (incluyendo operaciones shift << y >>).
Autor 1: Andres David Osorio Moreno
Autor 2: Daniel Mauricio Giraldo Moreno
"""
import re
import difflib
import itertools

class Assembler:
    """Traduce código ASM a binario HACK (instrucciones tipo A y C)."""

    # ── Constantes ────────────────────────────────────────────────────────

    _PATRON_SIMBOLO      = re.compile(r'^[a-zA-Z_.$:][a-zA-Z0-9_.$:]*$')
    _DIR_VARIABLE_INICIO = 16

    _SIMBOLOS_BASE = {
        "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
        "SCREEN": 16384, "KBD": 24576,
        **{f"R{i}": i for i in range(16)},
    }

    _ACOMP = {
        "0":"0101010", "1":"0111111", "-1":"0111010",
        "D":"0001100", "A":"0110000", "!D":"0001101",
        "!A":"0110001", "-D":"0001111", "-A":"0110011",
        "D+1":"0011111", "A+1":"0110111", "D-1":"0001110",
        "A-1":"0110010", "D+A":"0000010", "D-A":"0010011",
        "A-D":"0000111", "D&A":"0000000", "D|A":"0010101",
        "D<<1":"0000001", "D>>1":"0000011",
        "M":"1110000", "!M":"1110001", "-M":"1110011",
        "M+1":"1110111", "M-1":"1110010", "D+M":"1000010",
        "D-M":"1010011", "M-D":"1000111", "D&M":"1000000",
        "D|M":"1010101", "M<<1":"1000001", "M>>1":"1000011",
    }
    _DEST = {
        "NULL":"000", "M":"001", "D":"010", "MD":"011",
        "A":"100",  "AM":"101", "AD":"110", "AMD":"111",
    }
    _JUMP = {
        "NULL":"000", "JGT":"001", "JEQ":"010", "JGE":"011",
        "JLT":"100",  "JNE":"101", "JLE":"110", "JMP":"111",
    }

    # ── API pública ───────────────────────────────────────────────────────

    def ensamblar(self, lineas):
        """Convierte una lista de líneas ASM a una lista de strings binarios de 16 bits."""
        tabla   = self._tabla_simbolos()
        lineas  = self._primera_pasada(lineas, tabla)
        dir_var = self._DIR_VARIABLE_INICIO
        resultado = []

        for num, linea in enumerate(lineas, start=1):
            tipo = self._detectar_tipo(linea)

            if tipo == "A":
                binario, dir_var = self._traducir_a(linea, tabla, dir_var)
            elif tipo == "C":
                binario = self._traducir_c(linea)
            else:
                raise SyntaxError(
                    f"Instrucción inválida en línea {num}: '{linea}'"
                )
            resultado.append(binario)

        return resultado

    # ── Detección de tipo ─────────────────────────────────────────────────

    def _detectar_tipo(self, linea):
        """Retorna 'A' o 'C' según la instrucción."""
        if linea.startswith("@"):
            return "A"
        if "<<" in linea or ">>" in linea or "=" in linea or ";" in linea:
            return "C"
        raise ValueError(f"Instrucción inválida: '{linea}'")

    # ── Tabla de símbolos ─────────────────────────────────────────────────

    def _tabla_simbolos(self):
        """Retorna una copia fresca de los símbolos predefinidos."""
        return dict(self._SIMBOLOS_BASE)

    def _primera_pasada(self, lineas, tabla):
        """Registra etiquetas (LOOP) en la tabla y las elimina de las líneas."""
        limpias    = []
        contador   = 0

        for linea in lineas:
            if linea.startswith("(") and linea.endswith(")"):
                etiqueta = linea[1:-1]

                if not etiqueta.isupper() or not self._PATRON_SIMBOLO.match(etiqueta):
                    raise SyntaxError(
                        f"Etiqueta inválida: '{linea}'. "
                        f"Debe estar en mayúsculas y contener solo letras, números o '_'.\n"
                        f"Ejemplo válido: (LOOP), (END), (IF_TRUE)"
                    )
                if etiqueta in tabla:
                    raise SyntaxError(f"Etiqueta duplicada: '{etiqueta}'.")

                tabla[etiqueta] = contador
                continue

            limpias.append(linea)
            contador += 1

        return limpias

    # ── Traducción tipo A ─────────────────────────────────────────────────

    def _traducir_a(self, instruccion, tabla, dir_var):
        """Convierte '@valor' a 16 bits. Retorna (binario, dir_var actualizada)."""
        valor = instruccion.strip().replace(" ", "")[1:]  # quitar '@'

        if valor.isdigit():
            numero = int(valor)
            if not 0 <= numero <= 32767:
                raise ValueError(
                    f"Número fuera de rango: {numero}. Debe estar entre 0 y 32767."
                )
            return "0" + format(numero, "015b"), dir_var

        if not self._PATRON_SIMBOLO.match(valor):
            raise SyntaxError(
                f"Símbolo inválido: '{valor}'. "
                f"Debe comenzar con letra o '_' y contener solo letras, números o '_'."
            )

        if valor not in tabla:
            tabla[valor] = dir_var   # nueva variable → siguiente dirección libre
            dir_var += 1

        return "0" + format(tabla[valor], "015b"), dir_var

    # ── Traducción tipo C ─────────────────────────────────────────────────

    def _traducir_c(self, instruccion):
        """Convierte una instrucción tipo C a 16 bits."""
        instruccion = instruccion.strip().replace(" ", "").upper()
        dest, comp, jump = self._separar_c(instruccion)

        bits_dest = self._depurar_c("DEST", dest, self._DEST)
        bits_comp = self._depurar_c("COMP", comp, self._ACOMP)
        bits_jump = self._depurar_c("JUMP", jump, self._JUMP)

        return f"111{bits_comp}{bits_dest}{bits_jump}"

    def _separar_c(self, instruccion):
        """Separa 'dest=comp;jump' en sus tres campos."""
        dest = jump = "NULL"
        comp = ""

        if "<<" in instruccion or ">>" in instruccion:  # caso shift
            if ";" in instruccion:
                raise SyntaxError("Instrucción Shift inválida: no se permite campo JUMP.")
            dest, comp = instruccion.split("=") if "=" in instruccion else ("NULL", instruccion)
            return dest, comp, "NULL"

        if "=" in instruccion:
            dest, instruccion = instruccion.split("=", 1)
        if ";" in instruccion:
            comp, jump = instruccion.split(";", 1)
        else:
            comp = instruccion

        return dest, comp, jump

    def _depurar_c(self, campo, valor, diccionario):
        """Valida un campo tipo C y retorna sus bits; lanza ValueError con sugerencia si falla."""
        if not valor:
            valor = "NULL"
        if valor in diccionario:
            return diccionario[valor]

        sugerencias = []

        if campo == "DEST" and all(c in "ADM" for c in valor):
            # ← bug corregido: el for ahora está dentro del if
            for p in itertools.permutations(valor):
                candidato = "".join(p)
                if candidato in diccionario:
                    sugerencias.append(candidato)

        elif campo == "COMP":
            for op in ("+", "&", "|"):
                if op in valor:
                    partes = valor.split(op)
                    if len(partes) == 2:
                        invertido = partes[1] + op + partes[0]
                        if invertido in diccionario:
                            sugerencias.append(invertido)

        if not sugerencias:
            sugerencias = difflib.get_close_matches(valor, diccionario.keys(), n=1, cutoff=0.5)

        if sugerencias:
            raise ValueError(
                f"Campo {campo} inválido: '{valor}'. ¿Quisiste poner '{sugerencias[0]}'?"
            )
        raise ValueError(
            f"Campo {campo} inválido: '{valor}'. Revisar la sintaxis."
        )