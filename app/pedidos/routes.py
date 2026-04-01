from flask import render_template, redirect, url_for, flash, session, request
from . import pedidos_bp
from app.models import Pedido, DetallePedido, Bebida, Usuario
from app import db
from app.auth.routes import login_required
from decimal import Decimal


@pedidos_bp.route('/crear', methods=['POST'])
@login_required
def crear():
    cart = session.get('cart', {})
    if not cart:
        flash('Tu carrito esta vacio.', 'warning')
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
                'bebida_id':bebida.id,
                'cantidad':cantidad,
                'precio_unitario':bebida.precio,
                'subtotal':item_subtotal
            })
            
    if not detalles:
        flash('No hay bebidas disponibles en tu carrito.', 'warning')
        return redirect(url_for('carrito.ver_carrito'))
    
    tipo_entrega = request.form.get('tipo_entrega', 'sucursal')
    if tipo_entrega == 'domicilio':
        direccion == usuario_direccion or 'Sin direccion registrada' 
        
    else:
        direccion = 'Recoger en Sucursal'
        
    telefono = usuario.telefono or 'N/A'
    
    pedido = Pedido (
        usuario_id = session['user_id'],
        subtotal = subtotal,
        total = subtotal,
        direccion_entrega = direccion,
        telefono_contacto = telefono,
        notas=request.form.get('notas', ''),
        estado = 'pendiente'
    )
    
    db.session.add(pedido)
    db.session.flush()
    
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
    flash(f'Pedido #{pedido.id} creado exitosamente.', 'success')
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
    from flask import jsonify
    pedido = Pedido.query.get_or_404(id)
    if pedido.usuario_id != session['user_id']:
        return jsonify({'error': 'No autorizado'}), 403
    return jsonify({
        'id': pedido.id,
        'total': str(pedido.total),
        'estado': pedido.estado,
        'detalles': [{
            'bebida': d.bebida.nombre,
            'cantidad': d.cantidad,
            'precio_unitario': str(d.precio_unitario),
            'subtotal': str(d.subtotal)
        } for d in pedido.detalles.all()]
    })