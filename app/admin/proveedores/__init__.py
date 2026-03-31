from flask import Blueprint

proveedores_bp = Blueprint('admin_proveedores', __name__)

from . import routes