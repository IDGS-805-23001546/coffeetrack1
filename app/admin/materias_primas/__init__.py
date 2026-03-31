from flask import Blueprint 

materias_bp = Blueprint('admin_materias', __name__)

from . import routes 