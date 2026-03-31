from flask import render_template, redirect, url_for, request, flash
from . import proveedores_bp
from app.auth.routes import admin_required
from app.models import Proveedor
from app import db

@proveedores_bp.route('/')
@admin_required
def index():
    proveedores = Proveedor.query.filter_by(activo=True).all()
    return render_template('admin/proveedores.html', proveedores=proveedores)

# AGREGAR
@proveedores_bp.route('/add', methods=['POST'])
@admin_required
def add():
    nuevo = Proveedor(
        nombre_empresa=request.form['nombre_empresa'],
        contacto_nombre=request.form.get('contacto_nombre'),
        contacto_telefono=request.form.get('contacto_telefono'),
        contacto_email=request.form.get('contacto_email'),
        direccion=request.form.get('direccion'),
        rfc=request.form.get('rfc'),
        activo=True
    )
    db.session.add(nuevo)
    db.session.commit()
    flash('Proveedor agregado correctamente', 'success')
    return redirect(url_for('admin_proveedores.index'))

# ELIMINAR
@proveedores_bp.route('/delete/<int:id>')
@admin_required
def delete(id):
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    flash('Proveedor eliminado', 'warning')
    return redirect(url_for('admin_proveedores.index'))

# EDITAR PROVEEDOR
@proveedores_bp.route('/edit/<int:id>', methods=['POST'])
@admin_required
def edit(id):
    p = Proveedor.query.get_or_404(id)
    p.nombre_empresa = request.form['nombre_empresa']
    p.contacto_nombre = request.form.get('contacto_nombre')
    p.contacto_telefono = request.form.get('contacto_telefono')
    p.contacto_email = request.form.get('contacto_email')
    p.rfc = request.form.get('rfc')
    p.direccion = request.form.get('direccion')
    p.activo = request.form.get('activo') == 'True'
    
    db.session.commit()
    flash('Proveedor actualizado correctamente', 'success')
    return redirect(url_for('admin_proveedores.index'))