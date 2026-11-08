
from flask import Blueprint, jsonify, request
from database.conexion import mysql

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/', methods=['GET'])
def listar_pedidos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM pedidos")
    datos = cursor.fetchall()
    cursor.close()

    return jsonify(datos)


@pedidos_bp.route('/', methods=['POST'])
def registrar_pedido():

    datos = request.json

    cursor = mysql.connection.cursor()

    cursor.execute(
        "INSERT INTO pedidos (nombre, direccion, telefono, fecha, total) VALUES (%s, %s, %s, %s, %s)",
        (datos['nombre'], datos['direccion'], datos['telefono'], datos['fecha'], datos['total'])
    )

    mysql.connection.commit()

    id_pedido = cursor.lastrowid

    cursor.close()

    return jsonify({
        'mensaje': 'Pedido registrado correctamente',
        'id': id_pedido
    }), 201
