from flask import render_template, redirect, url_for, flash, session, request
from . import carrito_bp
from app.models import Bebida
from app.auth.routes import login_required

@carrito_bp.route('/')
@login_required
def ver_carrito():
    cart = session.get('cart', {})
    items = []
    total = 0
    for bebida_id, cantidad in cart.items():
        bebida = Bebida.query.get(int(bebida_id))
        if bebida:
            subtotal = bebida.precio * cantidad
            total += subtotal
            items.append({'bebida': bebida, 'cantidad': cantidad, 'subtotal': subtotal})
    return render_template('cliente/carrito.html', items=items, total=total)

@carrito_bp.route('/agregar/<int:bebida_id>', methods=['POST'])
@login_required
def agregar(bebida_id):
    cart = session.get('cart', {})
    str_id = str(bebida_id)
    cantidad = int(request.form.get('cantidad', 1))
    
    cart[str_id] = cart.get(str_id, 0) + cantidad
    session['cart'] = cart
    session.modified = True
    
    flash('Producto añadido al carrito.', 'success')
    
    return redirect(url_for('carrito.ver_carrito'))

@carrito_bp.route('/eliminar/<int:bebida_id>', methods=['POST'])
@login_required
def eliminar_carrito(bebida_id):
    cart = session.get('cart', {})
    str_id = str(bebida_id)
    if str_id in cart:
        del cart[str_id]
        session['cart'] = cart
        session.modified = True
        flash('Producto eliminado.', 'info')
    return redirect(url_for('carrito.ver_carrito'))