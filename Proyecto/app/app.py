from importlib.resources import contents
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/Users.db'


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuarios = db.Column(db.String(200))
    contrasena = db.Column(db.String(200))


@app.route('/')
def home():
    usuarios = Users.query.all()
    return render_template('index.html' , usuarios= usuarios)

@app.route('/create-Usuario', methods=['POST'])
def create():
    new_user = Users(usuarios=request.form['content'], contrasena= request.form['content2'])
    db.session.add(new_user)
    db.session.commit()
    #return 'funciona'
    return redirect(url_for('home'))

@app.route('/done/<id>')
def done(id):
    task = Users.query.filter_by(id=int(id)).first()
    task.done = not(task.done)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete/<id>')
def delete(id):
    Users.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)