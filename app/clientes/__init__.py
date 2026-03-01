from flask import Blueprint

# Este nombre es el que importa
cliente_bp = Blueprint(
    'cliente',
    __name__)

from . import routes