from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from . import models
        db.create_all() # Opcional: crea las tablas si no existen

    # IMPORTANTE: Importa y registra aquí
    from .auth import auth_bp
    from .clientes import cliente_bp
    from .carrito import carrito_bp  
    from .pedidos import pedidos_bp
    from .about import about_bp
    
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(cliente_bp, url_prefix='/cliente')
    app.register_blueprint(carrito_bp, url_prefix='/carrito')
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    app.register_blueprint(about_bp, url_prefix='/nosotros')

    return app