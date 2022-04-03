from importlib.resources import contents
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy 
import red #para los vecionos
import telnetlib
import ssh
import rip_ospf


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

@app.route('/topologia')
def Topoligia():
    aux='Para la deteccion de la topologia'
    #return redirect(url_for('home'))
    return render_template('base.html',aux=aux)

@app.route('/userrouter')
def Userrouter():
    aux= 'Para añadir usuarios a los routers'
    return render_template('userrouter.html',aux=aux)

#-----------------enrutamientos-------------------------------
@app.route('/rotocolos')
def enruterw():
    aux="Configuracion protocolos"
    return render_template('configurarprotocolo.html',aux=aux)

@app.route('/rotocolos/conf',methods=['POST'])
def enruterc():
    router= request.form['content'] 
    protocolo=request.form['content2']
    rip_ospf.enruter(router, protocolo)
    aux="PAra los protocolos....... debio configurar algo... creo"
    return render_template('mensajehome.html',aux=aux)

#----------------------ssh--------------------------
@app.route('/ssh')
def sshtw():
    aux="para el ssh, creo que funciona"
    return render_template('confssh.html',aux=aux)

@app.route('/ssh/conf', methods=['POST'])
def sshtc():
    username=request.form['content'] 
    contrasena= request.form['content2'] 
    ip= request.form['content3']
    ssh.ssht(username, contrasena, ip)
    aux="para el ssh, creo que funciona"
    return render_template('mensajehome.html',aux=aux)  




#------------------Telnet--------------
#Agrgar usuario telnet // edita la contraseña teniendo el nombre de usuario
@app.route('/telnet/crear',methods=['POST'])
def agregar():#ip,username,contrasena):
    
    
    #jala=request.form.get('content4')
    jala=1#añadir al formulario captura para la primer configuracion ip
    #añadir un agregar atodos los routers
    
    username=request.form['content'] 
    contrasena= request.form['content2'] 
    ip= request.form['content3']

    #print(jala)
        
    tn = telnetlib.Telnet(str(ip))
    #tn.write(b"enable \n")
    tn.read_until(b"Username: ")
    tn.write("kate\n".encode('UTF-8'))
    tn.read_until(b"Password: ")	
    tn.write("1234\n".encode('UTF-8'))
    tn.write(b"enable \n")
    tn.read_until(b"Password: ")
    tn.write("1234\n".encode('UTF-8'))	
    #tn.write(b"enable \n")
    tn.write(b"configure terminal \n")
    tn.write(("username " + str(username) + " priv 15 password " + str(contrasena) +"\n").encode('UTF-8'))
    tn.write(b"end \n")
    tn.write(b"exit \n")		
    texto =tn.read_all()
    print(texto.decode('UTF-8'))
    aux="usuario agregado con exito"
    return render_template('mensajehome.html',aux=aux)



#Editar usuario telnet //elimina el usuario teniendo el usuario
@app.route('/telnet/editar',methods=['POST'])
def Editar():
    username=request.form['content'] 
    contrasena= request.form['content2'] 
    ip= request.form['content3']
    tn = telnetlib.Telnet(str(ip))
    tn.read_until(b"Username: ")
    tn.write("kate\n".encode('UTF-8'))
    tn.read_until(b"Password: ")	
    tn.write("1234\n".encode('UTF-8'))	
    tn.write(b"enable \n")
    tn.read_until(b"Password: ")
    tn.write("1234\n".encode('UTF-8'))	
    tn.write(b"config t \n")
    tn.write(("username " + str(username) + " priv 15 password " + str(contrasena) +"\n").encode('UTF-8'))
    tn.write(b"end \n")
    tn.write(b"exit \n")		
    texto =tn.read_all()
    print(texto.decode('UTF-8'))
    aux="Credenciales de usuario actualizadas con exito"
    return render_template('mensajehome.html',aux=aux)

@app.route('/telnet/eliminar',methods=['POST'])
def eliminar():
    username=request.form['content']  
    ip= request.form['content3']
    tn = telnetlib.Telnet(str(ip))
    tn.read_until(b"Username: ")
    tn.write("kate\n".encode('UTF-8'))
    tn.read_until(b"Password: ")	
    tn.write("1234\n".encode('UTF-8'))	
    tn.write(b"enable \n")
    tn.read_until(b"Password: ")
    #tn.write("admin01\n".encode('UTF-8'))	
    tn.write("1234\n".encode('UTF-8'))	
    tn.write(b"config t \n")
    tn.write(("no username " + str(username) + "\n").encode('UTF-8'))
    tn.write(b"end \n")
    tn.write(b"exit \n")		
    texto =tn.read_all()
    print(texto.decode('UTF-8'))
    aux="Usuario eliminado con exito"
    return render_template('mensajehome.html',aux=aux)


if __name__ == '__main__':
    app.run(debug=True)