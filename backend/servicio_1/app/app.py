import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo



application = Flask(__name__)


#Conexión con el servidor de Mongo y la base de Datos
application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGO_INITDB_ROOT_USERNAME'] + ':' + os.environ['MONGO_INITDB_ROOT_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/'# + os.environ['MONGO_INITDB_ROOT_DATABASE']


mongo = PyMongo(application) #Relación de la base de datos con la aplicación Flask
db = mongo.db

db = mongo.cx[os.environ['MONGO_INITDB_ROOT_DATABASE']]

@application.route('/back_servicio_1', methods=['POST','GET']) #Ruta a procesar, unicamente POST
def createDato():
    if request.method == 'GET':
        return jsonify( #Si se escribió correctamente devuelvo un json con el mensaje y el estado
            status=True,
            message='Server is working!'
        ), 201
    
    data = request.get_json(force=True) #Convierte el json recibido en un diccionario
    item = {
        'servicio_1': data #servicio_1 sería el nombre del Data Collection, y los datos los correspondientes a la carga
    }
    
    try:
        
        #Creo la colección en caso de que no exista
        # Nombre de la colección que deseas trabajar
        collection_name = 'servicio_1'

    # Verificar si la colección ya existe
        if collection_name in db.list_collection_names():
        # Si la colección existe, seleccionarla
            collection = db[collection_name]
        else:
        # Si la colección no existe, crearla
            db.create_collection(collection_name)
            collection = db[collection_name]
        
        collection.insert_one(item) #Escribe el diccionario recibido en la colección indicada en item

        return jsonify( #Si se escribió correctamente devuelvo un json con el mensaje y el estado
            status=True,
            message='Data saved successfully!'
        ), 201
    except Exception as e:
        return jsonify( #Si ocurrió algún error en la escritura envío un mensaje con el error
            status=False,
            message=e.args
        ), 501
        

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 9090)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
        
