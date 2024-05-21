from flask import Flask, jsonify, request
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

#producto por id
@app.route('/product/<id_producto>', methods=['GET'])
def product_by_id(id_producto):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM product WHERE id_producto = '{0}' ".format(id_producto)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            producto={'id_producto':datos[0],'nombreproducto':datos[1], 'precioproducto':datos[2], 'detalleproducto':datos[3],
                      'ivaproducto':datos[4], 'preciototal':datos[5], 'fechaactualizacion':datos[6], 'fechacreacion':datos[7],
                      'urlImagen':datos[8], 'sistema':datos[9]}
            return jsonify({'productos': producto, 'mensaje': "Producto Encontrado"})
        else:
            return jsonify({'mensaje': "Producto no encontrado - verifique el id"})

    except Exception as es:
        return jsonify({'mensaje': "Error"})    

#registrar product
@app.route('/api/register', methods=['POST'])
def registrar_producto():
    try:
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO product (id_producto,nombreproducto,precioproducto, detalleproducto,ivaproducto, preciototal,fechaactualizacion,fechacreacion,urlImagen,sistema)
                 VALUES({0},'{1}',{2},'{3}',{4},{5},'{6}','{7}','{8}','{9}')""".format(request.json['id_producto'],request.json['nombreproducto'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({"mensaje":"Producto Registrador"})

    except Exception as es:
        print(es)
        return jsonify({'mensaje': "Error"}) 


#mensaje para cuando se accede a la página correcta
def pagina_no_encontrada(error):
    return "<h1> Página No existe</h1>"


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()