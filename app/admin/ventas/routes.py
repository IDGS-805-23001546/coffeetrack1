from flask import render_template, redirect, url_for, request, flash, jsonify, session
from . import ventas_bp
from app.auth.routes import admin_required
from app.models import Venta, Pedido, DetallePedido
from app import db
from datetime import date, datetime, timedelta
import pytz

@ventas_bp.route('/')
@admin_required
def index():
    tz_mexico = pytz.timezone('America/Mexico_City')
    ahora = datetime.now(tz_mexico)
    hoy = ahora.date()
    inicio_semana = (ahora - timedelta(days=ahora.weekday())).date()

    ventas = Venta.query.order_by(Venta.fecha_venta.desc()).all()
    ventas_pendientes = Venta.query.filter_by(estado_pago='pendiente').all()

    # Total del dia en hora Mexico
    ventas_hoy = []
    for v in ventas:
        fecha_mx = v.fecha_venta.replace(tzinfo=pytz.utc).astimezone(tz_mexico).date()
        if fecha_mx == hoy and v.estado_pago == 'pagado':
            ventas_hoy.append(v)
    total_hoy = sum(float(v.total) for v in ventas_hoy)

    # Grafica semanal
    dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    datos_semana = []
    for i in range(7):
        dia = inicio_semana + timedelta(days=i)
        total_dia = 0
        for v in ventas:
            fecha_mx = v.fecha_venta.replace(tzinfo=pytz.utc).astimezone(tz_mexico).date()
            if fecha_mx == dia and v.estado_pago == 'pagado':
                total_dia += float(v.total)
        datos_semana.append({'dia': dias[i], 'total': total_dia})

    return render_template('admin/ventas.html',
        ventas=ventas,
        ventas_pendientes=ventas_pendientes,
        total_hoy=total_hoy,
        transacciones_hoy=len(ventas_hoy),
        datos_semana=datos_semana,
        tz_mexico=tz_mexico,
        timedelta=timedelta
    )

@ventas_bp.route('/confirmar/<int:id>', methods=['POST'])
@admin_required
def confirmar(id):
    venta = Venta.query.get_or_404(id)
    try:
        venta.metodo_pago = request.form.get('metodo_pago')
        venta.estado_pago = 'pagado'
        venta.referencia_pago = request.form.get('referencia_pago') or venta.referencia_pago
        pedido = Pedido.query.get(venta.pedido_id)
        if pedido and pedido.notas:
            pedido.notas = pedido.notas.replace('| REF:', f'| PAGADO | REF:')
        db.session.commit()
        flash(f'Venta #{id} confirmada como pagada.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('admin_ventas.index'))

@ventas_bp.route('/cambiar_estado/<int:id>', methods=['POST'])
@admin_required
def cambiar_estado(id):
    venta = Venta.query.get_or_404(id)
    nuevo_estado = request.form.get('estado_pago')
    if nuevo_estado in ['pendiente', 'pagado', 'reembolsado']:
        venta.estado_pago = nuevo_estado
        db.session.commit()
        flash(f'Estado de venta #{id} actualizado.', 'success')
    return redirect(url_for('admin_ventas.index'))

@ventas_bp.route('/detalle/<int:id>')
@admin_required
def detalle(id):
    venta = Venta.query.get_or_404(id)
    pedido = venta.pedido
    return jsonify({
        'id': venta.id,
        'pedido_id': pedido.id,
        'cliente': f'{pedido.usuario.nombre} {pedido.usuario.apellidos}',
        'direccion': pedido.direccion_entrega,
        'telefono': pedido.telefono_contacto,
        'metodo_pago': venta.metodo_pago,
        'total': str(venta.total),
        'estado_pago': venta.estado_pago,
        'referencia': venta.referencia_pago or '—',
        'detalles': [{
            'bebida': d.bebida.nombre,
            'cantidad': d.cantidad,
            'precio_unitario': str(d.precio_unitario),
            'subtotal': str(d.subtotal)
        } for d in pedido.detalles.all()]
    })