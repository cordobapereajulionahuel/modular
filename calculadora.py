import os
import requests

URL_REPO = "https://tu-repo.com/"  # puede ser GitHub raw

def descargar_archivo(nombre):
    url = URL_REPO + nombre
    r = requests.get(url)
    with open(f"modulos/{nombre}", "wb") as f:
        f.write(r.content)

def actualizar_modulos():
    import json

    # versiones del servidor
    r = requests.get(URL_REPO + "versiones.json")
    versiones_remotas = r.json()

    # versiones locales
    if os.path.exists("versiones.json"):
        with open("versiones.json") as f:
            versiones_locales = json.load(f)
    else:
        versiones_locales = {}

    for modulo, version in versiones_remotas.items():
        if modulo not in versiones_locales or versiones_locales[modulo] < version:
            print(f"Actualizando {modulo}...")
            descargar_archivo(modulo + ".py")
            versiones_locales[modulo] = version

    with open("versiones.json", "w") as f:
        json.dump(versiones_locales, f)

# ejecutar actualización
actualizar_modulos()

# usar módulos
from modulos import suma, resta

print(suma.sumar(5, 3))
print(resta.restar(10, 4))