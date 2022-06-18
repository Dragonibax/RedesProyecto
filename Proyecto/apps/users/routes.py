from flask import Blueprint, request, url_for, redirect, render_template, flash
from database import database
from utils import sshconnection
from apps.protocols.models import Router, Entry
from apps.users.models import SSHUser

users = Blueprint('users', __name__, template_folder="templates", url_prefix="/users")

@users.route("/device",methods=['GET'])
def list_devices():
    return render_template('users/devices.html',routers=Router.query.all())

@users.route("/device/<id>/users",methods=['GET'])
def list_users(id):
    selected = Router.get_by_id(id)
    users = SSHUser.get_by_router(id)
    return render_template('users/users.html',router=selected, sshusers=users, size=len(users))

@users.route("/device/<id>/new",methods=['GET','POST'])
def new(id):
    parent = Router.get_by_id(id)
    if request.method == 'GET':
        return render_template('users/nuevo.html',router=parent)
    else:
        u_username = request.form.get('username')
        u_password = request.form.get('password')
        if sshconnection.create_ssh_user(u_username,u_password,parent.name):
            new_user = SSHUser(username=u_username,password=u_password, router_id=id)
            database.insert(new_user)
            return redirect(url_for('users.list_users',id=id))
        else:
            return redirect(url_for('auth.dashboard'))

@users.route("/device/<id>/enable",methods=['GET'])
def enable(id):
    parent = Router.get_by_id(id)
    if sshconnection.enable_ssh_service(parent.name):
        parent.update_ssh_status('1')
        parent.update_username('root')
        parent.update_password('root')
        return redirect(url_for('users.list_devices'))
    else:
        return redirect(url_for('auth.dashboard'))

## Eliminar Usuario

@users.route("/device/<id>/delete/<idu>",methods=['GET'])
def delete(id,idu):
    parent = Router.get_by_id(id)
    usu = SSHUser.get_by_id(idu)
    if sshconnection.delete_ssh_user(usu.username,parent.name):
        database.delete(usu)
        return redirect(url_for('users.list_users',id=id))
    else:
            return redirect(url_for('auth.dashboard'))

## modificar usaarios
#cambia el meotodo por post
@users.route("/device/<id>/modify/<idu>",methods=['GET','POST'])
def modify(id,idu):
    parent = Router.get_by_id(id)
    nsu = SSHUser.get_by_id(idu) #obtenemos el usuario actual
    if request.method == 'GET':
        return render_template('users/modify.html',router=parent,user=nsu)
    else:        
        old_username = request.form.get('oldusername')
        new_username = request.form.get('username')
        new_password = request.form.get('password')
        if sshconnection.delete_ssh_user(old_username,parent.name):
            if sshconnection.create_ssh_user(new_username,new_password,parent.name):
                nsu.update_username(new_username)
                nsu.update_password(new_password)
                return redirect(url_for('users.list_users',id=id))
            else:
                return redirect(url_for('auth.dashboard'))    
        else:
            return redirect(url_for('auth.dashboard'))