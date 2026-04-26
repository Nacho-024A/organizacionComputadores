"""
DisAssembler.py - Implementa el desensamblador de código binario HACK a ASM.
Traduce instrucciones tipo A y C, reconstruye símbolos y etiquetas,
e identifica destinos de salto para regenerar labels en ROM.
Autor 1: Andres David Osorio Moreno
Autor 2: Daniel Mauricio Giraldo Moreno
"""
from Assembler import Assembler  # reutiliza _ACOMP, _DEST, _JUMP y _SIMBOLOS_BASE

class DisAssembler:
    """Traduce código binario HACK a instrucciones ASM (tipo A y C)."""

    # Diccionarios inversos: bits → mnemónico
    _ACOMP_BIN = {v: k for k, v in Assembler._ACOMP.items()}
    _DEST_BIN  = {v: k for k, v in Assembler._DEST.items()}
    _JUMP_BIN  = {v: k for k, v in Assembler._JUMP.items()}

    # Orden de prioridad para recuperar símbolos: VM > Rx > número directo
    _PRIORIDAD_SIMBOLOS = [
        "SP", "LCL", "ARG", "THIS", "THAT", "SCREEN", "KBD",
        *[f"R{i}" for i in range(16)],
    ]

    # ── API pública ───────────────────────────────────────────────────────

    def desensamblar(self, lineas):
        """Convierte una lista de strings binarios de 16 bits a líneas ASM."""
        tabla    = dict(Assembler._SIMBOLOS_BASE)
        destinos = self._detectar_destinos(lineas)
        asm_temp = []

        for num, linea in enumerate(lineas, start=1):
            linea = linea.strip().replace(" ", "")
            self._validar_binario(linea, num)

            if linea.startswith("0"):
                asm_temp.append(self._traducir_a(linea, tabla, destinos, num - 1, lineas))
            elif linea.startswith("111"):
                asm_temp.append(self._traducir_c(linea))
            else:
                raise SyntaxError(
                    f"Instrucción binaria inválida en línea {num}: '{linea}'. "
                    f"Debe comenzar con '0' (tipo A) o '111' (tipo C)."
                )

        return self._insertar_etiquetas(asm_temp, destinos)

    # ── Validación ────────────────────────────────────────────────────────

    def _validar_binario(self, linea, num):
        """Lanza ValueError si la línea no es un binario de 16 bits válido."""
        if len(linea) != 16 or not all(b in "01" for b in linea):
            raise ValueError(
                f"Línea {num}: '{linea}' no es un binario de 16 bits válido."
            )

    # ── Traducción tipo A ─────────────────────────────────────────────────

    def _traducir_a(self, binario, tabla, destinos, idx, lineas):

        numero = int(binario, 2)

        usar_label = False

        # FILTRO: solo si la siguiente instrucción es salto
        if idx + 1 < len(lineas):

            siguiente = lineas[idx + 1].strip().replace(" ", "")

            if (
                siguiente.startswith("111")
                and siguiente[13:16] != "000"
                and numero in destinos
            ):
                usar_label = True

        if usar_label:
            return f"@{destinos[numero]}"

        tabla_invertida = {}

        for simbolo in self._PRIORIDAD_SIMBOLOS:
            if simbolo in tabla:
                valor = tabla[simbolo]

                # Solo guardar si aún no existe
                if valor not in tabla_invertida:
                    tabla_invertida[valor] = simbolo

        if numero in tabla_invertida:
            return f"@{tabla_invertida[numero]}"

        # Número normal (variable RAM)
        return f"@{numero}"

    # ── Traducción tipo C ─────────────────────────────────────────────────

    def _traducir_c(self, binario):
        """Convierte 16 bits tipo C a su mnemónico ASM."""
        b_comp = binario[3:10]
        b_dest = binario[10:13]
        b_jump = binario[13:16]

        if b_comp not in self._ACOMP_BIN:
            raise ValueError(f"Bits COMP inválidos: '{b_comp}'")
        if b_dest not in self._DEST_BIN:
            raise ValueError(f"Bits DEST inválidos: '{b_dest}'")
        if b_jump not in self._JUMP_BIN:
            raise ValueError(f"Bits JUMP inválidos: '{b_jump}'")

        comp = self._ACOMP_BIN[b_comp]
        dest = self._DEST_BIN[b_dest]
        jump = self._JUMP_BIN[b_jump]

        instruccion = comp if dest == "NULL" else f"{dest}={comp}"
        if jump != "NULL":
            instruccion = f"{instruccion};{jump}"
        return instruccion

    # ── Inserción de etiquetas ────────────────────────────────────────────

    def _insertar_etiquetas(self, lineas_asm, destinos):

        resultado = []
        rom = 0

        for linea in lineas_asm:

            if rom in destinos and rom != 0:
                resultado.append(f"({destinos[rom]})")

            resultado.append(linea)

            rom += 1

        return resultado

    # ── Detección de etiquetas ────────────────────────────────────────────
    def _detectar_destinos(self, lineas):

        destinos = set()

        for i in range(len(lineas) - 1):

            actual = lineas[i].strip().replace(" ", "")
            siguiente = lineas[i + 1].strip().replace(" ", "")

            # Debe ser instrucción A
            if not actual.startswith("0"):
                continue

            # Debe ser instrucción C con salto
            if not siguiente.startswith("111"):
                continue

            jump_bits = siguiente[13:16]

            if jump_bits == "000":
                continue

            direccion = int(actual, 2)

            # Debe apuntar dentro del ROM
            if direccion >= len(lineas):
                continue

            # Evitar ROM 0
            if direccion == 0:
                continue

            destinos.add(direccion)

        return {
            direccion: f"LABEL_{idx}"
            for idx, direccion in enumerate(sorted(destinos))
        }