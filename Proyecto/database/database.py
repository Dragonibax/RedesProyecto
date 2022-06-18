"""Esta clase nos permite construir todos los modelos contenidos en los archivos
models.py de cada blueprint que tenemos"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.app = app
    db.init_app(app)

def create_tables():
    db.create_all()
    
def insert(data):
    db.session.add(data)
    db.session.commit()
    
def delete(data):
    db.session.delete(data)
    db.session.commit()

def update():
    db.session.commit()

def modify(data):
    user = db.session.query(data).filter(data).first()
    user.username = data.username
    user.password = data.password
    db.session.commit()

def rollback():
    db.session.rollback()
    db.session.commit()