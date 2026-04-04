from flask import Blueprint

pedidos_admin_bp = Blueprint('admin_pedidos', __name__)

from . import routes