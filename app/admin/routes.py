from flask import render_template, redirect, url_for, jsonify, request, flash, g
from . import admin_bp
from app.auth.routes import admin_required
from app.models import (Bebida, MateriaPrima, Pedido, Venta, AlertaInventario,
                        Produccion, CategoriaBebida, Receta, DetallePedido)
from app import db
from datetime import date, datetime, timedelta
import pytz

@admin_bp.before_request
def cargar_datos_globales():
    g.pedidos_pendientes = Pedido.query.filter_by(estado='pendiente').count()

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    from sqlalchemy import func

    tz_mexico = pytz.timezone('America/Mexico_City')
    ahora = datetime.now(tz_mexico)
    hoy = ahora.date()
    inicio_semana = (ahora - timedelta(days=ahora.weekday())).date()
    inicio_semana_anterior = inicio_semana - timedelta(days=7)
    inicio_mes = hoy.replace(day=1)

    # --- KPIs ---
    total_bebidas = Bebida.query.filter_by(activo=True).count()
    bebidas_disponibles = Bebida.query.filter_by(disponible=True, activo=True).count()
    total_materias = MateriaPrima.query.filter_by(activo=True).count()
    materias_ok = MateriaPrima.query.filter(
        MateriaPrima.stock_actual > MateriaPrima.stock_minimo,
        MateriaPrima.activo == True
    ).count()
    producciones_completadas = Produccion.query.filter_by(estado='completada').count()
    producciones_activas = Produccion.query.filter(
        Produccion.estado.in_(['planificada', 'en_proceso'])
    ).count()

    # Ventas hoy
    ventas_hoy_list = []
    for v in Venta.query.filter(Venta.estado_pago == 'pagado').all():
        fecha_mx = v.fecha_venta.replace(tzinfo=pytz.utc).astimezone(tz_mexico).date()
        if fecha_mx == hoy:
            ventas_hoy_list.append(v)
    total_ventas_hoy = sum(float(v.total) for v in ventas_hoy_list)
    transacciones_hoy = len(ventas_hoy_list)

    # Ventas del mes
    ventas_mes_list = []
    for v in Venta.query.filter(Venta.estado_pago == 'pagado').all():
        fecha_mx = v.fecha_venta.replace(tzinfo=pytz.utc).astimezone(tz_mexico).date()
        if fecha_mx >= inicio_mes:
            ventas_mes_list.append(v)
    total_ventas_mes = sum(float(v.total) for v in ventas_mes_list)

    # Pedidos pendientes
    pedidos_pendientes_count = Pedido.query.filter_by(estado='pendiente').count()

    # --- GRÁFICA 1: Ventas últimos 7 días ---
    dias_labels = []
    dias_valores = []
    todas_ventas = Venta.query.filter(Venta.estado_pago == 'pagado').all()
    for i in range(6, -1, -1):
        dia = hoy - timedelta(days=i)
        total_dia = 0
        for v in todas_ventas:
            fecha_mx = v.fecha_venta.replace(tzinfo=pytz.utc).astimezone(tz_mexico).date()
            if fecha_mx == dia:
                total_dia += float(v.total)
        nombre_dia = ['Lun','Mar','Mié','Jue','Vie','Sáb','Dom'][dia.weekday()]
        dias_labels.append(f"{nombre_dia} {dia.strftime('%d/%m')}")
        dias_valores.append(round(total_dia, 2))

    # --- GRÁFICA 2: Ventas últimos 6 meses ---
    meses_labels = []
    meses_valores = []
    nombres_meses = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    for i in range(5, -1, -1):
        # Calcular mes
        mes_fecha = hoy.replace(day=1)
        for _ in range(i):
            mes_fecha = (mes_fecha - timedelta(days=1)).replace(day=1)
        mes_num = mes_fecha.month
        anio_num = mes_fecha.year
        total_mes = 0
        for v in todas_ventas:
            fecha_mx = v.fecha_venta.replace(tzinfo=pytz.utc).astimezone(tz_mexico).date()
            if fecha_mx.month == mes_num and fecha_mx.year == anio_num:
                total_mes += float(v.total)
        meses_labels.append(f"{nombres_meses[mes_num-1]} {anio_num}")
        meses_valores.append(round(total_mes, 2))

    # --- GRÁFICA 3: Top bebidas (dona) ---
    top_bebidas_raw = db.session.query(
        Bebida.nombre,
        func.sum(DetallePedido.cantidad).label('total_vendido')
    ).join(DetallePedido, Bebida.id == DetallePedido.bebida_id)\
    .group_by(Bebida.id)\
    .order_by(func.sum(DetallePedido.cantidad).desc())\
    .limit(5).all()

    top_bebidas = top_bebidas_raw
    dona_labels = [b.nombre for b in top_bebidas_raw]
    dona_valores = [int(b.total_vendido) for b in top_bebidas_raw]

    # --- Comparativa semanal ---
    ventas_esta_semana = sum(
        float(v.total) for v in todas_ventas
        if v.fecha_venta.replace(tzinfo=pytz.utc).astimezone(tz_mexico).date() >= inicio_semana
    )
    ventas_semana_anterior = sum(
        float(v.total) for v in todas_ventas
        if inicio_semana_anterior <= v.fecha_venta.replace(tzinfo=pytz.utc).astimezone(tz_mexico).date() < inicio_semana
    )
    if ventas_semana_anterior > 0:
        variacion = ((ventas_esta_semana - ventas_semana_anterior) / ventas_semana_anterior) * 100
    else:
        variacion = 0

    # --- Pedidos recientes ---
    pedidos_recientes = Pedido.query.order_by(Pedido.fecha_pedido.desc()).limit(6).all()

    # --- Alertas ---
    alertas = AlertaInventario.query.filter(
        AlertaInventario.activa == True,
        AlertaInventario.tipo_alerta.in_(['stock_bajo_materia', 'materia_agotada'])
    ).order_by(AlertaInventario.fecha_alerta.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
        # KPIs
        total_bebidas=total_bebidas,
        bebidas_disponibles=bebidas_disponibles,
        total_materias=total_materias,
        materias_ok=materias_ok,
        total_ventas_hoy=total_ventas_hoy,
        transacciones_hoy=transacciones_hoy,
        total_ventas_mes=total_ventas_mes,
        pedidos_pendientes_count=pedidos_pendientes_count,
        producciones_completadas=producciones_completadas,
        producciones_activas=producciones_activas,
        # Gráficas
        dias_labels=dias_labels,
        dias_valores=dias_valores,
        meses_labels=meses_labels,
        meses_valores=meses_valores,
        dona_labels=dona_labels,
        dona_valores=dona_valores,
        # Secciones
        top_bebidas=top_bebidas,
        pedidos_recientes=pedidos_recientes,
        alertas=alertas,
        ventas_esta_semana=ventas_esta_semana,
        ventas_semana_anterior=ventas_semana_anterior,
        variacion=variacion,
        tz_mexico=tz_mexico,
    )