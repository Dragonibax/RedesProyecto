from crypt import methods
from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from utils.security import bcrypt
from utils.session import login_manager
from database import database
from apps.auth.models import User, Settings
from utils.topology import detect, topology
from utils import system_threads

auth = Blueprint('auth', __name__, template_folder="templates", url_prefix="/auth")
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))

@auth.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.get_by_email(request.form.get('email'))
        if user:
            if bcrypt.check_password_hash(user.password,request.form.get('password')):
                login_user(user)
                system_threads.start_scheduler()
                system_threads.start_thread('topology',Settings.get_settings().topology_time)
                return redirect(url_for('auth.dashboard'))
    return render_template('auth/sign-in.html')

@auth.route("/register",methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/sign-up.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        hashed = bcrypt.generate_password_hash(password,5)
        newUser = User(email=email, password=hashed, name=name)
        database.insert(newUser)
        return redirect(url_for('auth.login'))

@auth.route("/dashboard", methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('auth/dashboard.html',topology=topology)

@auth.route("/logout",methods=['GET'])
@login_required
def logout():
    logout_user()
    system_threads.stop_scheduler()
    return redirect(url_for('auth.login'))

@auth.route("/settings",methods=['GET'])
@login_required
def settings():
    return render_template('auth/settings.html', settings = Settings.get_settings())

@auth.route("/update/email",methods=['POST'])
@login_required
def change_email():
    email = request.form.get('actualEmail')
    new_email = request.form.get('newEmail')
    my_user = User.get_by_id(current_user.id)
    if my_user: #si existe el usuario
        my_user.update_email(new_email)
    return redirect(url_for('auth.settings'))

@auth.route("/update/password",methods=['POST'])
@login_required
def change_password():
    former_password = request.form.get('formerPass')
    new_password = request.form.get('newPass')
    new_hashed = bcrypt.generate_password_hash(new_password,5)
    my_user = User.get_by_id(current_user.id)
    if my_user:
        if bcrypt.check_password_hash(my_user.password,former_password):
            my_user.update_password(new_hashed)
    return redirect(url_for('auth.settings'))   

@auth.route("/delete",methods=['GET'])
@login_required
def delete():
    user = current_user
    database.delete(user)
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/topology/change",methods=['POST'])
@login_required
def configure_topology():
    new_time = int(request.form.get('detection_time'))
    Settings.update_topology_time(new_time)
    system_threads.change_interval('topology',new_time)
    return redirect(url_for('auth.dashboard'))

@auth.route("/interfaces/change",methods=['POST'])
@login_required
def configure_interfaces():
    new_time = int(request.form.get('query_time'))
    Settings.update_interfaces_time(new_time)
    return redirect(url_for('auth.dashboard'))

@auth.route("/top",methods=['GET'])
def top():
    detect()
    return redirect(url_for('auth.dashboard'))

@auth.app_errorhandler(404)
def page_not_found(e):
    return render_template('auth/404.html')