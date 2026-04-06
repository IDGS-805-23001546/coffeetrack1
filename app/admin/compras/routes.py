from flask import render_template, redirect, url_for, request, flash, session
from . import compras_bp
from app.auth.routes import admin_required
from datetime import date
from app.models import CompraMateriaPrima, Proveedor, MateriaPrima, DetalleCompraMateriaPrima
from app import db

@compras_bp.route('/')
@admin_required
def index():
    compras = CompraMateriaPrima.query.order_by(CompraMateriaPrima.fecha_compra.desc()).all()
    proveedores = Proveedor.query.filter_by(activo=True).all()
    materias_primas = MateriaPrima.query.filter_by(activo=True).all()
    return render_template('admin/compras.html',
        compras=compras,
        proveedores=proveedores,
        materias_primas=materias_primas
    )

@compras_bp.route('/add', methods=['POST'])
@admin_required
def add():
    try:
        proveedor_id = request.form.get('proveedor_id')
        fecha_compra = request.form.get('fecha_compra') or date.today()
        estado = request.form.get('estado')
        notas = request.form.get('notas')

        materias_ids = request.form.getlist('materia_prima_id[]')
        cantidades = request.form.getlist('cantidad[]')
        precios = request.form.getlist('precio_unitario[]')

        total = sum(float(c) * float(p) for c, p in zip(cantidades, precios))

        nueva_compra = CompraMateriaPrima(
            proveedor_id=proveedor_id,
            fecha_compra=fecha_compra,
            total=total,
            estado=estado,
            notas=notas,
            usuario_registro_id=session.get('user_id')
        )
        db.session.add(nueva_compra)
        db.session.flush()

        for materia_id, cantidad, precio in zip(materias_ids, cantidades, precios):
            detalle = DetalleCompraMateriaPrima(
                compras_id=nueva_compra.id,
                materia_prima_id=materia_id,
                cantidad=float(cantidad),
                precio_unitario=float(precio),
                subtotal=float(cantidad) * float(precio)
            )
            db.session.add(detalle)

        db.session.commit()
        flash('Compra registrada correctamente.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al registrar la compra: {str(e)}', 'danger')

    return redirect(url_for('admin_compras.index'))


@compras_bp.route('/edit/<int:id>', methods=['POST'])
@admin_required
def edit(id):
    try:
        compra = CompraMateriaPrima.query.get_or_404(id)
        compra.estado = request.form.get('estado')
        db.session.commit()
        flash('Estado actualizado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar: {str(e)}', 'danger')
    return redirect(url_for('admin_compras.index'))