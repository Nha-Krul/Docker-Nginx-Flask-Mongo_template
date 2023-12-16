import os
from flask import Flask, redirect, jsonify, url_for
from flask_pymongo import PyMongo, ObjectId
from flask_login import LoginManager, logout_user
import logging as logging
from logging.handlers import RotatingFileHandler
from libraries.utils import User
from pymongo import IndexModel, ASCENDING

version = "Proyecto v1.0.0"

#Inicio de la aplicación
application = Flask(__name__, template_folder='./services/websrc/templates')

#Pongo una key para que encripte las cookies
application.config['SECRET_KEY'] = os.environ["SECRET_KEY"]


#--------------------------------------Logging--------------------------------------------------------------------
# Configuración del módulo de registro
log_file = './log/frontend.log'
# Configuración del manejador para el archivo
file_handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=5)
file_handler.setLevel(logging.INFO)

# Configuración del manejador para la consola
application.logger.addHandler(file_handler)

application.logger.setLevel(logging.DEBUG)

application.logger.debug(f"Inicio del servidor - {version}")
#-------------------------------------/Logging/-----------------------------------------------------------------------

#-------------------------------------Base de Datos-------------------------------------------------------------------
#Vinculación con el servidor de Mongo y la Base de datos
application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGO_INITDB_ROOT_USERNAME'] + ':' + os.environ['MONGO_INITDB_ROOT_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' #+ os.environ['MONGO_INITDB_ROOT_DATABASE']

#Conexión con el servidor de Mongo
mongo = PyMongo(application)
#Manejador de Mongo
db = mongo.db 
#Cambio a la base de datos del proyecto
db = mongo.cx[os.environ['MONGO_INITDB_ROOT_DATABASE']]

# Crear un índice único en el campo 'email' de la colección 'users'
index_users = IndexModel([('email', ASCENDING)], unique=True)
db['users'].create_indexes([index_users])
#--------------------------------------/Base de Datos/--------------------------------------------------------------

#------------------------------------------Routes-------------------------------------------------------------------
#Importo las librerías con las rutas (No las puedo importar hasta no tener la base de datos conectada)
from services.views import views #Importo la librería de rutas genéricas
application.register_blueprint(views, url_prefix='/')  #Agrego las rutas de la librería al servidor en base al root

from services.auth import auth #Importa la libreria de inicio de sesión
application.register_blueprint(auth, url_prefix='/') #Agrego las rutas de la librería en base al root

from services.userViews import userViews
application.register_blueprint(userViews, url_prefix='/')

#-----------------------------------------/Routes/--------------------------------------------------------------------

#-----------------------------------------Login por Cookies-----------------------------------------------------------
#Manejador de los usuarios en Flask
login_manager = LoginManager() #Asigno el motor encargado de los inicio de seción
login_manager.login_view = 'auth.login' #Asigno la vista de inicio al motor de login
login_manager.init_app(application) #Asigno el motor a la aplicación

#Compruebo si la cookie del usuario corresponde a un usuario en la base de datos, estos datos son devueltos al current_user
@login_manager.user_loader
def load_user(id):
    application.logger.debug(f"app.load_user - {id}")
    usuario = db["users"].find_one({'_id': ObjectId(id)}) #Busco al usuario por ID almacenado en la cookie
    application.logger.debug(f"app.load_user Usuario encontrado -> {usuario}")
    if usuario :
        return User(usuario) #Devuelvo el usuario en formato que usa el Manager  
    return None

#Si el usuario no está autorizado lo paso a la pantalla de Login
@login_manager.unauthorized_handler
def unauthorized():
    application.logger.error(f"app.unauthorized_handler -> No autorizado!")
    return redirect(url_for('auth.login')) 
#-----------------------------------------/Login por Cookies/------------------------------------------------------------    
   


#-----------------------------------------------Otros--------------------------------------------------------------------
#Definición en caso de que no se corra por Docker
if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 8080)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
