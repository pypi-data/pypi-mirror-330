import os
import json

def get_config():
    try:
        config_path = os.path.join(os.getcwd(), 'config.json')
        with open(config_path) as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        raise FileNotFoundError(
            "No se encontró el archivo config.json en el directorio raíz. "
            "Por favor, crea un archivo config.json en el directorio donde estás ejecutando tu aplicación."
        )