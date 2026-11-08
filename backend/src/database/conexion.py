from flask_mysqldb import MySQL
from config import Config

mysql = MySQL()

def conectar_db(app):
    app.config['MYSQL_HOST'] = Config.MYSQL_HOST
    app.config['MYSQL_USER'] = Config.MYSQL_USER
    app.config['MYSQL_PASSWORD'] = Config.MYSQL_PASSWORD
    app.config['MYSQL_DB'] = Config.MYSQL_DB
    app.config['MYSQL_PORT'] = Config.MYSQL_PORT

    mysql.init_app(app)