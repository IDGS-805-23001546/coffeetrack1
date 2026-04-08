# app/admin/recetas/routes.py
from flask import render_template, redirect, url_for, request, flash, jsonify
from . import recetas_bp
from app.auth.routes import admin_required
from app.models import Receta, Bebida, MateriaPrima
from app import db

@recetas_bp.route('/')
@admin_required
def index():
    bebidas = Bebida.query.filter_by(activo=True).all()
    materias = MateriaPrima.query.filter_by(activo=True).all()
    return render_template('admin/recetas.html',
        bebidas=bebidas,
        materias=materias
    )

@recetas_bp.route('/nueva', methods=['POST'])
@admin_required
def nueva():
    try:
        bebida_id = int(request.form.get('bebida_id'))
        materia_ids = request.form.getlist('materia_prima_id[]')
        cantidades = request.form.getlist('cantidad[]')
        unidades = request.form.getlist('unidad_medida[]')
        bebida = Bebida.query.get(bebida_id)

        for i in range(len(materia_ids)):
            if materia_ids[i] and cantidades[i]:
                existe = Receta.query.filter_by(
                    bebida_id=bebida_id,
                    materia_prima_id=int(materia_ids[i])
                ).first()
                if existe:
                    existe.cantidad = float(cantidades[i])
                    existe.unidad_medida = unidades[i]
                else:
                    receta = Receta(
                        nombre=bebida.nombre,
                        bebida_id=bebida_id,
                        materia_prima_id=int(materia_ids[i]),
                        cantidad=float(cantidades[i]),
                        unidad_medida=unidades[i]
                    )
                    db.session.add(receta)

        db.session.commit()
        flash('Receta guardada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar receta: {str(e)}', 'danger')
    return redirect(url_for('admin_recetas.index'))

@recetas_bp.route('/editar/<int:id>', methods=['POST'])
@admin_required
def editar(id):
    receta = Receta.query.get_or_404(id)
    try:
        receta.materia_prima_id = int(request.form.get('materia_prima_id'))
        receta.cantidad = float(request.form.get('cantidad'))
        receta.unidad_medida = request.form.get('unidad_medida')
        db.session.commit()
        return jsonify({'ok': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'ok': False, 'error': str(e)}), 500

@recetas_bp.route('/eliminar/<int:id>', methods=['POST'])
@admin_required
def eliminar(id):
    receta = Receta.query.get_or_404(id)
    db.session.delete(receta)
    db.session.commit()
    return jsonify({'ok': True})

