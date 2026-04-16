from flask import render_template, redirect, url_for, request, flash, jsonify
from . import recetas_bp
from app.auth.routes import admin_required
from app.models import Receta, Bebida, MateriaPrima
from app import db


def calcular_capacidad(bebida):
    """Calcula cuántas unidades se pueden producir con el stock actual"""
    recetas = bebida.recetas.all()
    if not recetas:
        return 0
    capacidades = []
    for r in recetas:
        mp = r.materia_prima
        if mp and float(r.cantidad) > 0:
            capacidades.append(int(float(mp.stock_actual) // float(r.cantidad)))
    return min(capacidades) if capacidades else 0


@recetas_bp.route('/')
@admin_required
def index():
    bebidas = Bebida.query.filter_by(activo=True).all()
    materias = MateriaPrima.query.filter_by(activo=True).all()

    # Calcular capacidad por bebida
    capacidades = {}
    for b in bebidas:
        capacidades[b.id] = calcular_capacidad(b)

    # Ingrediente limitante por bebida
    limitantes = {}
    for b in bebidas:
        recetas = b.recetas.all()
        if recetas:
            min_cap = None
            min_mp = None
            for r in recetas:
                mp = r.materia_prima
                if mp and float(r.cantidad) > 0:
                    cap = int(float(mp.stock_actual) // float(r.cantidad))
                    if min_cap is None or cap < min_cap:
                        min_cap = cap
                        min_mp = mp.nombre
            limitantes[b.id] = min_mp

    return render_template('admin/recetas.html',
        bebidas=bebidas,
        materias=materias,
        capacidades=capacidades,
        limitantes=limitantes
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

@recetas_bp.route('/eliminar_completa/<int:bebida_id>', methods=['POST'])
@admin_required
def eliminar_completa(bebida_id):
    try:
        bebida = Bebida.query.get_or_404(bebida_id)
        recetas_count = Receta.query.filter_by(bebida_id=bebida_id).count()
        Receta.query.filter_by(bebida_id=bebida_id).delete()
        db.session.commit()
        flash(f'Receta de "{bebida.nombre}" eliminada. {recetas_count} ingrediente(s) borrados.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('admin_recetas.index'))