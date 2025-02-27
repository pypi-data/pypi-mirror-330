#!/usr/bin/env python
import os
import shutil
from pathlib import Path

def clean_project():
    """Limpia archivos temporales y cache del proyecto"""
    # Directorios y archivos a limpiar
    patterns = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        "**/.pytest_cache",
        "**/.coverage",
        "**/.mypy_cache",
        "**/.tox",
        "**/build",
        "**/dist",
        "**/*.egg-info",
        "**/db_types.py",  # Archivo generado por introspección
    ]

    # Obtener directorio raíz del proyecto
    root = Path(__file__).parent.parent

    # Limpiar cada patrón
    for pattern in patterns:
        for path in root.glob(pattern):
            if path.is_file():
                path.unlink()
                print(f"Eliminado archivo: {path}")
            elif path.is_dir():
                shutil.rmtree(path)
                print(f"Eliminado directorio: {path}")

    patterns.extend([
        "**/.env",           # Archivos de entorno
        "**/.venv",          # Entornos virtuales
        "**/logs/*.log",     # Archivos de log
        "**/groovindb.json", # Archivos de configuración local
    ])

if __name__ == "__main__":
    clean_project() 