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

@app.route('/api/register', methods=['POST'])
def registrar_producto():
    try:
        # Obtener los datos del producto desde el request JSON
        data = request.get_json()
        id_producto = data['id_producto']
        nombreproducto = data['nombreproducto']
        precioproducto = data['precioproducto']
        detalleproducto = data['detalleproducto']
        ivaproducto = data['ivaproducto']
        preciototal = data['preciototal']
        fechaactualizacion = data['fechaactualizacion']
        fechacreacion = data['fechacreacion']
        urlImagen = data['urlImagen']
        sistema = data['sistema']

        cursor = conexion.connection.cursor()
        sql = """INSERT INTO product (id_producto, nombreproducto, precioproducto, detalleproducto, ivaproducto, preciototal, fechaactualizacion, fechacreacion, urlImagen, sistema)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (id_producto, nombreproducto, precioproducto, detalleproducto, ivaproducto, preciototal, fechaactualizacion, fechacreacion, urlImagen, sistema))
        conexion.connection.commit()

        return jsonify({"mensaje": "Producto Registrado"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'mensaje': "Error al registrar producto"}), 500

    finally:
        cursor.close()

#metodo para editar
@app.route('/api/update/<int:id_producto>', methods=['PUT'])
def actualizar_producto(id_producto):
    try:
        # Obtener los datos del producto desde el request JSON
        data = request.get_json()
        nombreproducto = data['nombreproducto']
        precioproducto = data['precioproducto']
        detalleproducto = data['detalleproducto']
        ivaproducto = data['ivaproducto']
        preciototal = data['preciototal']
        fechaactualizacion = data['fechaactualizacion']
        urlImagen = data['urlImagen']
        sistema = data['sistema']

        cursor = conexion.connection.cursor()
        sql = """UPDATE product SET 
                 nombreproducto = %s,
                 precioproducto = %s,
                 detalleproducto = %s,
                 ivaproducto = %s,
                 preciototal = %s,
                 fechaactualizacion = %s,
                 urlImagen = %s,
                 sistema = %s
                 WHERE id_producto = %s"""
        cursor.execute(sql, (nombreproducto, precioproducto, detalleproducto, ivaproducto, preciototal, fechaactualizacion, urlImagen, sistema, id_producto))
        conexion.connection.commit()

        return jsonify({"mensaje": "Producto Actualizado"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'mensaje': "Error al actualizar producto"}), 500

    finally:
        cursor.close()

#mensaje para cuando se accede a la página correcta
def pagina_no_encontrada(error):
    return "<h1> Página No existe</h1>"


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()