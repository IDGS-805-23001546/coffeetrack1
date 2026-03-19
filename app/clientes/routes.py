from flask import Blueprint, render_template, redirect, url_for, flash, session, request, jsonify
from app.models import Bebida, CategoriaBebida, Pedido, DetallePedido, Venta
from app.forms import PedidoForm
from app.auth.routes import login_required
from app import db
from decimal import Decimal
from . import cliente_bp 


@cliente_bp.route('/')
def inicio():
    bebidas_destacadas = Bebida.query.all() 
    print(f"DEBUG: Se encontraron {len(bebidas_destacadas)} bebidas")
    return render_template('cliente/inicio.html', bebidas=bebidas_destacadas)

@cliente_bp.route('/menu')
def menu():
    categorias = CategoriaBebida.query.all()
    # Esto traerá todas las bebidas ignorando si están activas o no
    bebidas = Bebida.query.all() 
    print(f"DEBUG: Se encontraron {len(bebidas)} bebidas en la DB") # Esto saldrá en tu terminal
    return render_template('cliente/menu.html', categorias=categorias, bebidas=bebidas)


@cliente_bp.route('/nosotros')
def about():
    return render_template('cliente/about.html')


@cliente_bp.route('/carrito')
@login_required
def carrito():
    cart = session.get('cart', {})
    items = []
    total = Decimal('0')
    for bebida_id, cantidad in cart.items():
        bebida = Bebida.query.get(int(bebida_id))
        if bebida:
            subtotal = bebida.precio * cantidad
            total += subtotal
            items.append({
                'bebida': bebida,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
    return render_template('cliente/carrito.html', items=items, total=total)

@cliente_bp.route('/carrito/agregar/<int:bebida_id>', methods=['POST'])
@login_required
def agregar_carrito(bebida_id):
    bebida = Bebida.query.get_or_404(bebida_id)
    if not bebida.disponible or not bebida.activo:
        flash('Esta bebida no está disponible.', 'warning')
        return redirect(url_for('cliente.menu'))

    cart = session.get('cart', {})
    str_id = str(bebida_id)
    cantidad = int(request.form.get('cantidad', 1))
    cart[str_id] = cart.get(str_id, 0) + cantidad
    session['cart'] = cart
    flash(f'{bebida.nombre} agregado al carrito.', 'success')
    return redirect(url_for('cliente.menu'))

@cliente_bp.route('/carrito/eliminar/<int:bebida_id>', methods=['POST'])
@login_required
def eliminar_carrito(bebida_id):
    cart = session.get('cart', {})
    str_id = str(bebida_id)
    if str_id in cart:
        del cart[str_id]
        session['cart'] = cart
        flash('Producto eliminado del carrito.', 'info')
    return redirect(url_for('cliente.carrito'))


@cliente_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('cliente.menu'))

    form = PedidoForm()
    if form.validate_on_submit():
        subtotal = Decimal('0')
        detalles = []
        for bebida_id, cantidad in cart.items():
            bebida = Bebida.query.get(int(bebida_id))
            if bebida and bebida.disponible:
                item_subtotal = bebida.precio * cantidad
                subtotal += item_subtotal
                detalles.append({
                    'bebida_id': bebida.id,
                    'cantidad': cantidad,
                    'precio_unitario': bebida.precio,
                    'subtotal': item_subtotal
                })

        pedido = Pedido(
            usuario_id=session['user_id'],
            subtotal=subtotal,
            total=subtotal,
            direccion_entrega=form.direccion_entrega.data,
            telefono_contacto=form.telefono_contacto.data,
            notas=form.notas.data
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
        flash(f'¡Pedido #{pedido.id} creado exitosamente!', 'success')
        return redirect(url_for('cliente.mis_pedidos'))

    return render_template('cliente/carrito.html', form=form, checkout=True)


@cliente_bp.route('/mis-pedidos')
@login_required
def mis_pedidos():
    pedidos = Pedido.query.filter_by(usuario_id=session['user_id']).order_by(
        Pedido.fecha_pedido.desc()
    ).all()
    return render_template('cliente/mis_pedidos.html', pedidos=pedidos)