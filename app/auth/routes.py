from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app.models import Usuario, CodigoVerificacion
from app.forms import LoginForm, RegistroForm
from app import db, mail
from functools import wraps
from datetime import datetime, timedelta
import random
import string
from flask_mail import Message

from . import auth_bp


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('user_rol') != 'admin':
            flash('No tienes permisos de administrador.', 'danger')
            return redirect(url_for('cliente.inicio'))
        return f(*args, **kwargs)
    return decorated_function


def generar_codigo():
    return ''.join(random.choices(string.digits, k=6))

def enviar_codigo(email, nombre, codigo):
    msg = Message(
        subject='CoffeeTrack — Código de verificación',
        recipients=[email]
    )
    msg.html = f'''
    <div style="font-family: Segoe UI, sans-serif; max-width: 500px; margin: auto; padding: 30px; background: #fdf8f3; border-radius: 16px;">
        <h2 style="color: #e8891a;">☕ CoffeeTrack</h2>
        <p>Hola <strong>{nombre}</strong>,</p>
        <p>Tu código de verificación es:</p>
        <div style="font-size: 2.5rem; font-weight: 700; color: #e8891a; background: white; padding: 20px; border-radius: 12px; text-align: center; letter-spacing: 8px; margin: 20px 0;">
            {codigo}
        </div>
        <p style="color: #888;">Este código expira en <strong>10 minutos</strong>.</p>
        <p style="color: #888; font-size: 0.85rem;">Si no solicitaste este código, ignora este mensaje.</p>
    </div>
    '''
    mail.send(msg)


@auth_bp.route('/')
def index():
    if 'user_id' in session:
        if session.get('user_rol') == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('cliente.inicio'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('auth.index'))

    # Limite de intentos
    intentos = session.get('login_intentos', 0)
    bloqueado_hasta = session.get('login_bloqueado_hasta')

    if bloqueado_hasta:
        bloqueado_hasta_dt = datetime.fromisoformat(bloqueado_hasta)
        if datetime.now() < bloqueado_hasta_dt:
            minutos = int((bloqueado_hasta_dt - datetime.now()).seconds / 60) + 1
            flash(f'Demasiados intentos fallidos. Espera {minutos} minuto(s).', 'danger')
            form = LoginForm()
            return render_template('auth/login.html', form=form)
        else:
            session.pop('login_intentos', None)
            session.pop('login_bloqueado_hasta', None)
            intentos = 0

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.check_password(form.password.data):
            if not usuario.activo:
                flash('Tu cuenta está desactivada.', 'danger')
                return render_template('auth/login.html', form=form)

            if not usuario.verificado:
                flash('Tu cuenta no está verificada. Revisa tu correo.', 'warning')
                return render_template('auth/login.html', form=form)

            # Login exitoso, resetear intentos
            session.pop('login_intentos', None)
            session.pop('login_bloqueado_hasta', None)

            session['user_id'] = usuario.id
            session['user_nombre'] = f"{usuario.nombre} {usuario.apellidos}"
            session['user_rol'] = usuario.rol
            session['user_email'] = usuario.email
            session['user_telefono'] = usuario.telefono or ''
            session['user_direccion'] = usuario.direccion or ''

            flash(f'¡Bienvenido, {usuario.nombre}!', 'success')

            if usuario.rol == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('cliente.inicio'))
        else:
            intentos += 1
            session['login_intentos'] = intentos

            restantes = 5 - intentos
            if intentos >= 5:
                session['login_bloqueado_hasta'] = (
                    datetime.now() + timedelta(minutes=5)
                ).isoformat()
                session['login_intentos'] = 0
                flash('Demasiados intentos fallidos. Cuenta bloqueada por 5 minutos.', 'danger')
            else:
                flash(f'Correo o contraseña incorrectos. Te quedan {restantes} intentos.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        existe = Usuario.query.filter_by(email=form.email.data).first()
        if existe:
            flash('Ya existe una cuenta con ese correo.', 'warning')
            return render_template('auth/login.html', form=form, registro=True)

        nuevo = Usuario(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            telefono=form.telefono.data,
            direccion=form.direccion.data,
            rol='cliente',
            verificado=False
        )
        nuevo.set_password(form.password.data)
        db.session.add(nuevo)
        db.session.flush()

        # Generar y guardar codigo
        codigo = generar_codigo()
        expira = datetime.now() + timedelta(minutes=10)
        cv = CodigoVerificacion(
            usuario_id=nuevo.id,
            codigo=codigo,
            expira_en=expira
        )
        db.session.add(cv)
        db.session.commit()

        # Enviar correo
        try:
            enviar_codigo(nuevo.email, nuevo.nombre, codigo)
            flash('Cuenta creada. Revisa tu correo para verificar tu cuenta.', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')

        return redirect(url_for('auth.verificar', email=nuevo.email))

    return render_template('auth/login.html', form=form, registro=True)


@auth_bp.route('/verificar', methods=['GET', 'POST'])
def verificar():
    email = request.args.get('email') or request.form.get('email')
    if not email:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        codigo_ingresado = request.form.get('codigo', '').strip()
        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            flash('Usuario no encontrado.', 'danger')
            return redirect(url_for('auth.login'))

        cv = CodigoVerificacion.query.filter_by(
            usuario_id=usuario.id,
            usado=False
        ).order_by(CodigoVerificacion.fecha_creacion.desc()).first()

        if not cv:
            flash('No hay código de verificación activo.', 'danger')
            return redirect(url_for('auth.login'))

        if datetime.now() > cv.expira_en:
            flash('El código expiró. Regístrate de nuevo.', 'danger')
            return redirect(url_for('auth.registro'))

        if cv.codigo != codigo_ingresado:
            flash('Código incorrecto. Intenta de nuevo.', 'danger')
            return render_template('auth/verificar.html', email=email)

        # Verificar cuenta
        usuario.verificado = True
        cv.usado = True
        db.session.commit()

        flash('¡Cuenta verificada! Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/verificar.html', email=email)


@auth_bp.route('/reenviar/<email>')
def reenviar_codigo(email):
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or usuario.verificado:
        return redirect(url_for('auth.login'))

    codigo = generar_codigo()
    expira = datetime.now() + timedelta(minutes=10)
    cv = CodigoVerificacion(
        usuario_id=usuario.id,
        codigo=codigo,
        expira_en=expira
    )
    db.session.add(cv)
    db.session.commit()

    try:
        enviar_codigo(usuario.email, usuario.nombre, codigo)
        flash('Código reenviado a tu correo.', 'success')
    except:
        flash('No se pudo reenviar el código.', 'danger')

    return redirect(url_for('auth.verificar', email=email))


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))