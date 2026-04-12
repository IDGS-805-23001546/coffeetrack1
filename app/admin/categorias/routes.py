from flask import render_template, redirect, url_for, request, flash
from . import categorias_bp
from app.auth.routes import admin_required
from app.models import CategoriaBebida
from app import db


@categorias_bp.route('/')
@admin_required
def index():
    categorias = CategoriaBebida.query.all()
    return render_template('admin/categorias.html', categorias=categorias)


@categorias_bp.route('/nueva', methods=['POST'])
@admin_required
def nueva():
    try:
        nombre = request.form.get('nombre').strip()
        descripcion = request.form.get('descripcion', '').strip()
        solo_frio = True if request.form.get('solo_frio') == 'on' else False
        sin_temperatura = True if request.form.get('sin_temperatura') == 'on' else False

        if not nombre:
            flash('El nombre es obligatorio.', 'danger')
            return redirect(url_for('admin_categorias.index'))

        existe = CategoriaBebida.query.filter_by(nombre=nombre).first()
        if existe:
            flash('Ya existe una categoría con ese nombre.', 'warning')
            return redirect(url_for('admin_categorias.index'))

        cat = CategoriaBebida(
            nombre=nombre,
            descripcion=descripcion,
            solo_frio=solo_frio,
            sin_temperatura=sin_temperatura
        )
        db.session.add(cat)
        db.session.commit()
        flash(f'Categoría "{nombre}" creada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('admin_categorias.index'))


@categorias_bp.route('/editar/<int:id>', methods=['POST'])
@admin_required
def editar(id):
    cat = CategoriaBebida.query.get_or_404(id)
    try:
        cat.nombre = request.form.get('nombre').strip()
        cat.descripcion = request.form.get('descripcion', '').strip()
        cat.solo_frio = True if request.form.get('solo_frio') == 'on' else False
        cat.sin_temperatura = True if request.form.get('sin_temperatura') == 'on' else False
        db.session.commit()
        flash('Categoría actualizada.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('admin_categorias.index'))


@categorias_bp.route('/eliminar/<int:id>', methods=['POST'])
@admin_required
def eliminar(id):
    cat = CategoriaBebida.query.get_or_404(id)
    if cat.bebidas.count() > 0:
        flash('No puedes eliminar una categoría que tiene bebidas asignadas.', 'danger')
        return redirect(url_for('admin_categorias.index'))
    db.session.delete(cat)
    db.session.commit()
    flash('Categoría eliminada.', 'info')
    return redirect(url_for('admin_categorias.index'))