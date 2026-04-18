from app import db 
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(15))
    direccion = db.Column(db.Text)
    rol = db.Column(db.Enum('admin', 'cliente'), default='cliente', index=True)
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    pedidos = db.relationship('Pedido', backref='usuario', lazy='dynamic')
    codigos = db.relationship('CodigoVerificacion', backref='usuario', cascade='all, delete-orphan')
    verificado = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.nombre} {self.apellidos}>'


class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_empresa = db.Column(db.String(150), nullable=False, index=True)
    contacto_nombre = db.Column(db.String(100))
    contacto_telefono = db.Column(db.String(50))
    contacto_email = db.Column(db.String(100))
    direccion = db.Column(db.Text)
    rfc = db.Column(db.String(50), index=True)
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    compras = db.relationship('CompraMateriaPrima', backref='proveedor', lazy='dynamic')

    def __repr__(self):
        return f'<Proveedor {self.nombre_empresa}>'


class CategoriaMateriaPrima(db.Model):
    __tablename__ = 'categorias_materia_prima'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    materias_primas = db.relationship('MateriaPrima', backref='categoria', lazy='dynamic')


class MateriaPrima(db.Model):
    __tablename__ = 'materias_primas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, index=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias_materia_prima.id'), nullable=False, index=True)
    unidad_medida = db.Column(db.String(20), nullable=False)
    stock_actual = db.Column(db.Numeric(10, 2), default=0)
    stock_minimo = db.Column(db.Numeric(10, 2), default=0)
    precio_unitario = db.Column(db.Numeric(10, 3), default=0)
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    recetas = db.relationship('Receta', backref='materia_prima', lazy='dynamic')

    def __repr__(self):
        return f'<MateriaPrima {self.nombre}>'


class CategoriaBebida(db.Model):
    __tablename__ = 'categoria_bebidas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    solo_frio = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    sin_temperatura = db.Column(db.Boolean, default=False)
    bebidas = db.relationship('Bebida', backref='categoria', lazy='dynamic')


class Bebida(db.Model):
    __tablename__ = 'bebidas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, index=True)
    descripcion = db.Column(db.Text)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria_bebidas.id'), nullable=False, index=True)
    volumen_ml = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    imagen_url = db.Column(db.String(255))
    disponible = db.Column(db.Boolean, default=True, index=True)
    stock_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=5)
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    recetas = db.relationship('Receta', backref='bebida', lazy='dynamic', cascade='all, delete-orphan')
    imagen_url_frio = db.Column(db.String(255))
    solo_caliente = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Bebida {self.nombre}>'


class Receta(db.Model):
    __tablename__ = 'recetas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    bebida_id = db.Column(db.Integer, db.ForeignKey('bebidas.id', ondelete='CASCADE'), nullable=False, index=True)
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materias_primas.id'), nullable=False, index=True)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    unidad_medida = db.Column(db.String(20), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('bebida_id', 'materia_prima_id', name='unique_receta'),
    )


class CompraMateriaPrima(db.Model):
    __tablename__ = 'compras_materia_prima'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False, index=True)
    fecha_compra = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.Enum('pendiente', 'recibida', 'cancelada'), default='pendiente')
    notas = db.Column(db.Text)
    usuario_registro_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    detalles = db.relationship('DetalleCompraMateriaPrima', backref='compra', lazy='dynamic', cascade='all, delete-orphan')


class DetalleCompraMateriaPrima(db.Model):
    __tablename__ = 'detalles_compras_materia_prima'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    compras_id = db.Column(db.Integer, db.ForeignKey('compras_materia_prima.id', ondelete='CASCADE'), nullable=False, index=True)
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materias_primas.id'), nullable=False, index=True)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    materia_prima = db.relationship('MateriaPrima', backref='compras_detalle')


