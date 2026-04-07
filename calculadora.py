import os
import requests
import json

URL_REPO = "https://raw.githubusercontent.com/cordobapereajulionahuel/modular/main/"

def descargar_archivo(nombre):
    url = URL_REPO + nombre
    r = requests.get(url)
    with open(f"modulos/{nombre}", "wb") as f:
        f.write(r.content)

def actualizar_modulos():
    r = requests.get(URL_REPO + "versiones.json")
    versiones_remotas = r.json()

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

actualizar_modulos()

from modulos import sumar, Restar ,multiplicar

print(sumar(5, 3))
print(Restar(10, 4))
print(multiplicar(10, 4))
