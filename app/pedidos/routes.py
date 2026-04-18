from flask import render_template, redirect, url_for, flash, session, request, jsonify
from . import pedidos_bp
from app.models import Pedido, DetallePedido, Bebida, Usuario
from app import db
from app.auth.routes import login_required
from decimal import Decimal
from datetime import datetime, date, timedelta, timezone
from flask import send_file
from reportlab.lib.pagesizes import letter, A5
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
import io


def generar_referencia(pedido_id):
    fecha = datetime.now().strftime('%Y%m%d')
    return f'CT-{fecha}-{str(pedido_id).zfill(3)}'


def calcular_entrega(tipo_entrega):
    ahora = datetime.now()
    dia_semana = ahora.weekday()
    hora_actual = ahora.hour * 60 + ahora.minute

    APERTURA = 7 * 60
    CIERRE_SEMANA = 22 * 60
    CIERRE_FIN = 19 * 60
    ULTIMO_ENVIO_SEMANA = 21 * 60
    ULTIMO_ENVIO_FIN = 18 * 60
    TIEMPO_PREP = 25

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

    # Nueva key formato: "bebida_id_temperatura"
    for key, datos in cart.items():
        bebida_id = int(key.split('_')[0])
        bebida = Bebida.query.get(bebida_id)
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
    metodo_pago = request.form.get('metodo_pago', 'efectivo')
    telefono = request.form.get('telefono') or usuario.telefono or 'N/A'
    direccion = request.form.get('direccion') or usuario.direccion or 'Recoger en sucursal'

    costo_envio = Decimal('30.00') if tipo_entrega == 'domicilio' else Decimal('0.00')
    total = subtotal + costo_envio

    if tipo_entrega == 'sucursal':
        direccion = 'Recoger en sucursal'

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
        dia_entrega=dia_entrega,
        metodo_pago_cliente=metodo_pago
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

    # Ticket en formato A5 — más parecido a un ticket real
    doc = SimpleDocTemplate(
        buffer,
        pagesize=(8.5*cm, 22*cm),  # Ancho ticket térmico
        rightMargin=0.5*cm,
        leftMargin=0.5*cm,
        topMargin=0.6*cm,
        bottomMargin=0.6*cm
    )

    styles = getSampleStyleSheet()

    # Estilos personalizados
    s_titulo = ParagraphStyle('titulo', parent=styles['Normal'],
        fontSize=16, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#e8891a'),
        alignment=TA_CENTER, spaceAfter=2)

    s_sub = ParagraphStyle('sub', parent=styles['Normal'],
        fontSize=7, textColor=colors.HexColor('#888888'),
        alignment=TA_CENTER, spaceAfter=1)

    s_ref = ParagraphStyle('ref', parent=styles['Normal'],
        fontSize=9, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1a1a1a'),
        alignment=TA_CENTER, spaceAfter=2)

    s_label = ParagraphStyle('label', parent=styles['Normal'],
        fontSize=7, textColor=colors.HexColor('#888888'),
        fontName='Helvetica-Bold', spaceAfter=0)

    s_valor = ParagraphStyle('valor', parent=styles['Normal'],
        fontSize=8, textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=3)

    s_total = ParagraphStyle('total', parent=styles['Normal'],
        fontSize=13, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#e8891a'),
        alignment=TA_RIGHT, spaceAfter=2)

    s_pie = ParagraphStyle('pie', parent=styles['Normal'],
        fontSize=7, textColor=colors.HexColor('#aaaaaa'),
        alignment=TA_CENTER, spaceAfter=1)

    ancho = 7.5*cm
    elementos = []

    # ── ENCABEZADO ─────────────────────────────────────────
    elementos.append(Paragraph('☕ CoffeeTrack', s_titulo))
    elementos.append(Paragraph('León, Guanajuato · 2026', s_sub))
    elementos.append(Spacer(1, 0.2*cm))
    elementos.append(HRFlowable(width=ancho, thickness=1.5,
        color=colors.HexColor('#e8891a'), spaceAfter=0.2*cm))

    # Referencia
    ref = ''
    if pedido.notas and 'REF:' in pedido.notas:
        ref = pedido.notas.split('REF:')[-1].strip()

    elementos.append(Paragraph(f'PEDIDO #{pedido.id}', s_ref))
    if ref:
        elementos.append(Paragraph(ref, s_sub))
    elementos.append(Spacer(1, 0.15*cm))

    # ── INFORMACIÓN DEL PEDIDO ─────────────────────────────
    elementos.append(HRFlowable(width=ancho, thickness=0.5,
        color=colors.HexColor('#e0d8d0'), spaceAfter=0.15*cm))

    # Fecha
    fecha_pedido = pedido.fecha_pedido
    if fecha_pedido.tzinfo is None:
        fecha_pedido = fecha_pedido.replace(tzinfo=timezone.utc)
    fecha_mx = fecha_pedido.astimezone(timezone(timedelta(hours=-6)))
    fecha_str = fecha_mx.strftime('%d/%m/%Y %H:%M')

    info = [
        ('FECHA', fecha_str),
        ('CLIENTE', f'{usuario.nombre} {usuario.apellidos}'),
        ('TELÉFONO', pedido.telefono_contacto),
        ('ENTREGA', pedido.direccion_entrega),
        ('PAGO', (pedido.metodo_pago_cliente or 'efectivo').upper()),
    ]

    if pedido.hora_estimada_entrega:
        hoy = date.today()
        if pedido.dia_entrega == hoy:
            entrega_str = f'Hoy a las {pedido.hora_estimada_entrega}'
        else:
            dias_es = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
            dia_nombre = dias_es[pedido.dia_entrega.weekday()]
            entrega_str = f'{dia_nombre} {pedido.dia_entrega.strftime("%d/%m")} {pedido.hora_estimada_entrega}'
        info.append(('HORA EST.', entrega_str))

    for label, valor in info:
        elementos.append(Paragraph(label, s_label))
        elementos.append(Paragraph(str(valor), s_valor))

    # ── PRODUCTOS ──────────────────────────────────────────
    elementos.append(HRFlowable(width=ancho, thickness=0.5,
        color=colors.HexColor('#e0d8d0'), spaceAfter=0.1*cm))
    elementos.append(Paragraph('PRODUCTOS', s_label))
    elementos.append(Spacer(1, 0.1*cm))

    # Tabla de productos
    prod_data = [['Bebida', 'Cant.', 'Precio', 'Total']]
    for d in pedido.detalles.all():
        temp = '🧊' if d.temperatura == 'frio' else '☕'
        prod_data.append([
            f'{temp} {d.bebida.nombre[:18]}',
            str(d.cantidad),
            f'${float(d.precio_unitario):.0f}',
            f'${float(d.subtotal):.0f}'
        ])

    tabla_prod = Table(prod_data, colWidths=[3.8*cm, 0.9*cm, 1.3*cm, 1.4*cm])
    tabla_prod.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8891a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        # Filas
        ('FONTSIZE', (0,1), (-1,-1), 7),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#fdf8f3'), colors.white]),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#e0d8d0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
    ]))
    elementos.append(tabla_prod)
    elementos.append(Spacer(1, 0.2*cm))

    # ── TOTALES ────────────────────────────────────────────
    elementos.append(HRFlowable(width=ancho, thickness=0.5,
        color=colors.HexColor('#e0d8d0'), spaceAfter=0.1*cm))

    costo_envio = float(pedido.costo_envio or 0)
    totales_data = [['Subtotal', f'${float(pedido.subtotal):.2f}']]
    if costo_envio > 0:
        totales_data.append(['Envío', f'${costo_envio:.2f}'])
    totales_data.append(['TOTAL', f'${float(pedido.total):.2f}'])

    tabla_totales = Table(totales_data, colWidths=[4.5*cm, 3*cm])
    ultima = len(totales_data) - 1
    tabla_totales.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('FONTNAME', (0,ultima), (-1,ultima), 'Helvetica-Bold'),
        ('FONTSIZE', (0,ultima), (-1,ultima), 11),
        ('TEXTCOLOR', (0,ultima), (-1,ultima), colors.HexColor('#e8891a')),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('LINEABOVE', (0,ultima), (-1,ultima), 1, colors.HexColor('#e8891a')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    elementos.append(tabla_totales)
    elementos.append(Spacer(1, 0.3*cm))

    # ── PIE ────────────────────────────────────────────────
    elementos.append(HRFlowable(width=ancho, thickness=1,
        color=colors.HexColor('#e8891a'), spaceAfter=0.15*cm))
    elementos.append(Paragraph('¡Gracias por tu compra!', s_ref))
    elementos.append(Paragraph('CoffeeTrack — León, Gto.', s_pie))
    elementos.append(Paragraph('coffeetrack.mx', s_pie))

    doc.build(elementos)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'ticket_CT_{pedido.id}.pdf',
        mimetype='application/pdf'
    )