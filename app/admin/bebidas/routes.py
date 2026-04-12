from flask import render_template, redirect, url_for, request, flash, jsonify, current_app
from . import bebidas_bp
from app.auth.routes import admin_required
from app.models import Bebida, CategoriaBebida, MateriaPrima, Receta, DetallePedido
from app import db
from sqlalchemy import func as sa_func
import os
import uuid
from werkzeug.utils import secure_filename


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def guardar_imagen(file):
    if file and file.filename and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        return filename
    return None


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

    # Calcular capacidad de producción
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
            capacidades[b.id] = 0

    return render_template('admin/bebidas.html',
        bebidas=bebidas,
        categorias=categorias,
        materias=materias,
        vendidas=vendidas,
        capacidades=capacidades
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
        disponible = True if request.form.get('disponible') == 'on' else False
        stock_actual = int(request.form.get('stock_actual', 0))
        stock_minimo = int(request.form.get('stock_minimo', 5))

        # Manejar imagen caliente
        imagen_url = None
        if 'imagen' in request.files:
            filename = guardar_imagen(request.files['imagen'])
            if filename:
                imagen_url = filename

        # Manejar imagen fría
        imagen_url_frio = None
        if 'imagen_frio' in request.files:
            filename_frio = guardar_imagen(request.files['imagen_frio'])
            if filename_frio:
                imagen_url_frio = filename_frio

        # Crear bebida con ambas imágenes
        bebida = Bebida(
            nombre=nombre,
            descripcion=descripcion,
            categoria_id=categoria_id,
            volumen_ml=volumen_ml,
            precio=precio,
            imagen_url=imagen_url,
            imagen_url_frio=imagen_url_frio,
            disponible=disponible,
            stock_actual=stock_actual,
            stock_minimo=stock_minimo
        )
        db.session.add(bebida)
        db.session.flush()

        # Guardar ingredientes de la receta
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


@bebidas_bp.route('/editar_imagen/<int:id>', methods=['POST'])
@admin_required
def editar_imagen(id):
    bebida = Bebida.query.get_or_404(id)
    try:
        if 'imagen' in request.files:
            filename = guardar_imagen(request.files['imagen'])
            if filename:
                if bebida.imagen_url:
                    old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], bebida.imagen_url)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                bebida.imagen_url = filename
                db.session.commit()
                flash('Imagen actualizada correctamente.', 'success')
            else:
                flash('Formato de imagen no válido. Usa PNG, JPG o WEBP.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('admin_bebidas.index'))


@bebidas_bp.route('/editar_imagen_frio/<int:id>', methods=['POST'])
@admin_required
def editar_imagen_frio(id):
    bebida = Bebida.query.get_or_404(id)
    try:
        if 'imagen' in request.files:
            filename = guardar_imagen(request.files['imagen'])
            if filename:
                if bebida.imagen_url_frio:
                    old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], bebida.imagen_url_frio)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                bebida.imagen_url_frio = filename
                db.session.commit()
                flash('Imagen fría actualizada correctamente.', 'success')
            else:
                flash('Formato no válido. Usa PNG, JPG o WEBP.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('admin_bebidas.index'))


@bebidas_bp.route('/toggle/<int:id>', methods=['POST'])
@admin_required
def toggle(id):
    bebida = Bebida.query.get_or_404(id)
    bebida.disponible = not bebida.disponible
    db.session.commit()
    return jsonify({'disponible': bebida.disponible})