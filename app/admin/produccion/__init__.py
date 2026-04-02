from flask import Blueprint

produccion_bp = Blueprint('admin_produccion', __name__)

from . import routes