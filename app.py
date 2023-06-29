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
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@127.0.0.1:3306/inmuebles'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 
#//root:root@localhost
# PERMITE MANIPULAR LA BASE DE DATOS DE LA APP
db = SQLAlchemy(app)
ma = Marshmallow(app)

# DEFINIR LA CLASE PRODUCTO (ESTRUCTURA DE LA TABLA DE UNA BASE DE DATOS)
class Inmueble(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    direccion = db.Column(db.String(100))
    tipo = db.Column(db.String(20))
    superficie_m2 = db.Column(db.Integer)
    valor=db.Column(db.Integer)
    imagen = db.Column(db.String(400))

    def __init__(self,direccion,tipo,superficie_m2,valor,imagen):
        self.direccion = direccion
        self.tipo = tipo
        self.superficie_m2 = superficie_m2
        self.valor = valor
        self.imagen = imagen



# CÓDIGO QUE CREARÁ TODAS LAS TABLAS
with app.app_context():
    db.create_all()


# CLASE QUE PERMITIRÁ ACCEDER A LOS MÉTODOS DE CONVERSIÓN DE DATOS -  7
class InmuebleSchema(ma.Schema):
    class Meta:
        fields = ("id", "direccion", "tipo", "superficie_m2", "valor", "imagen")


# CREAR DOS OBJETOS
inmueble_schema = InmuebleSchema()
inmuebles_schema = InmuebleSchema(many=True)

# RUTAS 
# '/productos' ENDPOINT PARA RECIBIR DATOS: POST
# '/productos' ENDPOINT PARA MOSTRAR TODOS LOS PRODUCTOS DISPONIBLES EN LA BASE DE DATOS: GET
# '/productos/<id>' ENDPOINT PARA MOSTRAR UN PRODUCTO POR ID: GET
# '/productos/<id>' ENDPOINT PARA BORRAR UN PRODUCTO POR ID: DELETE
# '/productos/<id>' ENDPOINT PARA MODIFICAR UN PRODUCTO POR ID: PUT

# ENDPOINT/RUTA
@app.route("/inmuebles", methods=['GET'])
def get_inmuebles(): 
    # CONSULTAR TODA LA INFO EN LA TABLA PRODUCTO
    all_inmuebles = Inmueble.query.all()
    
    return inmuebles_schema.jsonify(all_inmuebles)


# RUTA CREAR UN NUEVO REGISTRO EN LA TABLA
@app.route("/inmuebles", methods=['POST'])
def create_inmueble(): 
    """"
    EJEMPLO:
    ENTRADA DE DATOS
    {
        "nombre": "MICROONDAS",
        "precio": 50000,
        "stock": 10,
        "imagen": "https://picsum.photos/200/300?grayscale",
    }

    """
    # RECIBEN LOS DATOS
    direccion = request.json['direccion']
    tipo =request.json['tipo'] 
    superficie_m2 =request.json['superficie_m2'] 
    valor = request.json['valor']
    imagen = request.json['imagen']

   

    # INSERTAR EN DB
    new_inmueble = Inmueble(direccion, tipo, superficie_m2, valor, imagen)
    db.session.add(new_inmueble)
    db.session.commit()

    return inmueble_schema.jsonify(new_inmueble)

    
# MOSTRAR PRODUCTO POR ID
@app.route('/inmuebles/<id>',methods=['GET'])
def get_inmueble(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    inmueble=Inmueble.query.get(id)

   # Retorna el JSON de un producto recibido como parámetro
   # Para ello, usar el objeto producto_schema para que convierta con                   # jsonify los datos recién ingresados que son objetos a JSON  
    return inmueble_schema.jsonify(inmueble)   


# BORRAR
@app.route('/inmuebles/<id>',methods=['DELETE'])
def delete_inmueble(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    inmueble=Inmueble.query.get(id)
    
    # A partir de db y la sesión establecida con la base de datos borrar 
    # el producto.
    # Se guardan lo cambios con commit
    db.session.delete(inmueble)
    db.session.commit()

# MODIFICAR
@app.route('/inmuebles/<id>',methods=['PUT'])
def update_inmueble(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    inmueble=Inmueble.query.get(id)
 
    #  Recibir los datos a modificar

    direccion = request.json['direccion']
    tipo =request.json['tipo'] 
    superficie_m2 =request.json['superficie_m2'] 
    valor = request.json['valor']
    imagen = request.json['imagen']

    # Del objeto resultante de la consulta modificar los valores  
    inmueble.direccion=direccion
    inmueble.tipo=tipo
    inmueble.superficie_m2=superficie_m2
    inmueble.valor=valor
    inmueble.imagen=imagen
    #  Guardar los cambios
    db.session.commit()
   # Para ello, usar el objeto producto_schema para que convierta con                     # jsonify el dato recién eliminado que son objetos a JSON  
    return inmueble_schema.jsonify(inmueble)


# BLOQUE PRINCIPAL
if __name__== "__main__":
    app.run(debug=True)