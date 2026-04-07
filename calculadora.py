import os
import requests
import json
from pathlib import Path
from typing import Dict, Optional
import importlib.util
import sys

URL_REPO = "https://raw.githubusercontent.com/cordobapereajulionahuel/modular/main/"
MODULOS_DIR = Path("modulos")
VERSIONES_FILE = Path("versiones.json")
TIMEOUT = 5

class GestorModulos:
    def __init__(self):
        self.versiones_locales: Dict[str, int] = {}
        self.versiones_remotas: Dict[str, int] = {}
        self._crear_estructura()
    
    def _crear_estructura(self):
        """Crea la estructura de carpetas necesaria"""
        MODULOS_DIR.mkdir(exist_ok=True)
        self._cargar_versiones_locales()
    
    def _cargar_versiones_locales(self):
        """Carga versiones locales de forma segura"""
        if VERSIONES_FILE.exists():
            try:
                with open(VERSIONES_FILE) as f:
                    self.versiones_locales = json.load(f)
            except json.JSONDecodeError:
                print("⚠️  versiones.json corrupto. Reiniciando...")
                self.versiones_locales = {}
        else:
            self.versiones_locales = {}
    
    def descargar_archivo(self, nombre: str) -> bool:
        """Descarga un archivo del repositorio"""
        try:
            url = URL_REPO + nombre
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()  # Lanza excepción si el código es 4xx/5xx
            
            archivo_local = MODULOS_DIR / nombre
            archivo_local.write_bytes(response.content)
            print(f"✓ Descargado: {nombre}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error al descargar {nombre}: {e}")
            return False
    
    def obtener_versiones_remotas(self) -> bool:
        """Obtiene el archivo versiones.json del repositorio"""
        try:
            url = URL_REPO + "versiones.json"
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            
            self.versiones_remotas = response.json()
            print("✓ Versiones remotas obtenidas")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error al obtener versiones.json: {e}")
            return False
        except json.JSONDecodeError:
            print("✗ versiones.json remoto inválido")
            return False
    
    def actualizar_modulos(self):
        """Actualiza módulos que tienen versión más nueva"""
        if not self.obtener_versiones_remotas():
            print("No se pudo conectar al repositorio")
            return
        
        modulos_actualizados = 0
        
        for modulo, version_remota in self.versiones_remotas.items():
            version_local = self.versiones_locales.get(modulo, 0)
            
            if version_remota > version_local:
                print(f"→ {modulo}: v{version_local} → v{version_remota}")
                
                if self.descargar_archivo(f"{modulo}.py"):
                    self.versiones_locales[modulo] = version_remota
                    modulos_actualizados += 1
        
        # Guarda versiones locales
        self._guardar_versiones_locales()
        
        if modulos_actualizados == 0:
            print("✓ Todo actualizado")
        else:
            print(f"✓ {modulos_actualizados} módulo(s) actualizado(s)")
    
    def _guardar_versiones_locales(self):
        """Guarda versiones locales en JSON"""
        try:
            with open(VERSIONES_FILE, "w") as f:
                json.dump(self.versiones_locales, f, indent=2)
        except IOError as e:
            print(f"✗ Error al guardar versiones.json: {e}")
    
    def cargar_modulo(self, nombre: str):
        """Carga dinámicamente un módulo Python descargado"""
        try:
            archivo = MODULOS_DIR / f"{nombre}.py"
            
            if not archivo.exists():
                raise FileNotFoundError(f"Módulo {nombre} no encontrado")
            
            spec = importlib.util.spec_from_file_location(nombre, archivo)
            modulo = importlib.util.module_from_spec(spec)
            sys.modules[nombre] = modulo
            spec.loader.exec_module(modulo)
            
            return modulo
            
        except Exception as e:
            print(f"✗ Error al cargar {nombre}: {e}")
            return None


if __name__ == "__main__":
    # Inicializa gestor y actualiza
    gestor = GestorModulos()
    gestor.actualizar_modulos()
    
    # Carga y usa los módulos
    print("\n--- Pruebas ---")
    modulos = gestor.cargar_modulo("modulos")
    
    if modulos:
        print(f"Suma (5 + 3) = {modulos.sumar(5, 3)}")
        print(f"Resta (10 - 4) = {modulos.Restar(10, 4)}")
        print(f"Multiplicación (10 * 4) = {modulos.multiplicar(10, 4)}")