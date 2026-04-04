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

    total_bebidas = Bebida.query.filter_by(activo=True).count()
    bebidas_disponibles = Bebida.query.filter_by(disponible=True, activo=True).count()
    total_materias = MateriaPrima.query.filter_by(activo=True).count()
    materias_ok = MateriaPrima.query.filter(
        MateriaPrima.stock_actual > MateriaPrima.stock_minimo,
        MateriaPrima.activo == True
    ).count()

    ventas_hoy = Venta.query.filter(
        Venta.fecha_venta >= hoy,
        Venta.estado_pago == 'pagado'
    ).all()
    total_ventas_hoy = sum(float(v.total) for v in ventas_hoy)

    producciones = Produccion.query.filter_by(estado='completada').count()
    producciones_completadas = Produccion.query.filter_by(estado='completada').count()

    pedidos_recientes = Pedido.query.order_by(Pedido.fecha_pedido.desc()).limit(5).all()
    alertas = AlertaInventario.query.filter_by(activa=True).order_by(
        AlertaInventario.fecha_alerta.desc()
    ).limit(5).all()

    # Top 3 bebidas mas vendidas
    top_bebidas = db.session.query(
        Bebida.nombre,
        func.sum(DetallePedido.cantidad).label('total_vendido')
    ).join(DetallePedido, Bebida.id == DetallePedido.bebida_id)\
     .group_by(Bebida.id)\
     .order_by(func.sum(DetallePedido.cantidad).desc())\
     .limit(3).all()

    # Comparativa semana actual vs anterior
    ventas_esta_semana = sum(
        float(v.total) for v in Venta.query.filter(
            Venta.fecha_venta >= inicio_semana,
            Venta.estado_pago == 'pagado'
        ).all()
    )
    ventas_semana_anterior = sum(
        float(v.total) for v in Venta.query.filter(
            Venta.fecha_venta >= inicio_semana_anterior,
            Venta.fecha_venta < inicio_semana,
            Venta.estado_pago == 'pagado'
        ).all()
    )

    if ventas_semana_anterior > 0:
        variacion = ((ventas_esta_semana - ventas_semana_anterior) / ventas_semana_anterior) * 100
    else:
        variacion = 0

    return render_template('admin/dashboard.html',
        total_bebidas=total_bebidas,
        bebidas_disponibles=bebidas_disponibles,
        total_materias=total_materias,
        materias_ok=materias_ok,
        total_ventas_hoy=total_ventas_hoy,
        transacciones_hoy=len(ventas_hoy),
        producciones=producciones,
        producciones_completadas=producciones_completadas,
        pedidos_recientes=pedidos_recientes,
        alertas=alertas,
        top_bebidas=top_bebidas,
        ventas_esta_semana=ventas_esta_semana,
        ventas_semana_anterior=ventas_semana_anterior,
        variacion=variacion
    )