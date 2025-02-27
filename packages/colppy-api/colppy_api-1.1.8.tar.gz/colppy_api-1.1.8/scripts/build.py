#!/usr/bin/env python3.103
import os
import shutil
import subprocess
from pathlib import Path

def run_command(command: str, description: str) -> None:
    """Ejecuta un comando y muestra su descripción"""
    print(f"\n🔄 {description}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} completado")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        exit(1)

def clean_project():
    """Limpia archivos compilados y directorios de build"""
    print("\n🧹 Limpiando proyecto...")
    
    # Eliminar __pycache__
    for path in Path('.').rglob('__pycache__'):
        shutil.rmtree(path)
        print(f"Eliminado: {path}")
    
    # Eliminar archivos compilados
    for ext in ['*.pyc', '*.pyo', '*.pyd']:
        for file in Path('.').rglob(ext):
            file.unlink()
            print(f"Eliminado: {file}")
    
    # Eliminar directorios de build
    for dir_name in ['build', 'dist', '*.egg-info']:
        for path in Path('.').glob(dir_name):
            shutil.rmtree(path)
            print(f"Eliminado: {path}")

def main():
    print("🚀 Iniciando proceso de build...")
    
    # 1. Limpiar proyecto
    clean_project()
    
    # 2. Instalar dependencias de build
    run_command(
        "pip install build twine",
        "Instalación de dependencias de build"
    )
    
    # 3. Reinstalar en modo desarrollo
    run_command(
        "pip install -e .",
        "Instalación en modo desarrollo"
    )
    
    # 4. Construir el paquete
    run_command(
        "python3.10 -m build",
        "Construcción del paquete"
    )
    
    # 5. Preguntar si subir a PyPI
    while True:
        response = input("\n¿Quieres subir el paquete a PyPI? (y/n): ").lower()
        if response in ['y', 'n']:
            break
        print("Por favor, responde 'y' o 'n'")
    
    if response == 'y':
        run_command(
            "python3.10 -m twine upload dist/*",
            "Subida a PyPI"
        )
    
    print("\n✨ Proceso completado exitosamente!")

if __name__ == "__main__":
    main() 