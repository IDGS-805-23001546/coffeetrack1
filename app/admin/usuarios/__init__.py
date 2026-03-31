from flask import Blueprint

usuarios_bp = Blueprint('admin_usuarios', __name__)

from . import routes