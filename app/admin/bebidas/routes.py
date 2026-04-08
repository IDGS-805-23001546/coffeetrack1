from flask import render_template, redirect, url_for, request, flash, jsonify
from . import bebidas_bp
from sqlalchemy import func as sa_func
from app.auth.routes import admin_required
from app.models import Bebida, CategoriaBebida, MateriaPrima, Receta, DetallePedido
from app import db

@bebidas_bp.route('/')
@admin_required
def index():
    bebidas = Bebida.query.filter_by(activo=True).all()
    categorias = CategoriaBebida.query.all()
    materias = MateriaPrima.query.filter_by(activo=True).all()
    
    vendidas = dict(db.session.query(
        DetallePedido.bebida_id,
        sa_func.sum(DetallePedido.cantidad)
    ).group_by(DetallePedido.bebida_id).all())
    
    return render_template('admin/bebidas.html',
        bebidas=bebidas,
        categorias=categorias,
        materias=materias,
        vendidas=vendidas
    )

@bebidas_bp.route('/nueva', methods=['POST'])
@admin_required
def nueva():
    try:
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        categoria_id = int(request.form.get('categoria_id'))
        volumen_ml = int(request.form.get('volumen_ml'))
        precio = float(request.form.get('precio'))
        imagen_url = request.form.get('imagen_url')
        disponible = True if request.form.get('disponible') == 'on' else False
        stock_actual = int(request.form.get('stock_actual', 0))
        stock_minimo = int(request.form.get('stock_minimo', 5))

        bebida = Bebida(
            nombre=nombre,
            descripcion=descripcion,
            categoria_id=categoria_id,
            volumen_ml=volumen_ml,
            precio=precio,
            imagen_url=imagen_url,
            disponible=disponible,
            stock_actual=stock_actual,
            stock_minimo=stock_minimo
        )
        db.session.add(bebida)
        db.session.flush()

        materia_ids = request.form.getlist('materia_prima_id[]')
        cantidades = request.form.getlist('cantidad[]')
        unidades = request.form.getlist('unidad_medida[]')

        for i in range(len(materia_ids)):
            if materia_ids[i] and cantidades[i]:
                receta = Receta(
                    nombre=nombre,
                    bebida_id=bebida.id,
                    materia_prima_id=int(materia_ids[i]),
                    cantidad=float(cantidades[i]),
                    unidad_medida=unidades[i]
                )
                db.session.add(receta)

        db.session.commit()
        flash('Bebida creada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear bebida: {str(e)}', 'danger')

    return redirect(url_for('admin_bebidas.index'))

@bebidas_bp.route('/toggle/<int:id>', methods=['POST'])
@admin_required
def toggle(id):
    bebida = Bebida.query.get_or_404(id)
    bebida.disponible = not bebida.disponible
    db.session.commit()
    return jsonify({'disponible': bebida.disponible})