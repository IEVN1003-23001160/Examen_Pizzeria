
from flask import Blueprint, jsonify, request
from database.conexion import mysql

ventas_bp = Blueprint('ventas', __name__)


# CONSULTAR TODOS LOS DETALLES DE VENTA
@ventas_bp.route('/', methods=['GET'])
def listar_ventas():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM detalle_pedido")

    datos = cursor.fetchall()

    cursor.close()

    return jsonify(datos)


# REGISTRAR EL DETALLE DE UNA VENTA
@ventas_bp.route('/', methods=['POST'])
def registrar_venta():

    datos = request.json

    cursor = mysql.connection.cursor()

    cursor.execute(
        "INSERT INTO detalle_pedido (pedido_id, tamano, ingredientes, num_pizzas, subtotal) VALUES (%s, %s, %s, %s, %s)",
        (datos['pedido_id'], datos['tamano'], datos['ingredientes'], datos['cantidad'], datos['subtotal'])
    )

    mysql.connection.commit()

    cursor.close()

    return jsonify({
        'mensaje': 'Detalle de venta registrado correctamente'
    }), 201


# CONSULTAR VENTAS POR DIA DE LA SEMANA
@ventas_bp.route('/dia/<dia>', methods=['GET'])
def consultar_ventas_dia(dia):

    dias = {
        'domingo': 1,
        'lunes': 2,
        'martes': 3,
        'miercoles': 4,
        'miércoles': 4,
        'jueves': 5,
        'viernes': 6,
        'sabado': 7,
        'sábado': 7
    }

    dia = dia.lower().strip()

    if dia not in dias:
        return jsonify({
            'mensaje': 'Dia no valido'
        }), 400

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT id, nombre, direccion, telefono,
        DATE_FORMAT(fecha, '%%Y-%%m-%%d'), total
        FROM pedidos
        WHERE DAYOFWEEK(fecha) = %s
        ORDER BY fecha DESC
        """,
        (dias[dia],)
    )

    datos = cursor.fetchall()

    cursor.close()

    ventas = []

    for fila in datos:
        ventas.append({
            'id': fila[0],
            'nombre': fila[1],
            'direccion': fila[2],
            'telefono': fila[3],
            'fecha': fila[4],
            'total': float(fila[5] or 0)
        })

    total_dia = sum(venta['total'] for venta in ventas)

    return jsonify({
        'dia': dia,
        'ventas': ventas,
        'total_acumulado': total_dia
    })


# CONSULTAR VENTAS POR MES
@ventas_bp.route('/mes/<mes>', methods=['GET'])
def consultar_ventas_mes(mes):

    meses = {
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'octubre': 10,
        'noviembre': 11,
        'diciembre': 12
    }

    mes = mes.lower().strip()

    if mes not in meses:
        return jsonify({
            'mensaje': 'Mes no valido'
        }), 400

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT id, nombre, direccion, telefono,
        DATE_FORMAT(fecha, '%%Y-%%m-%%d'), total
        FROM pedidos
        WHERE MONTH(fecha) = %s
        ORDER BY fecha DESC
        """,
        (meses[mes],)
    )

    datos = cursor.fetchall()

    cursor.close()

    ventas = []

    for fila in datos:
        ventas.append({
            'id': fila[0],
            'nombre': fila[1],
            'direccion': fila[2],
            'telefono': fila[3],
            'fecha': fila[4],
            'total': float(fila[5] or 0)
        })

    total_mes = sum(venta['total'] for venta in ventas)

    return jsonify({
        'mes': mes,
        'ventas': ventas,
        'total_acumulado': total_mes
    })


# CONSULTAR EL DETALLE DE UNA VENTA ESPECIFICA
@ventas_bp.route('/detalle/<int:pedido_id>', methods=['GET'])
def consultar_detalle_venta(pedido_id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT
            p.id,
            p.nombre,
            p.direccion,
            p.telefono,
            DATE_FORMAT(p.fecha, '%%Y-%%m-%%d'),
            p.total,
            d.id,
            d.tamano,
            d.ingredientes,
            d.num_pizzas,
            d.subtotal
        FROM pedidos p
        LEFT JOIN detalle_pedido d ON p.id = d.pedido_id
        WHERE p.id = %s
        """,
        (pedido_id,)
    )

    datos = cursor.fetchall()

    cursor.close()

    if not datos:
        return jsonify({
            'mensaje': 'No se encontro el pedido'
        }), 404

    pedido = {
        'id': datos[0][0],
        'nombre': datos[0][1],
        'direccion': datos[0][2],
        'telefono': datos[0][3],
        'fecha': datos[0][4],
        'total': float(datos[0][5] or 0),
        'pizzas': []
    }

    for fila in datos:

        if fila[6] is not None:

            pedido['pizzas'].append({
                'id': fila[6],
                'tamano': fila[7],
                'ingredientes': fila[8],
                'cantidad': fila[9],
                'subtotal': float(fila[10] or 0)
            })

    return jsonify(pedido)
