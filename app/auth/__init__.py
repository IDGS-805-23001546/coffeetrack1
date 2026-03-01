from flask import Blueprint

# Este nombre es el que importa
auth_bp = Blueprint(
    'auth',
    __name__)

from . import routes