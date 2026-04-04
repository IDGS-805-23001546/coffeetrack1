from flask import render_template, redirect, url_for, request, flash, jsonify, session
from . import ventas_bp
from app.auth.routes import admin_required
from app.models import Venta, Pedido
from app import db
from datetime import date, datetime, timedelta
from datetime import date, datetime, timedelta
import pytz

@ventas_bp.route('/')
@admin_required
def index():
    
    tz_mexico = pytz.timezone('America/Mexico_City')
    ahora = datetime.now(tz_mexico)
    hoy = ahora.date()
    
    ventas = Venta.query.order_by(Venta.fecha_venta.desc()).all()

    # Ventas pendientes de confirmar metodo de pago
    ventas_pendientes = Venta.query.filter_by(estado_pago='pendiente').all()

    # Total del dia
    hoy = date.today()
    ventas_hoy = Venta.query.filter(
        Venta.fecha_venta >= hoy,
        Venta.estado_pago == 'pagado'
    ).all()
    total_hoy = sum(float(v.total) for v in ventas_hoy)

    # Datos grafica semanal
    hoy_dt = datetime.now()
    inicio_semana = hoy_dt - timedelta(days=hoy_dt.weekday())
    dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    datos_semana = []
    for i in range(7):
        dia = inicio_semana + timedelta(days=i)
        total_dia = sum(
            float(v.total) for v in ventas
            if v.fecha_venta.date() == dia.date() and v.estado_pago == 'pagado'
        )
        datos_semana.append({'dia': dias[i], 'total': total_dia})

    return render_template('admin/ventas.html',
        ventas=ventas,
        ventas_pendientes=ventas_pendientes,
        total_hoy=total_hoy,
        transacciones_hoy=len(ventas_hoy),
        datos_semana=datos_semana
    )

@ventas_bp.route('/confirmar/<int:id>', methods=['POST'])
@admin_required
def confirmar(id):
    venta = Venta.query.get_or_404(id)
    try:
        venta.metodo_pago = request.form.get('metodo_pago')
        venta.estado_pago = 'pagado'
        venta.referencia_pago = request.form.get('referencia_pago') or venta.referencia_pago

        # Reflejar en pedido como pagado en notas
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