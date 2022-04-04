import telnetlib
#ssh mediante telnet

#username="cisco";
#password="cosco";
secret="1234";

def ssht(username, password, ip):
    comandos = [#"Activar el cifrado",
        "conf t \n",
        "enable secret 1234 \n",
        "exit \n",
        "service password-encryption \n",
        #"write",
        #"- Activar SSH",
        "conf t \n",
        "ip domain-name adminredes.escom.ipn.mx \n",
        "ip ssh rsa keypair-name ssh \n",
        "crypto key generate rsa usage-keys label sshkey modulus 1024 \n",
        "ip ssh v 2 \n",
        "ip ssh time-out 30 \n",
        "ip ssh authentication-retries 3 \n",
        "do show line \n",
        "line vty 0 6 \n",
        "password cisco \n",
        "login local \n",
        "transport input ssh telnet \n",
        "end \n",
        #"write",
        #"- Crear un usuario con nombre y password",
        "conf t \n",
        "username cisco privilege 15 password cisco \n",
        "end \n",
        #"write",
        "exit\n"] 

    tn = telnetlib.Telnet(str(ip))
    tn.read_until(b"Username: ")
    tn.write("kate\n".encode('UTF-8'))
    tn.read_until(b"Password: ")	
    tn.write("1234\n".encode('UTF-8'))
    tn.write(b"enable \n")
    tn.read_until(b"Password: ")
    tn.write("1234\n".encode('UTF-8'))	
    #tn.write(str(comandos))
    tn.write(b"config t \n")
    #tn.write(b"enable secret 1234 \n")
    tn.write(b"exit \n")
    tn.write(b"service password-encryption \n")
    tn.write(b"conf t \n")
    #tn.write(b"ip domain-name adminredes.escom.ipn.mx \n")
    tn.write(b"ip ssh rsa keypair-name ssh \n")
    tn.write(b"crypto key generate rsa usage-keys label ssh modulus 1024 \n")
    tn.write(b"ip ssh v 2 \n")
    tn.write(b"ip ssh time-out 30 \n")
    tn.write(b"ip ssh authentication-retries 3 \n")
    tn.write(b"do show line \n")
    tn.write(b"line vty 0 6 \n")
    tn.write(b"password 1234 \n")
    tn.write(b"login local \n")
    tn.write(b"transport input ssh telnet \n")
    tn.write(b"end \n")
    tn.write(b"conf t \n")
    tn.write(("username " + str(username) + " priv 15 password " + str(password) +"\n").encode('UTF-8'))
    tn.write(b"end \n")
    tn.write(b"exit\n")

    #tn.write(("username " + str(username) + " priv 15 password " + str(password) +"\n").encode('UTF-8'))
    #tn.write(b"end \n")
    #tn.write(b"exit \n")		
    
    
    
    
    
    texto =tn.read_all()
    print(texto.decode('UTF-8'))
    aux="usuario agregado con exito"
    #return render_template('mensajehome.html',aux=aux)

    #return aux