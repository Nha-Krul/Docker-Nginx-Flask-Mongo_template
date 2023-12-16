
#TODO - Verificar que no se pueda solicitar borrar el mismo usuario que está conectado
#TODO - Verificar que no se deje sacar el modificador is_admin con el mismo usuario que está conectado
#TODO - Verificar que no se pueda desactivar el mismo usuario que se encuentra conectado
#TODO - Verificar comando HTML de Activación y de Borrado   -|__ Verificar cómo funciona la actualización de la base con Flask-pymongo 
#TODO - Verificar funcionamiento de edición                 -|

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, send_from_directory, send_file, get_flashed_messages
from flask_login import login_required, current_user
from flask_pymongo import ObjectId
from werkzeug.security import generate_password_hash
from services.auth import logout
from app import db, application
from libraries.utils import checkEmail
import json

userViews = Blueprint('userViews', __name__)

#Mostrar usuarios [administrador]
@userViews.route('/users', methods=['GET', 'DELETE'])
@login_required
def usersList():
    get_flashed_messages()
    if not current_user.is_admin: #Si no es un usuario administrador no puede ver la tabla de usuarios, lo devuelvo a la página principal
        return redirect(url_for('views.mainPage'))
    else:
        if request.method == 'GET':
            usuarios = db['users'].find()
            
            return render_template("usersTable.html", this_user=current_user, usuarios=usuarios)
        
        elif request.method == 'DELETE':
            id = json.loads(request.data)
            usuario = db['users'].find_one({'_id':ObjectId(id)})
            if usuario: #Verifico que no sea el usuario administrador del sistema, lo puedo editar, pero no borrar
                if usuario['email'] == 'admin@admin.com':
                    flash(f'No se puede eliminar el usuario administrador', category='error')
                    application.logger.error(f"userViews.usuarios -> {current_user['email']} Intentó borrar el usuario administrador")
                    #return render_template("usuarios.html", this_user=current_user) 
                else:
                    usuario = db['users'].find_one_and_delete({'_id':ObjectId(id)})
                    flash(f"Usuario {usuario['email']} borrado del sistama", category='success')
            
            usuarios = db['users'].find()
            return render_template("usersTable.html", this_user=current_user, usuarios=usuarios)
                    

@userViews.route('/users/adduser', methods=['GET', 'POST'])
@login_required
def adduser():
    if request.method == 'GET':
        return render_template('usersAdd.html', this_user=current_user, nombre="", email="", password1="", password2="", edit=False)
    
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        isAdmin = request.form.get('isAdmin') #Los checkbox aparecen como "" si estan marcados 
        if isAdmin=="":
                isAdmin = True
        else:
            isAdmin = False

        usuario = db['users'].find_one({'email': email})
        if usuario:
            application.logger.warning(f"{current_user.email} intentó registar el usuario con email:{email} que ya existe en la base de datos")
            flash('Ya existe un usuario registrado a ese email.', category='error')
        elif not checkEmail(email):
            flash('El email ingresado no tiene el formato correcto', category='error')
        elif len(nombre) < 5:
            flash('El nombre ingresado es muy corto.', category='error')
        elif len(password1) < 7:
            flash('La contraseña debe ser mayor a 7 caracteres.', category='error')
        elif password1 != password2:
            flash('Las contraseñas no coinciden.', category='error')
        else:
            try:
                hash = generate_password_hash(password1)
                userID = db['users'].insert_one({'fullname':nombre, 'password':hash, 'email':email, 'is_active':True, 'is_admin':isAdmin})
                application.logger.info(f"{current_user.email} registro el nuevo usuario con email: {email}")
                flash('Nuevo usuario creado!', category='success')
                return redirect(url_for('userViews.usersList'))
            except Exception as e:
                application.logger.error(f"{current_user.email} intentó registrar el usuario con email: {email} y ocurrió el siguiente error:\n{e.args}")
                flash('Error al crear el nuevo usuario.', category='error')
                return redirect(url_for('userViews.usuarios'))
        return render_template("usersAdd.html", this_user=current_user, nombre=nombre, email=email, password1=password1, password2=password2, isAdmin=isAdmin, edit=False)
    
