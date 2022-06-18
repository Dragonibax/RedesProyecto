from flask import Blueprint, request, url_for, redirect, render_template
from apps.alerts.models import Record
from apps.auth.models import Settings
from utils.mailing import send_email
from apps.monitor import snmpget

alerts = Blueprint('alerts', __name__, template_folder="templates", url_prefix="/correo")

@alerts.route("/configure",methods=['GET','POST'])
def configure():
    default_settings = Settings.get_settings()
    if request.method == 'GET':
        return render_template('alerts/configure.html',settings=default_settings,error_limit=Settings.get_settings().error_limit)
    else:
        alert_interface_packets = request.form.get('packets')
        alert_interface_status = request.form.get('status')
        alert_link = ''
        default_settings.update_alerts(alert_interface_packets,alert_interface_status,alert_link)
        return redirect(url_for('alerts.configure'))

@alerts.route("/records",methods=['GET'])
def list_records():
    records = Record.get_records()
    return render_template('alerts/records.html',records=records)