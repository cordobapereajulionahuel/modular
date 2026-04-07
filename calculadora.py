import os
import requests
import json
from pathlib import Path
import importlib.util

URL_REPO = "https://raw.githubusercontent.com/cordobapereajulionahuel/modular/main/"
MODULOS_DIR = Path("modulos")
VERSIONES_FILE = Path("versiones.json")

class SistemaModular:
    def __init__(self):
        MODULOS_DIR.mkdir(exist_ok=True)
        self.versiones_locales = self.cargar_local()
        self.modulos_cargados = {}

    def cargar_local(self):
        if VERSIONES_FILE.exists():
            with open(VERSIONES_FILE) as f:
                return json.load(f)
        return {}

    def guardar_local(self):
        with open(VERSIONES_FILE, "w") as f:
            json.dump(self.versiones_locales, f, indent=2)

    def obtener_remoto(self):
        r = requests.get(URL_REPO + "versiones.json")
        return r.json()

    def descargar(self, nombre):
     url = URL_REPO + nombre + ".py"
     print("Descargando:", url)

     r = requests.get(url)
     print("Status:", r.status_code)

     if r.status_code != 200:
        print("❌ ERROR: archivo no encontrado en el repo")
        return

     with open(MODULOS_DIR / f"{nombre}.py", "wb") as f:
        f.write(r.content)

    def actualizar(self):
     remoto = self.obtener_remoto()
     print("Remoto:", remoto)
     print("Local:", self.versiones_locales)

     for modulo, version in remoto.items():
        local = self.versiones_locales.get(modulo, 0)

        print(f"Comparando {modulo}: local={local}, remoto={version}")

        if version > local:
            print(f"Actualizando {modulo}...")
            self.descargar(modulo)
            self.versiones_locales[modulo] = version

     self.guardar_local()
    def cargar_modulos(self):
        for archivo in MODULOS_DIR.glob("*.py"):
            nombre = archivo.stem

            spec = importlib.util.spec_from_file_location(nombre, archivo)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)

            self.modulos_cargados[nombre] = modulo

    def menu(self):
        while True:
            print("\n--- CALCULADORA ---")

            nombres = list(self.modulos_cargados.keys())

            for i, nombre in enumerate(nombres):
                print(f"{i+1}. {nombre}")

            print("0. salir")

            opcion = int(input("Elegí: "))

            if opcion == 0:
                break

            if 1 <= opcion <= len(nombres):
                modulo = self.modulos_cargados[nombres[opcion-1]]

                a = float(input("Número 1: "))
                b = float(input("Número 2: "))

                resultado = modulo.ejecutar(a, b)
                print(f"Resultado: {resultado}")
            else:
                print("Opción inválida")


# EJECUCIÓN
sistema = SistemaModular()

sistema.actualizar()
sistema.cargar_modulos()
sistema.menu()