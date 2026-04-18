from flask import render_template, redirect, url_for, flash, session, request
from . import carrito_bp
from app.models import Bebida, MateriaPrima
from app.auth.routes import login_required

HIELO_ID = 14          # ID de la materia prima Hielo
HIELO_POR_BEBIDA = 100 # gramos de hielo por bebida fría


def calcular_capacidad(bebida, cart=None, excluir_key=None, temperatura='caliente'):
    """
    Calcula cuántas unidades se pueden producir considerando
    lo que ya está en el carrito (reserva de ingredientes compartidos).
    Si temperatura='frio', también verifica el stock de hielo.
    """
    recetas = bebida.recetas.all()
    if not recetas:
        return 999  # Sin receta = sin límite

    # Calcular reservas del carrito actual
    reservas = {}
    if cart:
        for key, datos in cart.items():
            if excluir_key and key == excluir_key:
                continue
            cant = datos['cantidad'] if isinstance(datos, dict) else datos
            temp_key = key.split('_')[1] if '_' in key else 'caliente'
            bid = int(key.split('_')[0])
            b = Bebida.query.get(bid)
            if b:
                for r in b.recetas.all():
                    mp_id = r.materia_prima_id
                    reservas[mp_id] = reservas.get(mp_id, 0) + float(r.cantidad) * cant
                # Si esta bebida del carrito es fría → reservar hielo
                if temp_key == 'frio':
                    reservas[HIELO_ID] = reservas.get(HIELO_ID, 0) + HIELO_POR_BEBIDA * cant

    caps = []
    for r in recetas:
        mp = r.materia_prima
        if mp and float(r.cantidad) > 0:
            stock_libre = float(mp.stock_actual) - reservas.get(mp.id, 0)
            caps.append(int(stock_libre // float(r.cantidad)))

    # Si pide frío → verificar también el hielo disponible
    if temperatura == 'frio':
        hielo = MateriaPrima.query.get(HIELO_ID)
        if hielo:
            stock_hielo_libre = float(hielo.stock_actual) - reservas.get(HIELO_ID, 0)
            caps.append(int(stock_hielo_libre // HIELO_POR_BEBIDA))

    return max(0, min(caps)) if caps else 0


def get_cantidad_carrito(cart, key):
    if key not in cart:
        return 0
    datos = cart[key]
    return datos['cantidad'] if isinstance(datos, dict) else datos


@carrito_bp.route('/')
@login_required
def ver_carrito():
    cart = session.get('cart', {})
    items = []
    total = 0
    for key, datos in cart.items():
        bebida_id = int(key.split('_')[0])
        bebida = Bebida.query.get(bebida_id)
        if bebida:
            if isinstance(datos, dict):
                cantidad = datos['cantidad']
                temperatura = datos.get('temperatura', 'caliente')
            else:
                cantidad = datos
                temperatura = 'caliente'
            subtotal = bebida.precio * cantidad
            total += subtotal
            items.append({
                'bebida': bebida,
                'cantidad': cantidad,
                'temperatura': temperatura,
                'subtotal': subtotal,
                'key': key
            })
    return render_template('cliente/carrito.html', items=items, total=total)


@carrito_bp.route('/agregar/<int:bebida_id>', methods=['POST'])
@login_required
def agregar(bebida_id):
    cart = session.get('cart', {})
    cantidad = int(request.form.get('cantidad', 1))
    temperatura = request.form.get('temperatura', 'caliente')
    key = f"{bebida_id}_{temperatura}"

    bebida = Bebida.query.get(bebida_id)
    if not bebida or not bebida.disponible or not bebida.activo:
        flash('Esta bebida no está disponible.', 'danger')
        return redirect(url_for('cliente.menu'))

    # Capacidad considerando ingredientes reservados + hielo si es frío
    capacidad = calcular_capacidad(bebida, cart=cart, excluir_key=key, temperatura=temperatura)
    cantidad_actual = get_cantidad_carrito(cart, key)
    cantidad_nueva = cantidad_actual + cantidad

    if capacidad == 0:
        if temperatura == 'frio':
            flash(f'No hay suficiente hielo para preparar {bebida.nombre} frío.', 'danger')
        else:
            flash(f'Lo sentimos, {bebida.nombre} no está disponible por falta de ingredientes.', 'danger')
        return redirect(url_for('cliente.menu'))

    if cantidad_nueva > capacidad:
        disponible = capacidad - cantidad_actual
        if disponible <= 0:
            flash(f'Ya tienes el máximo disponible de {bebida.nombre} ({capacidad} uds.).', 'warning')
        else:
            flash(f'Solo puedes agregar {disponible} más de {bebida.nombre}. Máximo disponible: {capacidad} uds.', 'warning')
        return redirect(url_for('carrito.ver_carrito'))

    if key in cart:
        cart[key]['cantidad'] += cantidad
    else:
        cart[key] = {'cantidad': cantidad, 'temperatura': temperatura}

    session['cart'] = cart
    session.modified = True
    temp_label = '🧊 Frío' if temperatura == 'frio' else '☕ Caliente'
    flash(f'{bebida.nombre} ({temp_label}) añadido al carrito.', 'success')
    return redirect(url_for('carrito.ver_carrito'))


@carrito_bp.route('/eliminar/<path:key>', methods=['POST'])
@login_required
def eliminar_carrito(key):
    cart = session.get('cart', {})
    if key in cart:
        del cart[key]
        session['cart'] = cart
        session.modified = True
        flash('Producto eliminado.', 'info')
    return redirect(url_for('carrito.ver_carrito'))


@carrito_bp.route('/aumentar/<path:key>', methods=['POST'])
@login_required
def aumentar(key):
    cart = session.get('cart', {})
    bebida_id = int(key.split('_')[0])
    temperatura = key.split('_')[1] if '_' in key else 'caliente'
    bebida = Bebida.query.get(bebida_id)
    if not bebida:
        return redirect(url_for('carrito.ver_carrito'))

    capacidad = calcular_capacidad(bebida, cart=cart, excluir_key=key, temperatura=temperatura)
    cantidad_actual = get_cantidad_carrito(cart, key)

    if cantidad_actual >= capacidad:
        if temperatura == 'frio':
            flash(f'No hay suficiente hielo para más {bebida.nombre} frío. Máximo: {capacidad} uds.', 'warning')
        else:
            flash(f'No puedes agregar más de {bebida.nombre}. Máximo disponible: {capacidad} uds.', 'warning')
        return redirect(url_for('carrito.ver_carrito'))

    if key in cart:
        if isinstance(cart[key], dict):
            cart[key]['cantidad'] += 1
        else:
            cart[key] = {'cantidad': cart[key] + 1, 'temperatura': temperatura}

    session['cart'] = cart
    session.modified = True
    return redirect(url_for('carrito.ver_carrito'))


@carrito_bp.route('/reducir/<path:key>', methods=['POST'])
@login_required
def reducir(key):
    cart = session.get('cart', {})
    if key in cart:
        if isinstance(cart[key], dict):
            cart[key]['cantidad'] -= 1
            if cart[key]['cantidad'] <= 0:
                del cart[key]
        else:
            cart[key] -= 1
            if cart[key] <= 0:
                del cart[key]
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('carrito.ver_carrito'))