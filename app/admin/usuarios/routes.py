from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from . import usuarios_bp
from app.auth.routes import admin_required
from app.models import Usuario,Pedido 
from app import db
import re

@usuarios_bp.route('/')
@admin_required
def index():
    # Solo mostramos usuarios activos en la lista principal
    usuarios = Usuario.query.order_by(Usuario.fecha_registro.desc()).all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

# AGREGAR USUARIO
@usuarios_bp.route('/add', methods=['POST'])
@admin_required
def add():
    try:
        nombre = request.form.get('nombre').strip()
        apellidos = request.form.get('apellidos').strip()
        email = request.form.get('email').strip().lower()
        telefono_raw = request.form.get('telefono', '')
        password = request.form.get('password')
        rol = request.form.get('rol')
        
        telefono_limpio = re.sub(r'[\s\-\(\)]', '', telefono_raw) if telefono_raw else None
        
        if telefono_limpio and len(telefono_limpio) > 15:
            flash('El número de teléfono no puede tener más de 15 dígitos', 'danger')
            return redirect(url_for('admin_usuarios.index'))
        
        if not nombre or not apellidos or not email or not password:
            flash('Todos los campos obligatorios deben ser llenados', 'danger')
            return redirect(url_for('admin_usuarios.index'))
        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            flash('Formato de email no válido', 'danger')
            return redirect(url_for('admin_usuarios.index'))
        
        existing_user = Usuario.query.filter_by(email=email).first()
        if existing_user:
            flash(f'El email {email} ya está registrado en el sistema', 'danger')
            return redirect(url_for('admin_usuarios.index'))
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'danger')
            return redirect(url_for('admin_usuarios.index'))

        nuevo_usuario = Usuario(
            nombre=nombre,
            apellidos=apellidos,
            email=email,
            telefono=telefono_limpio,
            password_hash=generate_password_hash(password),
            rol=rol,
            activo=True
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash(f'Usuario {nombre} {apellidos} creado exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear usuario: {str(e)}', 'danger')
    
    return redirect(url_for('admin_usuarios.index'))

# ELIMINAR USUARIO (Desactivación Lógica para evitar errores de FK)
@usuarios_bp.route('/delete/<int:id>')
@admin_required
def delete(id):
    usuario = Usuario.query.get_or_404(id)
 
    pedidos = Pedido.query.filter_by(usuario_id=usuario.id).all()
 
    for pedido in pedidos:
        Venta.query.filter_by(pedido_id=pedido.id).delete()
 
    Pedido.query.filter_by(usuario_id=usuario.id).delete()
    db.session.delete(usuario)
    db.session.commit()
 
    flash(f'Usuario {usuario.nombre} eliminado del sistema', 'warning')
    return redirect(url_for('admin_usuarios.index'))

# CAMBIAR ROL (Esta es la que te faltaba)
@usuarios_bp.route('/cambiar_rol/<int:id>/<nuevo_rol>')
@admin_required
def cambiar_rol(id, nuevo_rol):
    if nuevo_rol not in ['admin', 'cliente']:
        flash('Rol no válido', 'danger')
        return redirect(url_for('admin_usuarios.index'))

    try:
        usuario = Usuario.query.get_or_404(id)
        usuario.rol = nuevo_rol
        db.session.commit()
        flash(f'Rol de {usuario.nombre} actualizado a {nuevo_rol.upper()}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar rol: {str(e)}', 'danger')
        
    return redirect(url_for('admin_usuarios.index'))