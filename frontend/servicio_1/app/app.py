import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo



application = Flask(__name__)

application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGO_INITDB_ROOT_USERNAME'] + ':' + os.environ['MONGO_INITDB_ROOT_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' #+ os.environ['MONGO_INITDB_ROOT_DATABASE']

mongo = PyMongo(application)
db = mongo.db

db = mongo.cx[os.environ['MONGO_INITDB_ROOT_DATABASE']]

#Ruta al root de la app - Devuelve un JSON con el mensaje por default
@application.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the Dockerized Flask MongoDB app!'
    )
    
@application.route('/front_servicio_1')
def front_servicio_1():
    
    collection_name = 'servicio_1'

    # Verificar si la colección ya existe
    if collection_name in db.list_collection_names():
        # Si la colección existe, seleccionarla
        collection = db[collection_name]
        datos = list(collection.find()) #Debo de tener el nombre de la colección generada por el backend
        #Primero tengo que convertir todos los _id de ObjectId a String
        for dato in datos:
            dato['_id']= str(dato['_id'])
        
        return jsonify({'status': 'OK', 'message': 'servicio_1', 'data': datos})
        
    else:
        # Si la colección no existe, crearla
        return jsonify({'message': f'La colección todavía no tiene datos.'})

    

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 8080)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
