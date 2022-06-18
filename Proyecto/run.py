from flask import Flask, redirect
#blueprints
from apps.auth.routes import auth
from apps.monitor.models import IfData
from apps.users.routes import users
from apps.protocols.routes import prot
from apps.monitor.routes import monit
from apps.alerts.routes import alerts
#utilities
from database import database
from utils import security, session, mailing, system_threads
from apps.auth.models import Settings
from datetime import datetime as dt
from apps.monitor import snmpget

app = Flask(__name__)
app.config.from_object('config.DevConfig')
app.register_blueprint(auth)
app.register_blueprint(prot)
app.register_blueprint(users)
app.register_blueprint(monit)
app.register_blueprint(alerts)
database.init_app(app)
security.init_app(app)
session.init_app(app)
mailing.init_app()

"""Este metodo inserta los mensajes que se enviaran al administrador del sistema mediante email. los valores entre
asteriscos seran sustituidos por las interfaces correspondientes"""
def init_settings():
    default_interface_packets = "La interface *name* ha sobrepasado el *value* de paquetes salientes"
    default_interface_status = "La interface *name* ha cambiado su estado a *status*"
    default_link = "El enlace entre *device1* y *device2* ha sobrepasado el *value* de paquetes perdidos"
    default_settings = Settings(topology_time=50,interfaces_time=10,alert_interface_packets=default_interface_packets, alert_interface_status=default_interface_status,alert_link=default_link,error_limit=1000) 
    database.insert(default_settings)
    snmpget.init_app('192.168.0.10','192.168.0.1','public',2400,default_settings.error_limit)
    snmpget.reset_interfaces()
    snmpget.init_interfaces()

@app.route("/")
def handle_redirect():
    return redirect('/auth/dashboard')

with app.app_context():
    database.create_tables()
    init_settings()

if __name__ == '__main__':
    app.run()