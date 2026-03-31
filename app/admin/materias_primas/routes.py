from flask import render_template, redirect, url_for, request, flash, jsonify
from . import materias_bp
from app.auth.routes import admin_required
from app.models import MateriaPrima, CategoriaMateriaPrima
from app import db

@materias_bp.route('/')
@admin_required
def index():
    materias = MateriaPrima.query.filter_by(activo=True).all()
    categorias = CategoriaMateriaPrima.query.all()
    return render_template('admin/materias_primas.html',
        materias=materias,
        categorias=categorias
    )

@materias_bp.route('/nueva', methods=['POST'])
@admin_required
def nueva():
    try:
        materia = MateriaPrima(
            nombre=request.form.get('nombre'),
            categoria_id=int(request.form.get('categoria_id')),
            unidad_medida=request.form.get('unidad_medida'),
            stock_actual=float(request.form.get('stock_actual', 0)),
            stock_minimo=float(request.form.get('stock_minimo', 0)),
            precio_unitario=float(request.form.get('precio_unitario', 0))
        )
        db.session.add(materia)
        db.session.commit()
        flash('Materia prima registrada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('admin_materias.index'))

@materias_bp.route('/editar/<int:id>', methods=['POST'])
@admin_required
def editar(id):
    materia = MateriaPrima.query.get_or_404(id)
    try:
        materia.nombre = request.form.get('nombre')
        materia.categoria_id = int(request.form.get('categoria_id'))
        materia.unidad_medida = request.form.get('unidad_medida')
        materia.stock_actual = float(request.form.get('stock_actual', 0))
        materia.stock_minimo = float(request.form.get('stock_minimo', 0))
        materia.precio_unitario = float(request.form.get('precio_unitario', 0))
        db.session.commit()
        flash('Materia prima actualizada.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('admin_materias.index'))

@materias_bp.route('/eliminar/<int:id>', methods=['POST'])
@admin_required
def eliminar(id):
    materia = MateriaPrima.query.get_or_404(id)
    materia.activo = False
    db.session.commit()
    return jsonify({'ok': True})