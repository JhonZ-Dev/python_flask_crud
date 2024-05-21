from flask import Flask
from config import config
from flask_mysqldb import MySQL

app = Flask(__name__)
#conexion base de datos
conexion = MySQL(app)
@app.route('/')
def index():
    return "Bienvenido"


#método para listar
@app.route('/product')
def listar_productos():
    try:
        cursor= conexion.connection.cursor()
        sql = "SELECT * FROM product"
        cursor.execute(sql)
        datos = cursor.fetchall()
        print(datos)
        return "Listados"


    except Exception as es:
        return "Error"    



#mensaje para cuando se accede a la página correcta
def pagina_no_encontrada(error):
    return "<h1> Página No existe</h1>"


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()