from flask import Blueprint

bebidas_bp = Blueprint('admin_bebidas', __name__)

from . import routes