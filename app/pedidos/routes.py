from flask import render_template, redirect, url_for, flash, session, request, jsonify
from . import pedidos_bp
from app.models import Pedido, DetallePedido, Bebida, Usuario
from app import db
from app.auth.routes import login_required
from decimal import Decimal
from datetime import datetime
from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io

def generar_referencia(pedido_id):
    fecha = datetime.now().strftime('%Y%m%d')
    return f'CT-{fecha}-{str(pedido_id).zfill(3)}'

@pedidos_bp.route('/crear', methods=['POST'])
@login_required
def crear():
    cart = session.get('cart', {})
    if not cart:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('cliente.menu'))

    usuario = Usuario.query.get(session['user_id'])

    subtotal = Decimal('0')
    detalles = []
    for bebida_id, datos in cart.items():
        bebida = Bebida.query.get(int(bebida_id))
    if bebida and bebida.disponible:
        if isinstance(datos, dict):
            cantidad = datos['cantidad']
            temperatura = datos.get('temperatura', 'caliente')
        else:
            cantidad = datos
            temperatura = 'caliente'
        item_subtotal = bebida.precio * cantidad
        subtotal += Decimal(str(item_subtotal))
        detalles.append({
            'bebida_id': bebida.id,
            'cantidad': cantidad,
            'temperatura': temperatura,
            'precio_unitario': bebida.precio,
            'subtotal': item_subtotal
        })

    if not detalles:
        flash('No hay bebidas disponibles en tu carrito.', 'warning')
        return redirect(url_for('carrito.ver_carrito'))

    tipo_entrega = request.form.get('tipo_entrega', 'sucursal')
    telefono = request.form.get('telefono') or usuario.telefono or 'N/A'
    direccion = request.form.get('direccion') or usuario.direccion or 'Recoger en sucursal'

    if tipo_entrega == 'sucursal':
        direccion = 'Recoger en sucursal'

    pedido = Pedido(
        usuario_id=session['user_id'],
        subtotal=subtotal,
        total=subtotal,
        direccion_entrega=direccion,
        telefono_contacto=telefono[:15],
        notas=request.form.get('notas', ''),
        estado='pendiente'
    )
    db.session.add(pedido)
    db.session.flush()

    # Generar referencia automatica
    pedido.notas = (pedido.notas or '') + f' | REF: {generar_referencia(pedido.id)}'

    for d in detalles:
        detalle = DetallePedido(
        pedido_id=pedido.id,
        bebida_id=d['bebida_id'],
        cantidad=d['cantidad'],
        temperatura=d['temperatura'],
        precio_unitario=d['precio_unitario'],
        subtotal=d['subtotal']
    )
    db.session.add(detalle)

    db.session.commit()
    session.pop('cart', None)
    return redirect(url_for('pedidos.confirmacion', id=pedido.id))


@pedidos_bp.route('/mis-pedidos')
@login_required
def mis_pedidos():
    pedidos = Pedido.query.filter_by(
        usuario_id=session['user_id']
    ).order_by(Pedido.fecha_pedido.desc()).all()
    return render_template('cliente/mis_pedidos.html', pedidos=pedidos)


@pedidos_bp.route('/detalle/<int:id>')
@login_required
def detalle(id):
    pedido = Pedido.query.get_or_404(id)
    if pedido.usuario_id != session['user_id']:
        return jsonify({'error': 'No autorizado'}), 403
    return jsonify({
        'id': pedido.id,
        'total': str(pedido.total),
        'estado': pedido.estado,
        'direccion': pedido.direccion_entrega,
        'telefono': pedido.telefono_contacto,
        'notas': pedido.notas,
        'fecha': pedido.fecha_pedido.strftime('%d/%m/%Y %H:%M'),
        'detalles': [{
            'bebida': d.bebida.nombre,
            'cantidad': d.cantidad,
            'precio_unitario': str(d.precio_unitario),
            'subtotal': str(d.subtotal)
        } for d in pedido.detalles.all()]
    })
    
