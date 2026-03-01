from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, TextAreaField,
                     SelectField, DecimalField, IntegerField, DateField,
                     BooleanField, HiddenField, FloatField)
from wtforms.validators import (DataRequired, Email, Length, EqualTo,
                                 Optional, NumberRange, ValidationError)

# =============================================
# FORMULARIO: Login
# =============================================
class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[
        DataRequired(message='El correo es obligatorio'),
        Email(message='Ingresa un correo válido')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria')
    ])
    submit = SubmitField('Iniciar Sesión')

# =============================================
# FORMULARIO: Registro de Cliente
# =============================================
class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        DataRequired(), Length(min=2, max=100)
    ])
    apellidos = StringField('Apellidos', validators=[
        DataRequired(), Length(min=2, max=100)
    ])
    email = StringField('Correo Electrónico', validators=[
        DataRequired(), Email()
    ])
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=15)])
    direccion = TextAreaField('Dirección', validators=[Optional()])
    password = PasswordField('Contraseña', validators=[
        DataRequired(), Length(min=6, message='Mínimo 6 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(), EqualTo('password', message='Las contraseñas no coinciden')
    ])
    submit = SubmitField('Registrarse')

# =============================================
# FORMULARIO: Proveedor
# =============================================
class ProveedorForm(FlaskForm):
    nombre_empresa = StringField('Nombre de Empresa', validators=[
        DataRequired(), Length(max=150)
    ])
    contacto_nombre = StringField('Nombre de Contacto', validators=[Optional(), Length(max=100)])
    contacto_telefono = StringField('Teléfono', validators=[Optional(), Length(max=50)])
    contacto_email = StringField('Email', validators=[Optional(), Email()])
    direccion = TextAreaField('Dirección', validators=[Optional()])
    rfc = StringField('RFC', validators=[Optional(), Length(max=50)])
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar Proveedor')

# =============================================
# FORMULARIO: Materia Prima
# =============================================
class MateriaPrimaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    categoria_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    unidad_medida = SelectField('Unidad de Medida', choices=[
        ('gr', 'Gramos (gr)'),
        ('ml', 'Mililitros (ml)'),
        ('unidad', 'Unidad'),
        ('kg', 'Kilogramos (kg)'),
        ('lt', 'Litros (lt)')
    ], validators=[DataRequired()])
    stock_actual = DecimalField('Stock Actual', default=0, validators=[Optional()])
    stock_minimo = DecimalField('Stock Mínimo', default=0, validators=[Optional()])
    precio_unitario = DecimalField('Precio Unitario', places=3, default=0, validators=[Optional()])
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar Materia Prima')

# =============================================
# FORMULARIO: Bebida
# =============================================
class BebidaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    descripcion = TextAreaField('Descripción', validators=[Optional()])
    categoria_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    volumen_ml = IntegerField('Volumen (ml)', validators=[DataRequired(), NumberRange(min=1)])
    precio = DecimalField('Precio', places=2, validators=[DataRequired(), NumberRange(min=0.01)])
    imagen_url = StringField('URL de Imagen', validators=[Optional(), Length(max=255)])
    disponible = BooleanField('Disponible', default=True)
    stock_actual = IntegerField('Stock Actual', default=0, validators=[Optional()])
    stock_minimo = IntegerField('Stock Mínimo', default=5, validators=[Optional()])
    submit = SubmitField('Guardar Bebida')

# =============================================
# FORMULARIO: Receta
# =============================================
class RecetaForm(FlaskForm):
    bebida_id = SelectField('Bebida', coerce=int, validators=[DataRequired()])
    materia_prima_id = SelectField('Materia Prima', coerce=int, validators=[DataRequired()])
    cantidad = DecimalField('Cantidad', places=2, validators=[DataRequired(), NumberRange(min=0.01)])
    unidad_medida = SelectField('Unidad', choices=[
        ('ml', 'Mililitros'), ('gr', 'Gramos'), ('unidad', 'Unidad')
    ], validators=[DataRequired()])
    submit = SubmitField('Guardar Ingrediente')

# =============================================
# FORMULARIO: Producción
# =============================================
class ProduccionForm(FlaskForm):
    bebida_id = SelectField('Bebida', coerce=int, validators=[DataRequired()])
    cantidad_producida = IntegerField('Cantidad a Producir', validators=[
        DataRequired(), NumberRange(min=1)
    ])
    fecha_produccion = DateField('Fecha de Producción', validators=[DataRequired()])
    notas = TextAreaField('Notas', validators=[Optional()])
    submit = SubmitField('Registrar Producción')

# =============================================
# FORMULARIO: Compra de Materia Prima
# =============================================
class CompraForm(FlaskForm):
    proveedor_id = SelectField('Proveedor', coerce=int, validators=[DataRequired()])
    fecha_compra = DateField('Fecha de Compra', validators=[DataRequired()])
    notas = TextAreaField('Notas', validators=[Optional()])
    submit = SubmitField('Registrar Compra')

# =============================================
# FORMULARIO: Pedido (Cliente)
# =============================================
class PedidoForm(FlaskForm):
    direccion_entrega = TextAreaField('Dirección de Entrega', validators=[
        DataRequired(message='La dirección es obligatoria')
    ])
    telefono_contacto = StringField('Teléfono de Contacto', validators=[
        DataRequired(), Length(max=15)
    ])
    notas = TextAreaField('Notas adicionales', validators=[Optional()])
    submit = SubmitField('Confirmar Pedido')