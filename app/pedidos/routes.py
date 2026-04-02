from flask import render_template, redirect, url_for, flash, session, request, jsonify
from . import pedidos_bp
from app.models import Pedido, DetallePedido, Bebida, Usuario
from app import db
from app.auth.routes import login_required
from decimal import Decimal
from datetime import datetime

def generar_referencia(pedido_id):
    fecha = datetime.now().strftime('%Y%m%d')
    return f'CT-{fecha}-{str(pedido_id).zfill(3)}'

@pedidos_bp.route('/crear', methods=['POST'])
@login_required
def crear():
    cart = session.get('cart', {})
    if not cart:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('cliente.menu'))

    usuario = Usuario.query.get(session['user_id'])

    subtotal = Decimal('0')
    detalles = []
    for bebida_id, cantidad in cart.items():
        bebida = Bebida.query.get(int(bebida_id))
        if bebida and bebida.disponible:
            item_subtotal = bebida.precio * cantidad
            subtotal += Decimal(str(item_subtotal))
            detalles.append({
                'bebida_id': bebida.id,
                'cantidad': cantidad,
                'precio_unitario': bebida.precio,
                'subtotal': item_subtotal
            })

    if not detalles:
        flash('No hay bebidas disponibles en tu carrito.', 'warning')
        return redirect(url_for('carrito.ver_carrito'))

    tipo_entrega = request.form.get('tipo_entrega', 'sucursal')
    telefono = request.form.get('telefono') or usuario.telefono or 'N/A'
    direccion = request.form.get('direccion') or usuario.direccion or 'Recoger en sucursal'

    if tipo_entrega == 'sucursal':
        direccion = 'Recoger en sucursal'

    pedido = Pedido(
        usuario_id=session['user_id'],
        subtotal=subtotal,
        total=subtotal,
        direccion_entrega=direccion,
        telefono_contacto=telefono[:15],
        notas=request.form.get('notas', ''),
        estado='pendiente'
    )
    db.session.add(pedido)
    db.session.flush()

    # Generar referencia automatica
    pedido.notas = (pedido.notas or '') + f' | REF: {generar_referencia(pedido.id)}'

    for d in detalles:
        detalle = DetallePedido(
            pedido_id=pedido.id,
            bebida_id=d['bebida_id'],
            cantidad=d['cantidad'],
            precio_unitario=d['precio_unitario'],
            subtotal=d['subtotal']
        )
        db.session.add(detalle)

    db.session.commit()
    session.pop('cart', None)
    flash(f'Pedido #{pedido.id} confirmado exitosamente.', 'success')
    return redirect(url_for('pedidos.mis_pedidos'))


@pedidos_bp.route('/mis-pedidos')
@login_required
def mis_pedidos():
    pedidos = Pedido.query.filter_by(
        usuario_id=session['user_id']
    ).order_by(Pedido.fecha_pedido.desc()).all()
    return render_template('cliente/mis_pedidos.html', pedidos=pedidos)


@pedidos_bp.route('/detalle/<int:id>')
@login_required
def detalle(id):
    pedido = Pedido.query.get_or_404(id)
    if pedido.usuario_id != session['user_id']:
        return jsonify({'error': 'No autorizado'}), 403
    return jsonify({
        'id': pedido.id,
        'total': str(pedido.total),
        'estado': pedido.estado,
        'direccion': pedido.direccion_entrega,
        'telefono': pedido.telefono_contacto,
        'notas': pedido.notas,
        'fecha': pedido.fecha_pedido.strftime('%d/%m/%Y %H:%M'),
        'detalles': [{
            'bebida': d.bebida.nombre,
            'cantidad': d.cantidad,
            'precio_unitario': str(d.precio_unitario),
            'subtotal': str(d.subtotal)
        } for d in pedido.detalles.all()]
    })