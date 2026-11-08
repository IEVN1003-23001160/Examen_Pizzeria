from flask import Flask
from database.conexion import conectar_db
from blueprint.pedidos.routes import pedidos_bp
from blueprint.ventas.routes import ventas_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

conectar_db(app)

app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
app.register_blueprint(ventas_bp, url_prefix='/ventas')

@app.route('/')
def inicio():
    return "API de Pizzeria funcionando correctamente"

if __name__ == '__main__':
    app.run(debug=True)