from database.database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(150), nullable = False)

    def __init__(self, email, password, name):
        self.password = password
        self.email = email
        self.name = name

    def __repr__(self):
        return '<Usuario %r>' % self.id

    def update_email(self,new_email):
        self.email = new_email
        db.session.commit()
    
    def update_password(self,new_password):
        self.password = new_password
        db.session.commit()

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(id):
        return User.query.filter_by(id=id).first()

class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, unique = True, primary_key = True)
    topology_time = db.Column(db.Integer, nullable = False)
    interfaces_time = db.Column(db.Integer, nullable = False)
    alert_interface_packets = db.Column(db.Text,nullable = False)
    alert_link = db.Column(db.Text, nullable = False)
    alert_interface_status = db.Column(db.Text, nullable = False)
    error_limit = db.Column(db.Integer, nullable = False)

    def __init__(self, topology_time, interfaces_time, alert_interface_packets, alert_interface_status, alert_link, error_limit):
        self.topology_time = topology_time
        self.interfaces_time = interfaces_time
        self.alert_interface_packets = alert_interface_packets
        self.alert_interface_status = alert_interface_status
        self.alert_link = alert_link
        self.error_limit = error_limit

    def __repr__(self):
        return '<Settings %r>' % self.id

    def update_topology_time(self,topology_time):
        self.topology_time = topology_time
        db.session.commit()

    def update_interface_time(self,interfaces_time):
        self.interfaces_time = interfaces_time
        db.session.commit()

    def update_error_limit(self,error_limit):
        self.error_limit = error_limit
        db.session.commit()

    def update_alerts(self,packets,status,link):
        self.alert_interface_packets = packets
        self.alert_interface_status = status
        self.alert_link = link
        db.session.commit()

    @staticmethod
    def get_settings():
        return Settings.query.first()