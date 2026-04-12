from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from .config import Config
from datetime import timezone, timedelta

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)
    app.jinja_env.globals['enumerate'] = enumerate
    
    # Filtro de zona horaria México (CST = UTC-6)
    @app.template_filter('hora_mx')
    def hora_mx(dt):
        if dt is None:
            return ''
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        mx = dt.astimezone(timezone(timedelta(hours=-6)))
        return mx.strftime('%d/%m/%Y %H:%M')
    
    @app.after_request
    def add_no_cache(response):
        if 'user_id' not in session:
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        return response  # SIEMPRE debe retornar response

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
    from .admin.compras import compras_bp
    from .admin.categorias import categorias_bp

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
    app.register_blueprint(compras_bp, url_prefix='/admin/compras')
    app.register_blueprint(categorias_bp, url_prefix='/admin/categorias')
    
    

    

    return app