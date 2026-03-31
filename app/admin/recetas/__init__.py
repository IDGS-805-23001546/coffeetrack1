from flask import Blueprint

recetas_bp = Blueprint('admin_recetas', __name__)

from . import routes