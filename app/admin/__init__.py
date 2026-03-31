from flask import Blueprint

admin_bp = Blueprint('admin', __name__,
                     template_folder='templates')
from . import routes
from .bebidas import bebidas_bp
from .proveedores import proveedores_bp
from .usuarios import usuarios_bp 