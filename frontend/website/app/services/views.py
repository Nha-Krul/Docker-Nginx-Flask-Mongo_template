#Librería que tiene rutas genéricas para cargar la página web

from flask import Blueprint, request, redirect, url_for, send_file, render_template
from flask_login import login_required, current_user, logout_user
import os
from app import application

views = Blueprint('views', __name__)

#Rutas genericas
@views.route('/favicon.ico')
def favicon():
    return send_file('services/websrc/img/favicon.ico')

@views.route('/img/<file>')
def image(file):
    if file == 'logo.png':
        return send_file(f"services/websrc/img/{os.environ['COMPANY_LOGO']}")
    else:
        if current_user.is_authenticated: #TODO - Ver a que cambio esta definición
            return send_file(f'services/websrc/img/{file}')
        else:
            return 'Unauthorized', 401

#Rutas especiales
#Pagina de home
@views.route('/')
def home():
    try:
        application.logger.debug(f"views.home -> Usuario conectado: {current_user}")
        if current_user.is_authenticated:
            application.logger.debug(f"views.home -> Usuario autentificado, redirect to main")
            return redirect(url_for('views.mainPage'))
        else:
            application.logger.debug("views.home -> Ususario no autenticado o inactivo")
            logout_user()
            return redirect(url_for('auth.login'))
    except Exception as e: #Esto puede pasar si tiene una cookie no correspondiente
        logout_user()
        application.logger.error("views.home -> Ususario con cookie invalida o antigua")
        application.logger.error(f"views.home -> {e.args}")
        return redirect(url_for('auth.login'))

    
@views.route('/main')
@login_required
def mainPage():
    if request.method == 'GET':
        return render_template("home.html", this_user=current_user)