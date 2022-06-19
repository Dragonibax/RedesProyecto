from crypt import methods
from struct import pack
from flask import Blueprint, request, url_for, redirect, render_template, flash
from apps.monitor.models import IfData, Interface
from apps.monitor.snmpset import snmp_set
from apps.protocols.models import Router
from apps.alerts.models import Record
from apps.auth.models import Settings
from utils import mailing, system_threads, graphs
from apps.monitor import snmpget, snmptraps
from database import database
from datetime import datetime as dt


monit = Blueprint('monitor', __name__, template_folder = "templates", url_prefix = "/snmp")
# Suponemos que por alguna razón ya detectó la topología y encontró esto

@monit.route("/device",methods=['GET'])
def devices():
    return render_template("monitor/devices.html",routers=Router.query.all())

@monit.route("/device/<id>/edit",methods=['GET'])
def edit(id):
    return render_template("monitor/edit.html",router=Router.get_by_id(id))

@monit.route("/device/<id>/start",methods = ['GET'])
def start_monitor(id):
    router = Router.get_by_id(id)
    settings = Settings.get_settings()
    #system_threads.stop_thread('topology')
    snmpget.reset_interfaces()
    snmpget.init_app('192.168.0.10',router.ip,'public',2400,settings.error_limit)
    snmptraps.init_app('192.168.0.10',router.ip,'public',2400,settings.error_limit)
    snmpget.init_interfaces()
    system_threads.start_thread('interfaces',settings.interfaces_time)
    system_threads.start_thread('traps')
    return redirect(url_for('monitor.monitor_interface',id=id))


@monit.route("/device/<id>/monitor",methods = ['GET'])
def monitor_interface(id):
    router = Router.get_by_id(id)
    graphs.generate_graphs_interfaces()
    inter = []
    for item in Interface.get_interfaces():
        name = item.interface.replace("/","_")
        inter.append('files/'+name+'.png')
    print("Inter...",inter)
    return render_template('/monitor/graphs.html',interfaces = inter, router = router)

@monit.route("/device/<id>/stop",methods = ['GET'])
def stop_monitor(id):
    system_threads.stop_thread('interfaces')
    system_threads.stop_thread('traps')
    snmpget.delete_interfaces()
    return redirect(url_for('monitor.devices'))

@monit.route("/topology/view",methods = ['GET'])
def view():
    return render_template("monitor/view.html")

@monit.route("/device/<id>/name",methods=['POST'])
def change_name(id):
    router = Router.get_by_id(id)
    name = request.form.get('sysname')
    mailing.send_email(f'El router {router.name} ha cambiado su nombre a {name}','Cambios en la MIB-II','sabino.snm@gmail.com')
    router.update_name(name)
    return redirect(url_for('monitor.edit',id=id))

@monit.route("/device/<id>/location",methods=['POST'])
def change_location(id):
    router = Router.get_by_id(id)
    location = request.form.get('syslocation')
    mailing.send_email(f'El router {router.name} ha cambiado su ubicacion a {location}','Cambios en la MIB-II','sabino.snm@gmail.com')
    router.update_location(location)
    return redirect(url_for('monitor.edit',id=id))

@monit.route("/device/<id>/name",methods=['POST'])
def change_contact(id):
    router = Router.get_by_id(id)
    contact = request.form.get('syscontact')
    mailing.send_email(f'El router {router.name} ha cambiado su contacto a {contact}','Cambios en la MIB-II','sabino.snm@gmail.com')
    router.update_contact(contact)
    return redirect(url_for('monitor.edit',id=id))
