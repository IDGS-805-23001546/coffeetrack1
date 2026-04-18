from flask import Blueprint

admin_bp = Blueprint('admin', __name__,
                     template_folder='templates')

from . import routes
from .bebidas import bebidas_bp
from .recetas import recetas_bp
from .materias_primas import materias_bp
from .proveedores import proveedores_bp
from .usuarios import usuarios_bp
from .pedidos import pedidos_admin_bp
from .produccion import produccion_bp
from .ventas import ventas_bp
from .compras import compras_bp
