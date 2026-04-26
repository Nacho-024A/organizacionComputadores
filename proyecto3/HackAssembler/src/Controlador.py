"""
Controlador.py - Punto de entrada del sistema. Orquesta la lectura del archivo,
detecta su tipo (.asm o .hack) y delega el proceso al Assembler o DisAssembler.
Autor 1: Andres David Osorio Moreno
Autor 2: Daniel Mauricio Giraldo Moreno
"""
import os
from ManejadorArchivos import ManejadorArchivos
from Assembler import Assembler
from DisAssembler import DisAssembler

class Controlador:
    """Punto de entrada: lee el archivo, detecta la extensión y delega la traducción."""

    _EXTENSIONES_VALIDAS = {".asm", ".hack"}

    def __init__(self):
        self.manejador    = ManejadorArchivos()
        self.assembler    = Assembler()
        self.disassembler = DisAssembler()

    def ejecutar(self):
        """Orquesta el flujo completo: leer → traducir → escribir."""
        lineas, ruta, extension = self.manejador.leer_archivo()
        nombre_base = os.path.splitext(os.path.basename(ruta))[0]

        if extension not in self._EXTENSIONES_VALIDAS:
            raise ValueError(
                f"Extensión '{extension}' no válida. "
                f"Solo se aceptan archivos .asm o .hack."
            )

        if extension == ".asm":
            print("Modo: ASM → HACK")
            resultado = self.assembler.ensamblar(lineas)
            self.manejador.escribir_archivo(nombre_base, "hack", resultado)

        else:  # .hack
            print("Modo: HACK → ASM")
            resultado = self.disassembler.desensamblar(lineas)
            self.manejador.escribir_archivo(nombre_base + "Dis", "asm", resultado)


if __name__ == "__main__":
    Controlador().ejecutar()