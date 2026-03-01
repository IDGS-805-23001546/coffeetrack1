from flask import Blueprint

carrito_bp = Blueprint('carrito', __name__)

from . import routes