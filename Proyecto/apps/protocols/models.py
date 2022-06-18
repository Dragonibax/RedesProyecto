from enum import unique
from database.database import db

class Router(db.Model):
    __tablename__ = 'routers'
    id = db.Column(db.Integer, unique = True, primary_key = True)
    name = db.Column(db.String(20), unique = True)
    ip = db.Column(db.String(15), unique = True)
    protocol = db.Column(db.String(10))
    has_ssh = db.Column(db.String(1))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    secret = db.Column(db.String(255))
    location = db.Column(db.String(255))
    contact = db.Column(db.String(255))
    networks = db.Column(db.String(255))

    def __init__(self, name, ip, protocol, has_ssh, username, password, secret, location, contact, networks):
        self.name = name
        self.ip = ip
        self.protocol = protocol
        self.has_ssh = has_ssh
        self.username = username
        self.password = password
        self.secret = secret
        self.location = location
        self.contact = contact
        self.networks = networks

    def __repr__(self):
        return '<Router %r>' % self.id

    def update_ssh_status(self,new_status):
        self.has_ssh = new_status
        db.session.commit()

    def update_username(self,username):
        self.username = username
        db.session.commit()

    def update_password(self,password):
        self.password = password
        db.session.commit()

    def update_protocol(self,new_protocol):
        self.protocol = new_protocol
        db.session.commit()

    def update_name(self,name):
        self.name = name
        db.session.commit()
        
    def update_location(self,location):
        self.location = location
        db.session.commit()

    def update_contact(self,contact):
        self.contact = contact
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Router.query.filter_by(id=id).first()

    @staticmethod
    def get_by_name(name):
        return Router.query.filter_by(name=name).first()

class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, unique = True, primary_key = True)
    username = db.Column(db.String(255))
    datetime = db.Column(db.String(50))
    action = db.Column(db.String(255))
    
    def __init__(self,username,datetime,action):
        self.username = username
        self.datetime = datetime
        self.action = action

    def __repr__(self):
        return '<Entry %r>' % self.id
