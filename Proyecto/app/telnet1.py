from flask import Flask, url_for,request
import telnetlib

app = Flask(__name__)

@app.route('/agregar/<ip>/<username>/<password>',methods=['GET'])
def agregar(ip,username,password):

	tn = telnetlib.Telnet(str(ip))
	tn.read_until(b"Username: ")
	tn.write("admin\n".encode('UTF-8'))
	tn.read_until(b"Password: ")	
	tn.write("admin01\n".encode('UTF-8'))	
	tn.write(b"config t \n")
	tn.write(("username " + str(username) + " priv 15 password " + str(password) +"\n").encode('UTF-8'))
	tn.write(b"end \n")
	tn.write(b"exit \n")		
	texto =tn.read_all()
	print(texto.decode('UTF-8'))
	return("usuario agregado con exito")
@app.route('/Editar/<ip>/<username>/<password>',methods=['GET'])
def Editar(ip,username,password):
	tn = telnetlib.Telnet(str(ip))
	tn.read_until(b"Username: ")
	tn.write("admin\n".encode('UTF-8'))
	tn.read_until(b"Password: ")	
	tn.write("admin01\n".encode('UTF-8'))	
	tn.write(b"config t \n")
	tn.write(("username " + str(username) + " priv 15 password " + str(password) +"\n").encode('UTF-8'))
	tn.write(b"end \n")
	tn.write(b"exit \n")		
	texto =tn.read_all()
	print(texto.decode('UTF-8'))
	return("Credenciales de usuario actualizadas con exito")
@app.route('/Eliminar/<ip>/<username>',methods=['GET'])
def eliminar(ip,username):
	tn = telnetlib.Telnet(str(ip))
	tn.read_until(b"Username: ")
	tn.write("admin\n".encode('UTF-8'))
	tn.read_until(b"Password: ")	
	tn.write("admin01\n".encode('UTF-8'))	
	tn.write(b"config t \n")
	tn.write(("no username " + str(username) + "\n").encode('UTF-8'))
	tn.write(b"end \n")
	tn.write(b"exit \n")		
	texto =tn.read_all()
	print(texto.decode('UTF-8'))
	return("Usuario eliminado con exito")

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)


