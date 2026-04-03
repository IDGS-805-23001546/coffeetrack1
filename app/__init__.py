from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from .config import Config

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)
    app.jinja_env.globals['enumerate'] = enumerate

    with app.app_context():
        from . import models
        db.create_all() 

    from .auth import auth_bp
    from .clientes import cliente_bp
    from .carrito import carrito_bp  
    from .pedidos import pedidos_bp
    from .about import about_bp
    from .admin import admin_bp
    from .admin.bebidas import bebidas_bp
    from .admin.recetas import recetas_bp
    from .admin.materias_primas import materias_bp
    from .admin.proveedores import proveedores_bp
    from .admin.usuarios import usuarios_bp
    from .admin.pedidos import pedidos_admin_bp
    from .admin.produccion import produccion_bp
    from .admin.ventas import ventas_bp

    
    app.register_blueprint(auth_bp)
    app.register_blueprint(cliente_bp, url_prefix='/cliente')
    app.register_blueprint(carrito_bp, url_prefix='/carrito')
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    app.register_blueprint(about_bp, url_prefix='/nosotros')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(bebidas_bp, url_prefix='/admin/bebidas')
    app.register_blueprint(recetas_bp, url_prefix='/admin/recetas')
    app.register_blueprint(materias_bp, url_prefix='/admin/materias')
    app.register_blueprint(proveedores_bp, url_prefix='/admin/proveedores')
    app.register_blueprint(usuarios_bp, url_prefix='/admin/usuarios')
    app.register_blueprint(pedidos_admin_bp, url_prefix='/admin/pedidos')
    app.register_blueprint(produccion_bp, url_prefix='/admin/produccion')
    app.register_blueprint(ventas_bp, url_prefix='/admin/ventas')



    return app