''' Actualización de contraseña y o flag administrador'''    
@userViews.route('/users/pwuser/<id>', methods=['GET','POST'])
@login_required
def editUser(id):
    if request.method == 'GET': #Devuelvo la página de edición
        usuario = db['users'].find_one({'_id':ObjectId(id)}) #Busco al usuario en la base de datos
        if usuario: 
            application.logger.info(f"{current_user.email} solicitó la edición del usuario {usuario['email']}")
            return render_template('usersAdd.html', this_user=current_user, id=str(usuario['_id']), nombre=usuario['fullname'], email=usuario['email'], isAdmin=usuario['is_admin'], edit=True)
        else:
            application.logger.info(f"{current_user.email} solicitó la edición del usuario con id: {id}, pero este no se encontró en la base de datos")
            return redirect(url_for('userViews.usersList'))
    
    #Actualización del usuario
    elif request.method == 'POST':
        usuario = db['users'].find_one({'_id':ObjectId(id)}) #Busco el usuario a editar
        if not usuario:
            application.logger.warning(f'{current_user.email} envió nueva información para el usuario con id_ {id}, pero este no existe en la base de datos')
            flash('No existe el usuario que se quiere editar.', category='error')
            return redirect(url_for('userViews.usersList'))

        #Tomo los datos del formulario
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        isAdmin = request.form.get('isAdmin') #Los checkbox aparecen como "" si estan marcados 
        
        #Verifico que no se quira editar el flag de Administrador del usuario admin@admin.com
        if usuario['email'] == 'admin@admin.com': #No permito que se modifiquen los atributos del usuario administrador
            isAdmin = True
        elif current_user.get_id() == id: #Si el usuario a editar es el mismo que está conectado no le dejó cambiar el estado del flag administrador
            isAdmin = usuario['is_admin']
        else:
            if isAdmin=="": #El checkbox envía "" cuando está marcado
                isAdmin = True
            else:
                isAdmin = False
       
        
        #Verificar si no hay password => no se edita
        if len(password1) > 0:
            if len(password1) < 7:
                flash('La contraseña debe ser mayor a 7 caracteres.', category='error')
            elif password1 != password2:
                flash('Las contraseñas no coinciden.', category='error')
            else:
                hash= generate_password_hash(password1)
                response = db['users'].update_one({'_id':ObjectId(id)},{"$set":{'password':hash, 'is_admin':isAdmin}}) 
                if response.modified_count > 0:
                    application.logger.debug(f"{current_user.email} a modificado al usuario {usuario['email']}") 
                    flash('Usuario editado!', category='success')
                else:
                    application.logger.warning(f"{current_user.email} intentó modificar al usuario {usuario['email']} pero ocurrió un error")
                    flash('Error al intentar cambiar los datos del usuario')
                    
                if id == current_user.get_id(): #Si cambió el password del propio usuario entonces lo saco del login manager
                    application.logger.debug(f"{current_user.nombre} modificó su contraseña")
                    logout()
                    return redirect(url_for('views.home'))
                return redirect(url_for('userViews.usersList'))  

        else:
            response = db['users'].update_one({'_id':ObjectId(id)},{"$set":{'is_admin':isAdmin}}) 
            if response.modified_count > 0:
                application.logger.info(f"{current_user.nombre} modificó el tipo de usuario de {usuario['email']}") 
                flash('Usuario editado!', category='success')
            else:
                application.logger.warning(f"{current_user.nombre} intentó modificar el tipo de usuario de {usuario['email']} pero ocurrió un error")
                flash('Error al intentar cambiar los datos del usuario')
            return redirect(url_for('userViews.usersList'))
        return render_template("addUser.html", this_user=current_user, nombre=usuario['fullname'], email=usuario['email'], password1=password1, password2=password2, isAdmin=isAdmin, id=str(usuario['_id']), edit=True )

''' Edición del flag de usuario activo '''
@userViews.route('/users/eduser', methods=['POST'])
@login_required
def edUser():
    if request.method == 'POST':
        id = json.loads(request.data)
        usuario = db['users'].find_one({'_id':ObjectId(id)}) #Busco el usuario a editar
        if not usuario['email'] == "admin@admin.com": #Verifico que no se esté queriendo desactivar al usuario administrador
            if not current_user.get_id() == str(usuario['_id']): #Verifico si el usuario se está queriendo desactivar a si mismo 
                if usuario['is_active'] == True:
                    inUse = False
                else:
                    inUse = True
                response = db['users'].update_one({'_id':ObjectId(id)},{"$set":{'is_active':inUse}}) 
                if response.modified_count > 0: 
                    flash('Usuario editado!', category='success')
                else:
                    flash('Error al intentar cambiar los datos del usuario')
            else:
                application.logger.warning(f"{current_user.nombre} intentó desactivar su propio usuario")
                flash('No puede desactivar el usuario con el que ingresó al sistema')
        else:
            flash('No se puede deshabilitar el usuario Administrador', category='error')

    return redirect(url_for('userViews.usersList'))


