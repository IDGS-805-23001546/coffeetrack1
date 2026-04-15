from flask import render_template, redirect, url_for, request, flash, jsonify, session
from . import pedidos_admin_bp
from app.auth.routes import admin_required
from app.models import Pedido, DetallePedido, Produccion, Venta, Bebida
from app import db
from datetime import date, datetime, timedelta
import pytz


def calcular_entrega_rapida(pedido, minutos_prep):
    """Recalcula hora estimada con tiempo de preparación reducido"""
    tz_mexico = pytz.timezone('America/Mexico_City')
    ahora = datetime.now(tz_mexico)
    hoy = ahora.date()

    hora_actual = ahora.hour * 60 + ahora.minute
    entrega_min = hora_actual + minutos_prep

    horas = entrega_min // 60
    minutos = entrega_min % 60

    # Si se pasa de medianoche
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

    # Verificar stock disponible para cada pedido pendiente
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
        stock_info=stock_info
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

        # Al pasar a en_preparacion
        if nuevo_estado == 'en_preparacion':
            bebidas_en_stock = []
            bebidas_a_producir = []

            for detalle in pedido.detalles.all():
                bebida = detalle.bebida
                es_frio = detalle.temperatura == 'frio'

                # Verificar si ya hay stock producido disponible
                if bebida.stock_actual >= detalle.cantidad:
                    # Ya hay stock — no crear producción
                    bebidas_en_stock.append(f"{detalle.cantidad}x {bebida.nombre}")
                else:
                    # No hay stock suficiente — crear producción
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

            # Mensajes informativos
            if bebidas_en_stock:
                flash(
                    f'Stock disponible para: {", ".join(bebidas_en_stock)}. '
                    f'No se necesita producir de nuevo.',
                    'success'
                )

                # Reducir tiempo de entrega si TODO está en stock
                if not bebidas_a_producir:
                    # Todo en stock — tiempo reducido a 5 minutos
                    tipo_entrega = 'domicilio' if pedido.direccion_entrega != 'Recoger en sucursal' else 'sucursal'
                    hora_rapida, dia_rapido = calcular_entrega_rapida(pedido, 5)
                    pedido.hora_estimada_entrega = hora_rapida
                    pedido.dia_entrega = dia_rapido
                    flash(
                        f'⚡ Entrega rápida — todo está listo. Nueva hora estimada: {hora_rapida}',
                        'info'
                    )

            if bebidas_a_producir:
                flash(
                    f'Se creó orden de producción para: {", ".join(bebidas_a_producir)}.',
                    'info'
                )

        # Al marcar como entregado crear venta automáticamente
        if nuevo_estado == 'entregado':
            existe_venta = Venta.query.filter_by(pedido_id=pedido.id).first()
            if not existe_venta:
                ref = None
                if pedido.notas and 'REF:' in pedido.notas:
                    ref = pedido.notas.split('REF:')[-1].strip()

                venta = Venta(
                    pedido_id=pedido.id,
                    metodo_pago='efectivo',
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
        'hora_estimada': pedido.hora_estimada_entrega or '—',
        'detalles': [{
            'bebida': d.bebida.nombre,
            'cantidad': d.cantidad,
            'temperatura': d.temperatura,
            'precio_unitario': str(d.precio_unitario),
            'subtotal': str(d.subtotal)
        } for d in pedido.detalles.all()]
    })