from flask import render_template, redirect, url_for, request, flash, jsonify, session
from . import ventas_bp
from app.auth.routes import admin_required
from app.models import Venta, Pedido
from app import db
from datetime import date, datetime, timedelta

@ventas_bp.route('/')
@admin_required
def index():
    ventas = Venta.query.order_by(Venta.fecha_venta.desc()).all()
    
    #Pedidos entregados sin venta
    pedidos_sin_venta = Pedido.query.filter_by(estado='entregado').filter(
        ~Pedido.id.in_([v.pedido_id for v in ventas])
    ).all()
    
    #Ventas por dia 
    hoy = date.today()
    ventas_hoy = Venta.query.filter(
        Venta.fecha_venta >= hoy,
        Venta.estado_pago == 'pagado'
    ).all()
    total_hoy = sum(v.total for v in ventas_hoy)
    
    #Grafica de ventas semanales
    
    hoy_dt  = datetime.now()
    inicio_semana = hoy_dt - timedelta(days=hoy_dt.weekday())
    dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    
    datos_semana = []
    
    for i in range(7):
        dia = inicio_semana + timedelta(days=i)
        total_dia = sum(
            float(v.total) for v in ventas
            if v.fecha_venta.date() == dia.date() and v.estado_pago == 'pagado'
        )
        datos_semana.append({'dia':dias[i], 'total': total_dia})
        
    return render_template('admin/ventas.html', ventas=ventas, pedidos_sin_venta=pedidos_sin_venta,
        total_hoy=total_hoy,
        transacciones_hoy=len(ventas_hoy),
        datos_semana=datos_semana
    )

@ventas_bp.route('/nueva', methods=['POST'])
@admin_required
def nueva():
    try:
        pedido_id = int(request.form.get('pedido_id'))
        metodo_pago = request.form.get('metodo_pago')
        referencia = request.form.get('referencia_pago', '')
        
        pedido = Pedido.query.get(pedido_id)
        
        #Verificar que no halla ventas regitadas
        existe = Venta.query.filter_by(pedido_id=pedido_id).first()
        if existe:
            flash('Este pedido ya tiene una venta registrada.', 'warning')
            return redirect(url_for('admin_ventas.index'))
        
        venta = Venta(
            pedido_id=pedido_id, metodo_pago=metodo_pago, total=pedido.total,
            estado_pago='pagado', 
            referencia_pago = referencia if referencia else None
        )
        db.session.add(venta)
        
        #Si no esta el pedido a entregado, actualizar
        
        if pedido.estado != 'entregado':
            pedido.estado = 'entregado'
            
        db.session.commit()
        flash(f'Venta registrada exitosamente por ${pedido.total}.','success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        
    return redirect(url_for('admin_ventas.index'))

@ventas_bp.route('/cambiar_estado/<int:id>', methods=['POST'])
@admin_required
def cambiar_estado(id):
    venta = Venta.query.get_or_404(id)
    nuevo_estado = request.form.get('estado_pagado')
    if nuevo_estado in ['pendiente','pagado', 'reembolsado']:
        venta.estado_pago = nuevo_estado
        db.session.commit()
        flash(f'Estado de venta #{id} actualizado.', 'success')
    return redirect(url_for('admin_ventas.index'))
    
    
