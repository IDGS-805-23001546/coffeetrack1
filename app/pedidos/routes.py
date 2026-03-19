from flask import render_template, redirect, url_for, flash, session, request
from . import pedidos_bp
from app.models import Pedido, DetallePedido, Bebida
from app import db
from app.auth.routes import login_required
from decimal import Decimal

@pedidos_bp.route('/crear', methods=['POST'])
@login_required
def crear():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('cliente.menu'))

    
    db.session.commit()
    session.pop('cart', None) 
    
    flash('¡Pedido realizado con éxito!', 'success')
    return redirect(url_for('pedidos.mis_pedidos'))

@pedidos_bp.route('/mis-pedidos')
@login_required
def mis_pedidos():
    pedidos = Pedido.query.filter_by(usuario_id=session['user_id']).all()
    return render_template('cliente/mis_pedidos.html', pedidos=pedidos)