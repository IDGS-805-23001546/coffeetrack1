from flask import Blueprint

categorias_bp = Blueprint('admin_categorias', __name__)

from . import routes