from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app.models import Usuario
from app.forms import LoginForm, RegistroForm
from app import db
from functools import wraps

from . import auth_bp


def login_required(f):
    """Decorador: requiere sesión activa."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador: requiere rol de administrador."""
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

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.check_password(form.password.data):
            if not usuario.activo:
                flash('Tu cuenta está desactivada. Contacta al administrador.', 'danger')
                return render_template('auth/login.html', form=form)
            
            session['user_id'] = usuario.id
            session['user_nombre'] = f"{usuario.nombre} {usuario.apellidos}"
            session['user_rol'] = usuario.rol
            session['user_email'] = usuario.email

            flash(f'¡Bienvenido, {usuario.nombre}!', 'success')

            if usuario.rol == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('cliente.inicio'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        existe = Usuario.query.filter_by(email=form.email.data).first()
        if existe:
            flash('Ya existe una cuenta con ese correo.', 'warning')
            return render_template('auth/login.html', form=form)

        nuevo = Usuario(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.email.data,
            telefono=form.telefono.data,
            direccion=form.direccion.data,
            rol='cliente'
        )
        nuevo.set_password(form.password.data)
        db.session.add(nuevo)
        db.session.commit()
        flash('¡Cuenta creada exitosamente! Inicia sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html', form=form, registro=True)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))