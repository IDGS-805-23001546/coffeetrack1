from flask import render_template, session, redirect, url_for
from . import admin_bp
from app.auth.routes import admin_required
from app.models import Bebida, MateriaPrima, Pedido, Venta, AlertaInventario
from datetime import date

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # Tarjetas superiores
    total_bebidas = Bebida.query.filter_by(activo=True).count()
    bebidas_disponibles = Bebida.query.filter_by(disponible=True, activo=True).count()
    total_materias = MateriaPrima.query.filter_by(activo=True).count()
    materias_ok = MateriaPrima.query.filter(
        MateriaPrima.stock_actual > MateriaPrima.stock_minimo,
        MateriaPrima.activo == True
    ).count()

    # Ventas del día
    hoy = date.today()
    ventas_hoy = Venta.query.filter(
        Venta.fecha_venta >= hoy
    ).all()
    total_ventas_hoy = sum(v.total for v in ventas_hoy)

    # Producción activa
    from app.models import Produccion
    producciones = Produccion.query.filter_by(estado='completada').count()
    producciones_completadas = Produccion.query.filter_by(estado='completada').count()

    # Pedidos recientes
    pedidos_recientes = Pedido.query.order_by(
        Pedido.fecha_pedido.desc()
    ).limit(5).all()

    # Alertas activas
    alertas = AlertaInventario.query.filter_by(activa=True).order_by(
        AlertaInventario.fecha_alerta.desc()
    ).limit(5).all()

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
        alertas=alertas
    )