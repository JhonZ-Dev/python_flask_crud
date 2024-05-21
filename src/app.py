from flask import Flask, jsonify
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
        #print(datos)
        productos = []
        for fila in datos:
            producto={'id_producto':fila[0],'nombreproducto':fila[1], 'precioproducto':fila[2], 'detalleproducto':fila[3],
                      'ivaproducto':fila[4], 'preciototal':fila[5], 'fechaactualizacion':fila[6], 'fechacreacion':fila[7],
                      'urlImagen':fila[8], 'sistema':fila[9]}
            productos.append(producto)
        return jsonify({'productos': productos, 'mensaje': "Productos Listados"})
    except Exception as es:
        return jsonify({'mensaje': "Error"})    



#mensaje para cuando se accede a la página correcta
def pagina_no_encontrada(error):
    return "<h1> Página No existe</h1>"


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()