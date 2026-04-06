from flask import Blueprint

compras_bp = Blueprint('admin_compras', __name__)

from . import routes