from flask import render_template
from . import about_bp

@about_bp.route('/')
def nosotros():
    
    return render_template('clientes/about.html')