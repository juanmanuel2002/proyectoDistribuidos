from flask import Flask
app = Flask(
    __name__,
    template_folder='frontend/templates',  # Ruta a las plantillas en la carpeta frontend
    static_folder='frontend/static'        # Ruta a los archivos estáticos en la carpeta frontend
)
from . import view

