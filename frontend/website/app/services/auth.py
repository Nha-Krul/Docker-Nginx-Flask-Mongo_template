from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import check_password_hash
from app import db, application
from libraries.utils import User 
from datetime import timedelta

auth = Blueprint('auth', __name__)

#Defino que hacer en la url login
@auth.route('/login', methods=['GET', 'POST'])
def login():
       
    if request.method == 'GET':
        if current_user.is_authenticated and not current_user.is_anonymous:
           return redirect(url_for('views.mainPage'))
        return render_template("login.html", this_user=current_user) #Devuelvo al usuario a la pantalla de Login
    
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
                     
        usuario = db.users.find_one({'email':email}) #Busco el usuario por el mail
                
        if usuario:
            application.logger.debug(f"auth.login -> Usuario {email} encontrado")
            if check_password_hash(usuario['password'], password):
                if(usuario['is_active'] == True):
                    login_user(user=User(usuario), remember=True, duration=timedelta(weeks=1)) #Pongo al usuario como activo
                    application.logger.debug(f"auth.login -> Usuario {usuario} autenticado")
                    return redirect(url_for('views.mainPage'))
                else:
                    application.logger.error(f"auth.login -> Usuario {email} es correcto pero no está activo")
                    flash('Su usuario se encuentra bloqueado en el sistema, comuniquese con el administrador', category='error')
            else:
                application.logger.error(f"auth.login -> Usuario {email} password incorrecto")
                flash('Usuario o contraseña incorrectos', category='error') 
        else:
            application.logger.error(f"auth.login -> Usuario {email} no encontrado")
            flash('Usuario o contraseña incorrectos', category='error')

    return render_template("login.html", this_user=current_user)    #Devuelvo al usuario a la pantalla de ingreso


@auth.route('/logout')
@login_required
def logout():
    application.logger.debug(f"{current_user.email} se desconectó del servidor")
    logout_user() #Saco al usuario del manejador
    flash('Gracias por haber usado esta aplicación', category='success')
    return redirect(url_for('auth.login'))