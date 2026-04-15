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

    inicio_semana = hoy - timedelta(days=6)

    ventas = Venta.query.order_by(Venta.fecha_venta.desc()).all()
    ventas_pendientes = Venta.query.filter_by(estado_pago='pendiente').all()

    # Total del dia
    ventas_hoy = []
    for v in ventas:
        fecha_mx = v.fecha_venta.replace(tzinfo=pytz.utc).astimezone(tz_mexico).date()
        if fecha_mx == hoy and v.estado_pago == 'pagado':
            ventas_hoy.append(v)
    total_hoy = sum(float(v.total) for v in ventas_hoy)

    # Grafica: ultimos 7 dias
    datos_semana = []
    for i in range(7):
        dia = inicio_semana + timedelta(days=i)
        total_dia = 0
        for v in ventas:
            fecha_mx = v.fecha_venta.replace(tzinfo=pytz.utc).astimezone(tz_mexico).date()
            if fecha_mx == dia and v.estado_pago == 'pagado':
                total_dia += float(v.total)
        nombre_dia = ['Lun','Mar','Mié','Jue','Vie','Sáb','Dom'][dia.weekday()]
        datos_semana.append({
            'dia': f"{nombre_dia}\n{dia.strftime('%d/%m')}",
            'total': total_dia,
            'fecha': dia.strftime('%d/%m')
        })

    # Agrupar ventas por dia para el historial
    ventas_por_dia = {}
    for v in ventas:
        if v.estado_pago == 'pagado':
            fecha_mx = v.fecha_venta.replace(tzinfo=pytz.utc).astimezone(tz_mexico).date()
            key = fecha_mx.strftime('%Y-%m-%d')
            label = fecha_mx.strftime('%d/%m/%Y')
            if key not in ventas_por_dia:
                ventas_por_dia[key] = {
                    'label': label,
                    'ventas': [],
                    'total_dia': 0
                }
            ventas_por_dia[key]['ventas'].append(v)
            ventas_por_dia[key]['total_dia'] += float(v.total)

    ventas_por_dia = dict(sorted(ventas_por_dia.items(), reverse=True))

    # Ventas por mes — últimos 6 meses
    nombres_meses = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    meses_labels = []
    meses_valores = []
    meses_cantidades = []

    for i in range(5, -1, -1):
        mes_fecha = hoy.replace(day=1)
        for _ in range(i):
            mes_fecha = (mes_fecha - timedelta(days=1)).replace(day=1)
        mes_num = mes_fecha.month
        anio_num = mes_fecha.year
        total_mes = 0
        cant_mes = 0
        for v in ventas:
            if v.estado_pago == 'pagado':
                fecha_mx = v.fecha_venta.replace(tzinfo=pytz.utc).astimezone(tz_mexico).date()
                if fecha_mx.month == mes_num and fecha_mx.year == anio_num:
                    total_mes += float(v.total)
                    cant_mes += 1
        meses_labels.append(f"{nombres_meses[mes_num-1]} {anio_num}")
        meses_valores.append(round(total_mes, 2))
        meses_cantidades.append(cant_mes)

    # Ventas por día de la semana actual completa (Lun-Dom)
    semana_labels = []
    semana_valores = []
    semana_cantidades = []
    inicio_semana_lunes = hoy - timedelta(days=hoy.weekday())

    for i in range(7):
        dia = inicio_semana_lunes + timedelta(days=i)
        total_dia = 0
        cant_dia = 0
        for v in ventas:
            if v.estado_pago == 'pagado':
                fecha_mx = v.fecha_venta.replace(tzinfo=pytz.utc).astimezone(tz_mexico).date()
                if fecha_mx == dia:
                    total_dia += float(v.total)
                    cant_dia += 1
        nombre_dia = ['Lun','Mar','Mié','Jue','Vie','Sáb','Dom'][dia.weekday()]
        semana_labels.append(f"{nombre_dia} {dia.strftime('%d/%m')}")
        semana_valores.append(round(total_dia, 2))
        semana_cantidades.append(cant_dia)

    return render_template('admin/ventas.html',
        ventas=ventas,
        ventas_pendientes=ventas_pendientes,
        total_hoy=total_hoy,
        transacciones_hoy=len(ventas_hoy),
        datos_semana=datos_semana,
        ventas_por_dia=ventas_por_dia,
        tz_mexico=tz_mexico,
        timedelta=timedelta,
        pytz=pytz,
        meses_labels=meses_labels,
        meses_valores=meses_valores,
        meses_cantidades=meses_cantidades,
        semana_labels=semana_labels,
        semana_valores=semana_valores,
        semana_cantidades=semana_cantidades,
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