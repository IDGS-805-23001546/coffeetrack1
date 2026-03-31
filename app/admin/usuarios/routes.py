from flask import render_template, redirect, url_for, request, flash
from . import usuarios_bp
from app.auth.routes import admin_required
from app.models import Usuario
from app import db

@usuarios_bp.route('/')
@admin_required
def index():
    # Traemos a todos los usuarios, ordenados por fecha de registro
    usuarios = Usuario.query.order_by(Usuario.fecha_registro.desc()).all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

# CAMBIAR ROL (Ascender/Degradar)
@usuarios_bp.route('/cambiar_rol/<int:id>/<nuevo_rol>')
@admin_required
def cambiar_rol(id, nuevo_rol):
    # Validación de seguridad para los roles permitidos
    if nuevo_rol not in ['admin', 'cliente']:
        flash('Rol no válido', 'danger')
        return redirect(url_for('admin_usuarios.index'))

    usuario = Usuario.query.get_or_404(id)
    

    usuario.rol = nuevo_rol
    db.session.commit()
    
    msg = f"El usuario {usuario.nombre} ahora es {nuevo_rol.upper()}"
    flash(msg, 'success')
    return redirect(url_for('admin_usuarios.index'))

# ELIMINAR O DESACTIVAR USUARIO
@usuarios_bp.route('/delete/<int:id>')
@admin_required
def delete(id):
    usuario = Usuario.query.get_or_404(id)
    
    # En lugar de borrar, lo marcamos como inactivo (borrado lógico)
    usuario.activo = False
    db.session.commit()
    
    flash(f'Usuario {usuario.nombre} desactivado del sistema', 'warning')
    return redirect(url_for('admin_usuarios.index'))