@pedidos_bp.route('/ticket/<int:id>')
@login_required
def ticket(id):
    pedido = Pedido.query.get_or_404(id)
    if pedido.usuario_id != session['user_id']:
        flash('No autorizado.', 'danger')
        return redirect(url_for('pedidos.mis_pedidos'))

    usuario = Usuario.query.get(pedido.usuario_id)
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50, leftMargin=50,
        topMargin=50, bottomMargin=50
    )

    styles = getSampleStyleSheet()
    elementos = []

    # Estilo titulo
    estilo_titulo = ParagraphStyle(
        'titulo',
        parent=styles['Title'],
        fontSize=22,
        textColor=colors.HexColor('#e8891a'),
        spaceAfter=4
    )
    estilo_subtitulo = ParagraphStyle(
        'subtitulo',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#888888'),
        spaceAfter=2
    )
    estilo_normal = ParagraphStyle(
        'normal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333'),
        spaceAfter=4
    )
    estilo_bold = ParagraphStyle(
        'bold',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#1a1a1a'),
        fontName='Helvetica-Bold'
    )

    # Encabezado
    elementos.append(Paragraph('CoffeeTrack', estilo_titulo))
    elementos.append(Paragraph('Gestión de Café Bebible — León, Gto.', estilo_subtitulo))
    elementos.append(Spacer(1, 0.2*inch))

    # Linea separadora
    elementos.append(Table(
        [['']],
        colWidths=[6.5*inch],
        style=TableStyle([('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor('#e8891a'))])
    ))
    elementos.append(Spacer(1, 0.2*inch))

    # Info del pedido
    # Extraer referencia de notas
    ref = ''
    if pedido.notas and 'REF:' in pedido.notas:
        ref = pedido.notas.split('REF:')[-1].strip()

    info_data = [
        ['Ticket de Compra', ''],
        [f'Pedido #', f'{pedido.id}'],
        ['Referencia:', ref or 'N/A'],
        ['Fecha:', pedido.fecha_pedido.strftime('%d/%m/%Y %H:%M')],
        ['Cliente:', f'{usuario.nombre} {usuario.apellidos}'],
        ['Teléfono:', pedido.telefono_contacto],
        ['Entrega:', pedido.direccion_entrega],
        ['Estado:', pedido.estado.upper()],
    ]

    tabla_info = Table(info_data, colWidths=[2*inch, 4.5*inch])
    tabla_info.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#888888')),
        ('TEXTCOLOR', (1,0), (1,-1), colors.HexColor('#1a1a1a')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor('#fdf8f3'), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    elementos.append(tabla_info)
    elementos.append(Spacer(1, 0.3*inch))

    # Detalle de productos
    elementos.append(Paragraph('Detalle del Pedido', estilo_bold))
    elementos.append(Spacer(1, 0.1*inch))

    detalle_data = [['Bebida', 'Temp.', 'Cantidad', 'Precio Unit.', 'Subtotal']]
    for d in pedido.detalles.all():
        temp = '🧊 Frío' if d.temperatura == 'frio' else '☕ Caliente'
        detalle_data.append([
        d.bebida.nombre,
        temp,
        str(d.cantidad),
        f'${float(d.precio_unitario):.2f}',
        f'${float(d.subtotal):.2f}'
    ])

    tabla_detalle = Table(detalle_data, colWidths=[2.5*inch, 1*inch, 0.8*inch, 1.2*inch, 1*inch])
    tabla_detalle.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8891a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#fdf8f3'), colors.white]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e0d8d0')),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    elementos.append(tabla_detalle)
    elementos.append(Spacer(1, 0.2*inch))

    # Total
    total_data = [
        ['', '', 'Subtotal:', f'${float(pedido.subtotal):.2f}'],
        ['', '', 'Descuento:', f'-${float(pedido.descuento):.2f}'],
        ['', '', 'TOTAL:', f'${float(pedido.total):.2f}'],
    ]
    tabla_total = Table(total_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1*inch])
    tabla_total.setStyle(TableStyle([
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('FONTNAME', (3,2), (3,2), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('TEXTCOLOR', (2,0), (2,-1), colors.HexColor('#888888')),
        ('TEXTCOLOR', (3,2), (3,2), colors.HexColor('#e8891a')),
        ('FONTSIZE', (3,2), (3,2), 13),
        ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEABOVE', (2,2), (-1,2), 1, colors.HexColor('#e8891a')),
    ]))
    elementos.append(tabla_total)
    elementos.append(Spacer(1, 0.4*inch))

    # Pie de pagina
    elementos.append(Table(
        [['']],
        colWidths=[6.5*inch],
        style=TableStyle([('LINEABOVE', (0,0), (-1,-1), 0.5, colors.HexColor('#e0d8d0'))])
    ))
    elementos.append(Spacer(1, 0.1*inch))
    elementos.append(Paragraph('Gracias por tu compra. CoffeeTrack — León, Gto. 2026', estilo_subtitulo))

    doc.build(elementos)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'ticket_pedido_{pedido.id}.pdf',
        mimetype='application/pdf'
    )
    
    #ruta para detalle del pedido y generar tiket
@pedidos_bp.route('/confirmacion/<int:id>')
@login_required
def confirmacion(id):
    pedido = Pedido.query.get_or_404(id)
    if pedido.usuario_id != session['user_id']:
        return redirect(url_for('pedidos.mis_pedidos'))
    
    ref = ''
    if pedido.notas and 'REF:' in pedido.notas:
        ref = pedido.notas.split('REF:')[-1].strip()
    
    return render_template('cliente/confirmacion_pedido.html', 
        pedido=pedido, 
        ref=ref
    )