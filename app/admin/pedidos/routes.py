from flask import render_template, redirect, url_for, request, flash, jsonify, session
from . import pedidos_admin_bp
from app.auth.routes import admin_required
from app.models import Pedido, DetallePedido, Produccion, Venta, Bebida
from app import db
from datetime import date, datetime, timedelta
import pytz


def calcular_entrega_rapida(pedido, minutos_prep):
    tz_mexico = pytz.timezone('America/Mexico_City')
    ahora = datetime.now(tz_mexico)
    hoy = ahora.date()
    hora_actual = ahora.hour * 60 + ahora.minute
    entrega_min = hora_actual + minutos_prep
    horas = entrega_min // 60
    minutos = entrega_min % 60
    if horas >= 24:
        horas = horas - 24
        dia = hoy + timedelta(days=1)
    else:
        dia = hoy
    return f"{horas:02d}:{minutos:02d}", dia


@pedidos_admin_bp.route('/')
@admin_required
def index():
    pedidos = Pedido.query.order_by(Pedido.fecha_pedido.desc()).all()
    detalles = DetallePedido.query.all()
    bebidas_disponibles = Bebida.query.filter_by(activo=True, disponible=True).all()

    stock_info = {}
    for pedido in pedidos:
        if pedido.estado in ['pendiente', 'confirmado']:
            info = []
            for d in pedido.detalles.all():
                stock_disponible = d.bebida.stock_actual
                tiene_stock = stock_disponible >= d.cantidad
                info.append({
                    'bebida': d.bebida.nombre,
                    'cantidad_pedida': d.cantidad,
                    'stock_disponible': stock_disponible,
                    'tiene_stock': tiene_stock
                })
            todo_en_stock = all(i['tiene_stock'] for i in info)
            stock_info[pedido.id] = {
                'items': info,
                'todo_disponible': todo_en_stock
            }

    return render_template('admin/pedidos.html',
        pedidos=pedidos,
        detalles=detalles,
        timedelta=timedelta,
        stock_info=stock_info,
        bebidas_disponibles=bebidas_disponibles
    )


@pedidos_admin_bp.route('/nuevo_presencial', methods=['POST'])
@admin_required
def nuevo_presencial():
    try:
        nombre_cliente = request.form.get('nombre_cliente', 'Cliente Presencial')
        metodo_pago = request.form.get('metodo_pago', 'efectivo')
        notas = request.form.get('notas', '')

        bebida_ids = request.form.getlist('bebida_id[]')
        cantidades = request.form.getlist('cantidad[]')
        temperaturas = request.form.getlist('temperatura[]')

        if not bebida_ids or not any(b for b in bebida_ids):
            flash('Agrega al menos una bebida.', 'danger')
            return redirect(url_for('admin_pedidos.index'))

        subtotal = 0
        detalles = []
        for i in range(len(bebida_ids)):
            if not bebida_ids[i]:
                continue
            bebida = Bebida.query.get(int(bebida_ids[i]))
            if bebida:
                cant = int(cantidades[i])
                temp = temperaturas[i]
                sub = float(bebida.precio) * cant
                subtotal += sub
                detalles.append({
                    'bebida_id': bebida.id,
                    'cantidad': cant,
                    'temperatura': temp,
                    'precio_unitario': float(bebida.precio),
                    'subtotal': sub
                })

        if not detalles:
            flash('No hay bebidas válidas en el pedido.', 'danger')
            return redirect(url_for('admin_pedidos.index'))

        fecha_str = datetime.now().strftime('%Y%m%d')

        pedido = Pedido(
            usuario_id=None,
            nombre_cliente=nombre_cliente,
            subtotal=subtotal,
            total=subtotal,
            costo_envio=0,
            direccion_entrega='Recoger en sucursal',
            telefono_contacto='N/A',
            notas=notas,
            estado='confirmado',
            metodo_pago_cliente=metodo_pago
        )
        db.session.add(pedido)
        db.session.flush()

        pedido.notas = (pedido.notas or '') + f' | REF: CT-{fecha_str}-{str(pedido.id).zfill(3)}'

        for d in detalles:
            detalle = DetallePedido(
                pedido_id=pedido.id,
                bebida_id=d['bebida_id'],
                cantidad=d['cantidad'],
                temperatura=d['temperatura'],
                precio_unitario=d['precio_unitario'],
                subtotal=d['subtotal']
            )
            db.session.add(detalle)

        db.session.commit()
        flash(f'Pedido presencial de {nombre_cliente} creado. #{pedido.id} — Total: ${subtotal:.2f}', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('admin_pedidos.index'))