class Produccion(db.Model):
    __tablename__ = 'produccion'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bebida_id = db.Column(db.Integer, db.ForeignKey('bebidas.id'), nullable=False, index=True)
    cantidad_producida = db.Column(db.Integer, nullable=False)
    es_frio = db.Column(db.Boolean, default=False)
    fecha_produccion = db.Column(db.Date, nullable=False)
    costo_produccion = db.Column(db.Numeric(10, 2))
    usuario_registrado_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    notas = db.Column(db.Text)
    estado = db.Column(db.Enum('planificada', 'en proceso', 'completada', 'cancelada'), default='planificada', index=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    bebida = db.relationship('Bebida', backref='producciones')
    usuario = db.relationship('Usuario', backref='producciones')


class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True, index=True)
    nombre_cliente = db.Column(db.String(150))
    fecha_pedido = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    descuento = db.Column(db.Numeric(10, 2), default=0)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.Enum('pendiente', 'confirmado', 'en_preparacion', 'enviado', 'entregado', 'cancelado'), default='pendiente', index=True)
    direccion_entrega = db.Column(db.Text, nullable=False)
    telefono_contacto = db.Column(db.String(15), nullable=False)
    notas = db.Column(db.Text)
    fecha_entrega_estimada = db.Column(db.Date)
    fecha_entrega_real = db.Column(db.Date)
    costo_envio = db.Column(db.Numeric(10, 2), default=0)
    hora_estimada_entrega = db.Column(db.String(10))
    dia_entrega = db.Column(db.Date)
    metodo_pago_cliente = db.Column(db.String(20), default='efectivo')
    detalles = db.relationship('DetallePedido', backref='pedido', lazy='dynamic', cascade='all, delete-orphan')
    venta = db.relationship('Venta', backref='pedido', uselist=False)


class DetallePedido(db.Model):
    __tablename__ = 'detalle_pedidos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id', ondelete='CASCADE'), nullable=False, index=True)
    bebida_id = db.Column(db.Integer, db.ForeignKey('bebidas.id'), nullable=False, index=True)
    cantidad = db.Column(db.Integer, nullable=False)
    temperatura = db.Column(db.Enum('caliente', 'frio'), default='caliente')
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    bebida = db.relationship('Bebida', backref='detalles_pedido')


class Venta(db.Model):
    __tablename__ = 'ventas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False, index=True)
    fecha_venta = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    metodo_pago = db.Column(db.Enum('efectivo', 'tarjeta', 'transferencia', 'paypal'), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado_pago = db.Column(db.Enum('pendiente', 'pagado', 'reembolsado'), default='pendiente', index=True)
    referencia_pago = db.Column(db.String(100))


class HistorialInventario(db.Model):
    __tablename__ = 'historial_inventario'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materias_primas.id'), nullable=False, index=True)
    tipo_movimiento = db.Column(db.Enum('entrada', 'salida', 'ajuste'), nullable=False, index=True)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    stock_anterior = db.Column(db.Numeric(10, 2), nullable=False)
    stock_nuevo = db.Column(db.Numeric(10, 2), nullable=False)
    referencia = db.Column(db.String(100))
    motivo = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_movimiento = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    materia_prima = db.relationship('MateriaPrima', backref='historial')
    usuario = db.relationship('Usuario', backref='historial_inventario')


class AlertaInventario(db.Model):
    __tablename__ = 'alertas_inventario'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materias_primas.id'))
    bebida_id = db.Column(db.Integer, db.ForeignKey('bebidas.id'))
    tipo_alerta = db.Column(db.Enum('stock_bajo_materia', 'stock_bajo_bebida', 'materia_agotada', 'bebida_agotada'), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    activa = db.Column(db.Boolean, default=True, index=True)
    fecha_alerta = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    fecha_resolucion = db.Column(db.DateTime)
    materia_prima = db.relationship('MateriaPrima', backref='alertas')
    bebida = db.relationship('Bebida', backref='alertas')


class CodigoVerificacion(db.Model):
    __tablename__ = 'codigos_verificacion'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    codigo = db.Column(db.String(6), nullable=False)
    expira_en = db.Column(db.DateTime, nullable=False)
    usado = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
class ProveedorMateria(db.Model):
    __tablename__ = 'proveedor_materias'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materias_primas.id'), nullable=False)
    materia_prima = db.relationship('MateriaPrima')