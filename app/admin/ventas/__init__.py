from flask import Blueprint

ventas_bp = Blueprint('admin_ventas', __name__)

from . import routes
 