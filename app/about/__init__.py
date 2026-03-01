from flask import Blueprint

# Definimos el blueprint
about_bp = Blueprint('about', __name__)

# Importamos las rutas para que se registren
from . import routes