from flask import render_template, redirect, url_for, request, flash, jsonify
from . import produccion_bp
from app.auth.routes import admin_required
from app.models import Produccion, Bebida, Usuario, Pedido
from app import db
from datetime import date

@produccion_bp.route('/')
@admin_required
def index():
    producciones = Produccion.query.order_by(Produccion.fecha_produccion.desc()).all()
    bebidas = Bebida.query.filter_by(activo=True).all()
    return render_template('admin/produccion.html',
        producciones=producciones,
        bebidas=bebidas
    )

@produccion_bp.route('/nueva', methods=['POST'])
@admin_required
def nueva():
    try:
        from flask import session
        bebida_id = int(request.form.get('bebida_id'))
        cantidad = int(request.form.get('cantidad_producida'))
        fecha = request.form.get('fecha_produccion')
        notas = request.form.get('notas', '')

        # Calcular costo desde recetas
        bebida = Bebida.query.get(bebida_id)
        costo = 0
        for r in bebida.recetas.all():
            costo += float(r.cantidad) * float(r.materia_prima.precio_unitario)
        costo_total = costo * cantidad
        
        es_frio = True if request.form.get('es_frio') == 'on' else False
        
        if es_frio:
            costo_total +=100 * 0.015 * cantidad

        produccion = Produccion(
            bebida_id=bebida_id,
            cantidad_producida=cantidad,
            fecha_produccion=fecha,
            costo_produccion=costo_total,
            usuario_registrado_id=session['user_id'],
            notas=notas,
            estado='planificada'
        )
        db.session.add(produccion)
        db.session.commit()
        flash('Producción registrada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('admin_produccion.index'))

@produccion_bp.route('/completar/<int:id>', methods=['POST'])
@admin_required
def completar(id):
    try:
        produccion = Produccion.query.get_or_404(id)
        produccion.estado = 'completada'
        db.session.commit()
        flash(f'Producción #{id} completada. Stock actualizado automáticamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('admin_produccion.index'))

@produccion_bp.route('/cancelar/<int:id>', methods=['POST'])
@admin_required
def cancelar(id):
    produccion = Produccion.query.get_or_404(id)
    produccion.estado = 'cancelada'
    db.session.commit()
    flash(f'Producción #{id} cancelada.', 'info')
    return redirect(url_for('admin_produccion.index'))