@pedidos_admin_bp.route('/cambiar_estado/<int:id>', methods=['POST'])
@admin_required
def cambiar_estado(id):
    pedido = Pedido.query.get_or_404(id)
    nuevo_estado = request.form.get('estado')
    estados_validos = ['pendiente', 'confirmado', 'en_preparacion', 'enviado', 'entregado', 'cancelado']

    if nuevo_estado not in estados_validos:
        flash('Estado no válido.', 'danger')
        return redirect(url_for('admin_pedidos.index'))

    transacciones_validas = {
        'pendiente':      ['confirmado', 'cancelado'],
        'confirmado':     ['en_preparacion', 'cancelado'],
        'en_preparacion': ['enviado', 'entregado', 'cancelado'],
        'enviado':        ['entregado', 'cancelado'],
        'entregado':      [],
        'cancelado':      []
    }

    estado_actual = pedido.estado or 'pendiente'
    if nuevo_estado not in transacciones_validas.get(estado_actual, []):
        mensajes = {
            ('pendiente', 'en_preparacion'): 'Primero debes confirmar el pedido antes de mandarlo a producción.',
            ('pendiente', 'enviado'):        'Primero confirma el pedido y mándalo a producción.',
            ('pendiente', 'entregado'):      'Primero confirma el pedido y mándalo a producción.',
            ('confirmado', 'enviado'):       'Primero debes mandar el pedido a producción antes de enviarlo.',
            ('confirmado', 'entregado'):     'Primero debes mandar el pedido a producción.',
            ('en_preparacion', 'confirmado'):'El pedido ya está en producción, no puedes regresar a confirmado.',
        }
        msg = mensajes.get((estado_actual, nuevo_estado),
            f'No puedes cambiar de "{estado_actual}" a "{nuevo_estado}". Sigue el flujo correcto.')
        flash(msg, 'danger')
        return redirect(url_for('admin_pedidos.index'))

    try:
        pedido.estado = nuevo_estado

        if nuevo_estado == 'en_preparacion':
            bebidas_en_stock = []
            bebidas_a_producir = []

            for detalle in pedido.detalles.all():
                bebida = detalle.bebida
                es_frio = detalle.temperatura == 'frio'

                stock_planificado = sum(
                    p.cantidad_producida for p in bebida.producciones
                    if p.estado == 'planificada'
                    and f'Pedido #' not in (p.notas or '')
                )
                stock_real = bebida.stock_actual + stock_planificado

                if stock_real >= detalle.cantidad:
                    bebidas_en_stock.append(f"{detalle.cantidad}x {bebida.nombre}")
                else:
                    bebidas_a_producir.append(bebida.nombre)
                    costo = sum(
                        float(r.cantidad) * float(r.materia_prima.precio_unitario)
                        for r in bebida.recetas.all()
                    )
                    costo_total = costo * detalle.cantidad
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

            if bebidas_en_stock:
                flash(f'Stock disponible para: {", ".join(bebidas_en_stock)}. No se necesita producir de nuevo.', 'success')
                if not bebidas_a_producir:
                    hora_rapida, dia_rapido = calcular_entrega_rapida(pedido, 5)
                    pedido.hora_estimada_entrega = hora_rapida
                    pedido.dia_entrega = dia_rapido
                    flash(f'⚡ Entrega rápida — todo está listo. Nueva hora estimada: {hora_rapida}', 'info')

            if bebidas_a_producir:
                flash(f'Se creó orden de producción para: {", ".join(bebidas_a_producir)}.', 'info')

        if nuevo_estado == 'entregado':
            existe_venta = Venta.query.filter_by(pedido_id=pedido.id).first()
            if not existe_venta:
                ref = None
                if pedido.notas and 'REF:' in pedido.notas:
                    ref = pedido.notas.split('REF:')[-1].strip()

                venta = Venta(
                    pedido_id=pedido.id,
                    metodo_pago=pedido.metodo_pago_cliente or 'efectivo',
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
    if pedido.usuario:
        cliente = f'{pedido.usuario.nombre} {pedido.usuario.apellidos}'
    else:
        cliente = pedido.nombre_cliente or 'Cliente Presencial'

    return jsonify({
        'id': pedido.id,
        'cliente': cliente,
        'direccion': pedido.direccion_entrega,
        'telefono': pedido.telefono_contacto,
        'notas': pedido.notas,
        'estado': pedido.estado,
        'total': str(pedido.total),
        'hora_estimada': pedido.hora_estimada_entrega or '—',
        'detalles': [{
            'bebida': d.bebida.nombre,
            'cantidad': d.cantidad,
            'temperatura': d.temperatura,
            'precio_unitario': str(d.precio_unitario),
            'subtotal': str(d.subtotal)
        } for d in pedido.detalles.all()]
    })