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
        es_frio = True if request.form.get('es_frio') == 'on' else False

        bebida = Bebida.query.get(bebida_id)
        costo = 0

        # Verificar stock de materias primas
        advertencias = []
        for r in bebida.recetas.all():
            necesario = float(r.cantidad) * cantidad
            disponible = float(r.materia_prima.stock_actual)
            if disponible < necesario:
                advertencias.append(
                    f'{r.materia_prima.nombre}: necesitas {necesario} {r.unidad_medida} pero solo hay {disponible}'
                )
            costo += float(r.cantidad) * float(r.materia_prima.precio_unitario)

        costo_total = costo * cantidad
        if es_frio:
            costo_total += 100 * 0.015 * cantidad

        # Si hay advertencias las mostramos pero dejamos continuar
        if advertencias:
            for adv in advertencias:
                flash(f' Stock bajo: {adv}', 'warning')

        produccion = Produccion(
            bebida_id=bebida_id,
            cantidad_producida=cantidad,
            fecha_produccion=fecha,
            costo_produccion=costo_total,
            usuario_registrado_id=session['user_id'],
            notas=notas,
            estado='planificada',
            es_frio=es_frio
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
        bebida = produccion.bebida

        # Verificar stock suficiente antes de completar
        faltantes = []
        for r in bebida.recetas.all():
            necesario = float(r.cantidad) * produccion.cantidad_producida
            disponible = float(r.materia_prima.stock_actual)
            if disponible < necesario:
                faltantes.append(
                    f'{r.materia_prima.nombre}: necesitas {necesario} {r.unidad_medida} pero solo hay {disponible}'
                )

        # Verificar hielo si es frio
        if produccion.es_frio:
            from app.models import MateriaPrima
            hielo = MateriaPrima.query.get(14)
            hielo_necesario = 100 * produccion.cantidad_producida
            if hielo and float(hielo.stock_actual) < hielo_necesario:
                faltantes.append(
                    f'Hielo: necesitas {hielo_necesario} gr pero solo hay {hielo.stock_actual} gr'
                )

        # Si faltan ingredientes BLOQUEAR
        if faltantes:
            for f in faltantes:
                flash(f' No se puede completar — {f}', 'danger')
            return redirect(url_for('admin_produccion.index'))

        # Todo bien, completar
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