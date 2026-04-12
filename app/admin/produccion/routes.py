from flask import render_template, redirect, url_for, request, flash, jsonify, session
from . import produccion_bp
from app.auth.routes import admin_required
from app.models import Produccion, Bebida, MateriaPrima
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
        bebida_id = int(request.form.get('bebida_id'))
        cantidad = int(request.form.get('cantidad_producida'))
        fecha = request.form.get('fecha_produccion')
        notas = request.form.get('notas', '')

        bebida = Bebida.query.get(bebida_id)
        costo = sum(
            float(r.cantidad) * float(r.materia_prima.precio_unitario)
            for r in bebida.recetas.all()
        )
        costo_total = costo * cantidad

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

@produccion_bp.route('/verificar_stock/<int:id>')
@admin_required
def verificar_stock(id):
    produccion = Produccion.query.get_or_404(id)
    bebida = produccion.bebida
    faltantes = []
    suficiente = True

    for r in bebida.recetas.all():
        cantidad_necesaria = float(r.cantidad) * produccion.cantidad_producida
        stock_disponible = float(r.materia_prima.stock_actual)
        if stock_disponible < cantidad_necesaria:
            suficiente = False
            faltante = cantidad_necesaria - stock_disponible
            faltantes.append({
                'materia': r.materia_prima.nombre,
                'categoria': r.materia_prima.categoria.nombre,
                'necesario': round(cantidad_necesaria, 2),
                'disponible': round(stock_disponible, 2),
                'faltante': round(faltante, 2),
                'unidad': r.unidad_medida,
                'precio_unitario': float(r.materia_prima.precio_unitario),
                'costo_faltante': round(faltante * float(r.materia_prima.precio_unitario), 2)
            })

    return jsonify({
        'puede_completar': suficiente,
        'bebida': bebida.nombre,
        'cantidad': produccion.cantidad_producida,
        'faltantes': faltantes,
        'total_costo_faltante': round(sum(f['costo_faltante'] for f in faltantes), 2)
    })

@produccion_bp.route('/completar/<int:id>', methods=['POST'])
@admin_required
def completar(id):
    try:
        produccion = Produccion.query.get_or_404(id)
        bebida = produccion.bebida

        # Verificar stock antes de completar
        faltantes = []
        for r in bebida.recetas.all():
            cantidad_necesaria = float(r.cantidad) * produccion.cantidad_producida
            stock_disponible = float(r.materia_prima.stock_actual)
            if stock_disponible < cantidad_necesaria:
                faltantes.append({
                    'materia': r.materia_prima.nombre,
                    'necesario': round(cantidad_necesaria, 2),
                    'disponible': round(stock_disponible, 2),
                    'faltante': round(cantidad_necesaria - stock_disponible, 2),
                    'unidad': r.unidad_medida
                })

        if faltantes:
            msgs = [f"{f['materia']}: faltan {f['faltante']} {f['unidad']}" for f in faltantes]
            flash(f'No se puede completar la producción. Stock insuficiente: {", ".join(msgs)}. Por favor realiza una compra antes de continuar.', 'danger')
            return redirect(url_for('admin_produccion.index'))

        produccion.estado = 'completada'
        db.session.commit()
        flash(f'Producción #{id} completada. Stock de materia prima actualizado automáticamente.', 'success')
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