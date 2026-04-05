from flask import render_template, redirect, url_for, request, flash, jsonify, session
from . import pedidos_admin_bp
from app.auth.routes import admin_required
from app.models import Pedido, DetallePedido, Produccion, Venta
from app import db
from datetime import date

@pedidos_admin_bp.route('/')
@admin_required
def index():
    pedidos = Pedido.query.order_by(Pedido.fecha_pedido.desc()).all()
    detalles = DetallePedido.query.all()
    return render_template('admin/pedidos.html',
        pedidos=pedidos,
        detalles=detalles
    )

@pedidos_admin_bp.route('/cambiar_estado/<int:id>', methods=['POST'])
@admin_required
def cambiar_estado(id):
    pedido = Pedido.query.get_or_404(id)
    nuevo_estado = request.form.get('estado')
    estados_validos = ['pendiente', 'confirmado', 'en_preparacion', 'enviado', 'entregado', 'cancelado']

    if nuevo_estado not in estados_validos:
        flash('Estado no válido.', 'danger')
        return redirect(url_for('admin_pedidos.index'))

    try:
        pedido.estado = nuevo_estado

        # Al pasar a en_preparacion crear produccion automaticamente
        if nuevo_estado == 'en_preparacion':
            for detalle in pedido.detalles.all():
                bebida = detalle.bebida
                es_frio = detalle.temperatura == 'frio'
                costo = sum(
                    float(r.cantidad) * float(r.materia_prima.precio_unitario)
                    for r in bebida.recetas.all()
                )
                costo_total = costo * detalle.cantidad

                # Si es frio agregar costo de hielo
                if es_frio:
                    costo_total += 100 * 0.015 * detalle.cantidad

                produccion = Produccion(
                    bebida_id=detalle.bebida_id,
                    cantidad_producida=detalle.cantidad,
                    fecha_produccion=date.today(),
                    costo_produccion=costo_total,
                    usuario_registrado_id=session['user_id'],
                    notas=f'Generado automáticamente por Pedido #{pedido.id}',
                    estado='planificada',
                    es_frio=es_frio
                )
                db.session.add(produccion)

        # Al marcar como entregado crear venta automaticamente
        if nuevo_estado == 'entregado':
            existe_venta = Venta.query.filter_by(pedido_id=pedido.id).first()
            if not existe_venta:
                # Extraer referencia del pedido
                ref = None
                if pedido.notas and 'REF:' in pedido.notas:
                    ref = pedido.notas.split('REF:')[-1].strip()

                venta = Venta(
                    pedido_id=pedido.id,
                    metodo_pago='efectivo',  # por defecto, el admin cambia despues
                    total=pedido.total,
                    estado_pago='pendiente',
                    referencia_pago=ref
                )
                db.session.add(venta)

        db.session.commit()
        flash(f'Pedido #{id} actualizado a {nuevo_estado}.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('admin_pedidos.index'))

@pedidos_admin_bp.route('/detalle/<int:id>')
@admin_required
def detalle(id):
    pedido = Pedido.query.get_or_404(id)
    return jsonify({
        'id': pedido.id,
        'cliente': f'{pedido.usuario.nombre} {pedido.usuario.apellidos}',
        'direccion': pedido.direccion_entrega,
        'telefono': pedido.telefono_contacto,
        'notas': pedido.notas,
        'estado': pedido.estado,
        'total': str(pedido.total),
        'detalles': [{
            'bebida': d.bebida.nombre,
            'cantidad': d.cantidad,
            'temperatura': d.temperatura,
            'precio_unitario': str(d.precio_unitario),
            'subtotal': str(d.subtotal)
        } for d in pedido.detalles.all()]
    })