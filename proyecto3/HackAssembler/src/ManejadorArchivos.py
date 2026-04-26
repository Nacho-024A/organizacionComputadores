"""
ManejadorArchivos.py - Gestiona la interacción con el sistema de archivos.
Permite seleccionar, leer y escribir archivos ASM y HACK, eliminando
comentarios y líneas vacías, y manejando rutas de entrada y salida.
Autor 1: Andres David Osorio Moreno
Autor 2: Daniel Mauricio Giraldo Moreno
"""
import os

class ManejadorArchivos:
    """Gestiona la selección, lectura y escritura de archivos ASM y HACK."""

    TIPOS_LECTURA = [
        ("Archivos ASM",  "*.asm"),
        ("Archivos HACK", "*.hack"),
        ("Todos",         "*.*"),
    ]

    def _seleccionar_ruta(self, titulo, tipos):
        """Abre un diálogo de archivo; si falla, pide la ruta por consola."""
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            ruta = filedialog.askopenfilename(title=titulo, filetypes=tipos)
            root.destroy()
        except (ImportError, tk.TclError):  # ← específico, no Exception genérico
            print("No se pudo abrir el selector. Ingrese la ruta por consola.")
            ruta = ""

        if not ruta:
            ruta = input(f"{titulo} (ej: C:/ruta/archivo.asm): ")
        if not ruta:
            raise FileNotFoundError("No se seleccionó ningún archivo.")
        return ruta

    def _seleccionar_carpeta(self, titulo):
        """Abre un diálogo de carpeta; si falla, pide la ruta por consola."""
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            ruta = filedialog.askdirectory(title=titulo)
            root.destroy()
        except (ImportError, tk.TclError):
            print("No se pudo abrir el selector. Ingrese la ruta por consola.")
            ruta = ""

        if not ruta:
            ruta = input(f"{titulo} (ej: C:/ruta/carpeta): ")
        if not ruta:
            raise FileNotFoundError("No se seleccionó ninguna carpeta.")
        return ruta

    def leer_archivo(self):
        """Selecciona y lee un archivo, retornando líneas limpias, ruta y extensión."""
        ruta = self._seleccionar_ruta("Selecciona el archivo a traducir", self.TIPOS_LECTURA)
        extension = os.path.splitext(ruta)[1].lower()
        lineas = []

        with open(ruta, "r", encoding="utf-8") as archivo:  # ← encoding explícito
            for linea in archivo:
                if "//" in linea:
                    linea = linea[:linea.index("//")]  # eliminar comentarios
                linea = linea.strip()
                if linea:
                    lineas.append(linea)

        return lineas, ruta, extension

    def escribir_archivo(self, nombre, extension, lineas):
        """Escribe las líneas traducidas en la carpeta seleccionada."""
        carpeta = self._seleccionar_carpeta("Seleccionar carpeta de destino")
        ruta_completa = os.path.join(carpeta, f"{nombre}.{extension}")

        with open(ruta_completa, "w", encoding="utf-8") as archivo:  # ← encoding explícito
            archivo.writelines(linea + "\n" for linea in lineas)

        print(f"Archivo guardado en: {ruta_completa}")
        return ruta_completa