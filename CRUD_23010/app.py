# Importar
#  flask
# flask_cors
# flask_sqlalchemy
# flask_marshmallow

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# CREAR LA APP
app = Flask(__name__)

# PERMITIR EL ACCESO DEL FRONTEND A LA RUTAS DE LAS APP
CORS(app)

# CONFIGURACIÓN A LA BASE DE DATOS                    //USER:PASSWORD@LOCALHOST/NOMBRE DB
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/mascotas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 

# PERMITE MANIPULAR LA BASE DE DATOS DE LA APP
db = SQLAlchemy(app)
ma = Marshmallow(app)

# DEFINIR LA CLASE PRODUCTO (ESTRUCTURA DE LA TABLA DE UNA BASE DE DATOS)
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estado= db.Column(db.String(10))
    nombre = db.Column(db.String(100))
    telefono = db.Column(db.String(12))
    email = db.Column(db.String(25))
    barrio = db.Column(db.String(20))
    fecha = db.Column(db.String(20))
    imagen = db.Column(db.String(400))

    def __init__(self, estado, nombre, telefono, email, barrio, fecha, imagen):
        self.estado = estado
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.barrio = barrio
        self.fecha = fecha
        self.imagen = imagen


# CÓDIGO QUE CREARÁ TODAS LAS TABLAS
with app.app_context():
    db.create_all()


# CLASE QUE PERMITIRÁ ACCEDER A LOS MÉTODOS DE CONVERSIÓN DE DATOS -  7
class ProductoSchema(ma.Schema):
    class Meta:
        fields = ("id", "estado", "nombre", "telefono", "email", "barrio", "fecha", "imagen")


# CREAR DOS OBJETOS
producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

# RUTAS 
# '/productos' ENDPOINT PARA RECIBIR DATOS: POST
# '/productos' ENDPOINT PARA MOSTRAR TODOS LOS PRODUCTOS DISPONIBLES EN LA BASE DE DATOS: GET
# '/productos/<id>' ENDPOINT PARA MOSTRAR UN PRODUCTO POR ID: GET
# '/productos/<id>' ENDPOINT PARA BORRAR UN PRODUCTO POR ID: DELETE
# '/productos/<id>' ENDPOINT PARA MODIFICAR UN PRODUCTO POR ID: PUT


# ENDPOINT/RUTA
@app.route("/productos", methods=['GET'])
def get_productos(): 
    # CONSULTAR TODA LA INFO EN LA TABLA PRODUCTO
    all_productos = Producto.query.all()
    
    return productos_schema.jsonify(all_productos)


# RUTA CREAR UN NUEVO REGISTRO EN LA TABLA
@app.route("/productos", methods=['POST'])
def create_producto(): 
    """"
    EJEMPLO:
    ENTRADA DE DATOS
    {
        "estado": "encontrado",
        "nombre": "Carlos",
        "telefono": "11-3445-4556",
        "email": "polo@codoacodo.com.ar",
        "barrio": "villa del parque",
        "fecha": "10-10-2020 15:00:00",
        "imagen": "https://picsum.photos/200/300?grayscale",
    }

    """
    # RECIBEN LOS DATOS
    estado= request.json['estado']
    nombre = request.json['nombre']
    telefono =request.json['telefono'] 
    email =request.json['email'] 
    barrio =request.json['barrio'] 
    fecha =request.json['fecha'] 
    imagen = request.json['imagen']

    # INSERTAR EN DB
    new_producto = Producto(estado, nombre, telefono, email, barrio, fecha, imagen)
    db.session.add(new_producto)
    db.session.commit()

    return producto_schema.jsonify(new_producto)

    
# MOSTRAR PRODUCTO POR ID
@app.route('/productos/<id>',methods=['GET'])
def get_producto(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    producto=Producto.query.get(id)

   # Retorna el JSON de un producto recibido como parámetro
   # Para ello, usar el objeto producto_schema para que convierta con                   # jsonify los datos recién ingresados que son objetos a JSON  
    return producto_schema.jsonify(producto)   


# BORRAR
@app.route('/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    producto=Producto.query.get(id)
    
    # A partir de db y la sesión establecida con la base de datos borrar 
    # el producto.
    # Se guardan lo cambios con commit
    db.session.delete(producto)
    db.session.commit()

# MODIFICAR
@app.route('/productos/<id>' ,methods=['PUT'])
def update_producto(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    producto=Producto.query.get(id)
 
    #  Recibir los datos a modificar
    estado = request.json['estado']
    nombre = request.json['nombre']
    telefono =request.json['telefono'] 
    email =request.json['email'] 
    barrio =request.json['barrio'] 
    fecha =request.json['fecha'] 
    imagen = request.json['imagen']

    # Del objeto resultante de la consulta modificar los valores  
    producto.estado= estado
    producto.nombre= nombre
    producto.telefono= telefono
    producto.email= email
    producto.barrio= barrio
    producto.fecha= fecha
    producto.imagen=imagen
    #  Guardar los cambios
    db.session.commit()
   # Para ello, usar el objeto producto_schema para que convierta con                     # jsonify el dato recién eliminado que son objetos a JSON  
    return producto_schema.jsonify(producto)


# BLOQUE PRINCIPAL
if __name__== "__main__":
    app.run(debug=True)