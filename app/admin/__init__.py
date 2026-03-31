from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

from . import routes
from .bebidas import bebidas_bp
from .recetas import recetas_bp
from .materias_primas import materias_bp