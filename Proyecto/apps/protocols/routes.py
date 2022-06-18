from distutils.log import error
from flask import Blueprint, request, url_for, redirect, render_template, flash
from database import database
from apps.protocols.models import Router, Entry
from apps.users.models import SSHUser
from utils import sshconnection
from utils.topology import detect
from datetime import datetime

prot = Blueprint('protocols', __name__, template_folder = "templates", url_prefix = "/protocols")
# Suponemos que por alguna razón ya detectó la topología y encontró esto

@prot.route("/router", methods = ['GET', 'POST'])
def proto():
    routers = Router.query.all()
    sshUsers = SSHUser.query.all()
    return render_template('protocols/protocolos.html',routers=routers, sshUsers=sshUsers)

@prot.route("/router/<id>/configure", methods = ['GET', 'POST'])
def conf_protocolos(id):
    if request.method == 'GET':
        router = Router.get_by_id(id) 
        sshUsers = SSHUser.get_by_router(id)
        return render_template("protocols/configurar-router.html", router=router, sshUsers=sshUsers)
    else:
        errors = []
        router = Router.get_by_id(id) 
        name = router.name
        username = request.form['username-select']
        password = request.form['ssh-password']
        secret = router.secret
        protocol = request.form['protocolo-select']
        if protocol == '':
            errors.append('Debes seleccionar un protocolo')            
        if username is None or username == '':
            errors.append('Debes seleccionar un usuario')
        if password is None or password == '':
            errors.append('Debes ingresar tu contraseña')
        if errors:
            return render_template("protocols/configurar-router.html", router=router, sshUsers=sshUsers, errors=errors)
        sshUser = SSHUser.get_by_username(username)
        if sshUser.password == password:
            if router.protocol == 'no protocol':
                if sshconnection.enable_protocol(protocol, name, router.networks.split(',')):
                    entry = Entry(username=username,datetime=datetime.now(),action=f'Se ha cambiado el protocolo del router {router.id} de {router.protocol} a {protocol}')
                    router.update_protocol(protocol)
                    database.insert(entry)
                    return redirect(url_for('protocols.proto'))
                else:
                    errors.append('Hubo un error en el proceso, revise la configuración SSH del router')
                    return render_template("protocols/configurar-router.html", router=router, errors=errors)
            else:
                if sshconnection.change_protocol(router.protocol, protocol, name, router.networks.split(',')):
                    entry = Entry(username=username,datetime=datetime.now(),action=f'Se ha cambiado el protocolo del router {router.id} de {router.protocol} a {protocol}')
                    router.update_protocol(protocol)
                    database.insert(entry)
                    return redirect(url_for('protocols.proto'))
        else:
            errors.append('La contraseña es incorrecta')
        return render_template("protocols/configurar-router.html", router=router, sshUsers=sshUsers, errors=errors)

@prot.route("/entries",methods=['GET'])
def get_entries():
    entries = Entry.query.all()
    print(entries)
    return render_template("/protocols/entries.html",entries=entries)

@prot.app_errorhandler(404)
def page_not_found(e):
    return render_template('protocols/404.html')