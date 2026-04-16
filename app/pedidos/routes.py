from flask import render_template, redirect, url_for, flash, session, request, jsonify
from . import pedidos_bp
from app.models import Pedido, DetallePedido, Bebida, Usuario
from app import db
from app.auth.routes import login_required
from decimal import Decimal
from datetime import datetime, date, timedelta, timezone
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


def calcular_entrega(tipo_entrega):
    """Calcula hora estimada y día de entrega según horario de la cafetería"""
    ahora = datetime.now()
    dia_semana = ahora.weekday()  # 0=lunes, 6=domingo
    hora_actual = ahora.hour * 60 + ahora.minute

    APERTURA = 7 * 60           # 7:00 AM
    CIERRE_SEMANA = 22 * 60     # 10:00 PM lunes-viernes
    CIERRE_FIN = 19 * 60        # 7:00 PM sábado-domingo
    ULTIMO_ENVIO_SEMANA = 21 * 60  # 9:00 PM lunes-viernes
    ULTIMO_ENVIO_FIN = 18 * 60     # 6:00 PM sábado-domingo
    TIEMPO_PREP = 25            # minutos de preparación

    es_fin_semana = dia_semana >= 5
    cierre = CIERRE_FIN if es_fin_semana else CIERRE_SEMANA
    ultimo_envio = ULTIMO_ENVIO_FIN if es_fin_semana else ULTIMO_ENVIO_SEMANA

    limite = ultimo_envio if tipo_entrega == 'domicilio' else (cierre - TIEMPO_PREP)
    hora_lista = hora_actual + TIEMPO_PREP

    if hora_actual < APERTURA:
        dia = ahora.date()
        entrega_min = APERTURA + TIEMPO_PREP
    elif hora_lista <= limite:
        dia = ahora.date()
        entrega_min = hora_lista
    else:
        siguiente = ahora + timedelta(days=1)
        # Si es domicilio saltar fines de semana si ya no hay servicio
        while tipo_entrega == 'domicilio' and siguiente.weekday() >= 5:
            siguiente += timedelta(days=1)
        dia = siguiente.date()
        entrega_min = APERTURA + TIEMPO_PREP

    horas = entrega_min // 60
    minutos = entrega_min % 60
    hora_str = f"{horas:02d}:{minutos:02d}"
    return hora_str, dia


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

    # Costo de envío
    costo_envio = Decimal('30.00') if tipo_entrega == 'domicilio' else Decimal('0.00')
    total = subtotal + costo_envio

    if tipo_entrega == 'sucursal':
        direccion = 'Recoger en sucursal'

    # Calcular horario estimado
    hora_estimada, dia_entrega = calcular_entrega(tipo_entrega)

    pedido = Pedido(
        usuario_id=session['user_id'],
        subtotal=subtotal,
        total=total,
        costo_envio=costo_envio,
        direccion_entrega=direccion,
        telefono_contacto=telefono[:15],
        notas=request.form.get('notas', ''),
        estado='pendiente',
        hora_estimada_entrega=hora_estimada,
        dia_entrega=dia_entrega
    )
    db.session.add(pedido)
    db.session.flush()

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
            'temperatura': d.temperatura,
            'precio_unitario': str(d.precio_unitario),
            'subtotal': str(d.subtotal)
        } for d in pedido.detalles.all()]
    })


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
        ref=ref,
        now=datetime.now
    )


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

    estilo_titulo = ParagraphStyle(
        'titulo', parent=styles['Title'],
        fontSize=22, textColor=colors.HexColor('#e8891a'), spaceAfter=4
    )
    estilo_subtitulo = ParagraphStyle(
        'subtitulo', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor('#888888'), spaceAfter=2
    )
    estilo_bold = ParagraphStyle(
        'bold', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor('#1a1a1a'), fontName='Helvetica-Bold'
    )

    elementos.append(Paragraph('CoffeeTrack', estilo_titulo))
    elementos.append(Paragraph('Gestión de Café Bebible — León, Gto.', estilo_subtitulo))
    elementos.append(Spacer(1, 0.2*inch))

    elementos.append(Table(
        [['']],
        colWidths=[6.5*inch],
        style=TableStyle([('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor('#e8891a'))])
    ))
    elementos.append(Spacer(1, 0.2*inch))

    ref = ''
    if pedido.notas and 'REF:' in pedido.notas:
        ref = pedido.notas.split('REF:')[-1].strip()

    # Hora en zona horaria México
    fecha_pedido = pedido.fecha_pedido
    if fecha_pedido.tzinfo is None:
        fecha_pedido = fecha_pedido.replace(tzinfo=timezone.utc)
    fecha_mx = fecha_pedido.astimezone(timezone(timedelta(hours=-6)))
    fecha_str = fecha_mx.strftime('%d/%m/%Y %H:%M')

    # Entrega estimada
    entrega_str = ''
    if pedido.hora_estimada_entrega and pedido.dia_entrega:
        hoy = date.today()
        if pedido.dia_entrega == hoy:
            entrega_str = f'Hoy a las {pedido.hora_estimada_entrega}'
        else:
            dias_es = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
            dia_nombre = dias_es[pedido.dia_entrega.weekday()]
            entrega_str = f'{dia_nombre} {pedido.dia_entrega.strftime("%d/%m")} a las {pedido.hora_estimada_entrega}'

    info_data = [
        ['Ticket de Compra', ''],
        ['Pedido #', f'{pedido.id}'],
        ['Referencia:', ref or 'N/A'],
        ['Fecha:', fecha_str],
        ['Cliente:', f'{usuario.nombre} {usuario.apellidos}'],
        ['Teléfono:', pedido.telefono_contacto],
        ['Entrega:', pedido.direccion_entrega],
        ['Hora estimada:', entrega_str or '—'],
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

    elementos.append(Paragraph('Detalle del Pedido', estilo_bold))
    elementos.append(Spacer(1, 0.1*inch))

    detalle_data = [['Bebida', 'Temp.', 'Cantidad', 'Precio Unit.', 'Subtotal']]
    for d in pedido.detalles.all():
        temp = ' Frío' if d.temperatura == 'frio' else ' Caliente'
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

    # Totales con costo de envío
    costo_envio = float(pedido.costo_envio or 0)
    total_data = [
        ['', '', 'Subtotal:', f'${float(pedido.subtotal):.2f}'],
    ]
    if costo_envio > 0:
        total_data.append(['', '', 'Envío a domicilio:', f'${ costo_envio:.2f}'])
    total_data.append(['', '', 'TOTAL:', f'${float(pedido.total):.2f}'])

    tabla_total = Table(total_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1*inch])
    ultima_fila = len(total_data) - 1
    tabla_total.setStyle(TableStyle([
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('FONTNAME', (3,ultima_fila), (3,ultima_fila), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('TEXTCOLOR', (2,0), (2,-1), colors.HexColor('#888888')),
        ('TEXTCOLOR', (3,ultima_fila), (3,ultima_fila), colors.HexColor('#e8891a')),
        ('FONTSIZE', (3,ultima_fila), (3,ultima_fila), 13),
        ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEABOVE', (2,ultima_fila), (-1,ultima_fila), 1, colors.HexColor('#e8891a')),
    ]))
    elementos.append(tabla_total)
    elementos.append(Spacer(1, 0.4*inch))

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