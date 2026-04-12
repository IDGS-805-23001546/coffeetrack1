from flask import Blueprint, render_template, redirect, url_for, flash, session, request, jsonify
from app.models import Bebida, CategoriaBebida, Pedido, DetallePedido, MateriaPrima, Venta
from app.auth.routes import login_required
from app import db
from decimal import Decimal
from . import cliente_bp


@cliente_bp.route('/')
def inicio():
    bebidas_destacadas = Bebida.query.filter_by(activo=True, disponible=True).limit(6).all()
    return render_template('cliente/inicio.html', bebidas=bebidas_destacadas)


@cliente_bp.route('/menu')
def menu():
    categorias = CategoriaBebida.query.all()
    bebidas = Bebida.query.filter_by(activo=True, disponible=True).all()

    # Calcular capacidad de producción por bebida
    capacidades = {}
    for b in bebidas:
        recetas = b.recetas.all()
        if recetas:
            caps = []
            for r in recetas:
                mp = r.materia_prima
                if mp and float(r.cantidad) > 0:
                    caps.append(int(float(mp.stock_actual) // float(r.cantidad)))
            capacidades[b.id] = min(caps) if caps else 0
        else:
            capacidades[b.id] = 999  # sin receta = sin límite

    return render_template('cliente/menu.html',
        bebidas=bebidas,
        categorias=categorias,
        capacidades=capacidades
    )


@cliente_bp.route('/nosotros')
def about():
    return render_template('cliente/about.html')


@cliente_bp.route('/carrito')
@login_required
def carrito():
    cart = session.get('cart', {})
    items = []
    total = Decimal('0')
    for bebida_id, cantidad in cart.items():
        bebida = Bebida.query.get(int(bebida_id))
        if bebida:
            subtotal = bebida.precio * cantidad
            total += subtotal
            items.append({
                'bebida': bebida,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
    return render_template('cliente/carrito.html', items=items, total=total)


@cliente_bp.route('/mis-pedidos')
@login_required
def mis_pedidos():
    pedidos = Pedido.query.filter_by(usuario_id=session['user_id']).order_by(
        Pedido.fecha_pedido.desc()
    ).all()
    return render_template('cliente/mis_pedidos.html', pedidos=pedidos)