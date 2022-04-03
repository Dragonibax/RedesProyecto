import os
from netmiko import ConnectHandler;

user_name="kate";
password="1234";
secret="1234";


def get_neighbour(neighbour):
    elementos=neighbour.split(" ");
    return {
		"hostname": elementos[1][0:2],
		"ip_vecino_inmediato":elementos[6],
		"nombre_interfaz":elementos[8]
	}

def comando_neighbors(respuesta_neighbor):
	primer_particion=respuesta_neighbor.replace("\n"," ").replace(",","").strip().split("Device ID:");
	primer_particion.pop(0);
	lista=[];
	for neighbour in primer_particion:
		neighbour_json=get_neighbour(neighbour);
		lista.append(neighbour_json);

	return lista;

def get_networkmask(prefix):

	prefix_int=int(prefix);
	cadena="";
	ipv4len=32;
	ceros=32-prefix_int;

	for i in range(0,int(prefix_int)):
		cadena=cadena+"1";

	for i in range(0,ceros):
		cadena=cadena+"0";

	primer_octeto=cadena[0:8];
	segundo_octeto=cadena[8:16];
	tercer_octeto=cadena[16:24];
	cuarto_octeto=cadena[24:]

	return str(int(primer_octeto, 2))+"."+str(int(segundo_octeto, 2))+"."+str(int(tercer_octeto, 2))+"."+str(int(cuarto_octeto, 2))

def show_ip_row(resultado):

	resultado=resultado.strip().replace("\n","").split(" ");
	#print(resultado);
	id_red=resultado[3].split("/")[0];
	prefix=resultado[3].split("/")[1];
	return {
	"id_red":id_red,
	"prefix":prefix,
	"networkmask": get_networkmask(prefix)
	}

def enrutamiento_ospf(mi_ip,siguiente_salto, conta):
	informacion_red = netmiko_connection(mi_ip,"show ip route " +siguiente_salto,False);
	get_neighbour_information = show_ip_row(informacion_red);

	#comandos = ["interface loopback 0",
	#	"ip add 200.0.0.3 255.255.255.255"]
	#ejecucion=netmiko_connection(mi_ip,comandos,True);
	#print("Inicio OSPF:",ejecucion)

	comando="network "+get_neighbour_information["id_red"]+" 0.0.0.255 area 1";

	comandos=["router ospf "+conta,
		"redistribute rip subnets",
		comando]
	ejecucion=netmiko_connection(mi_ip,comandos,True);
	print("Inicio OSPF_:",ejecucion)
	return ejecucion;

def enrutamiento_rip(mi_ip, siguiente_salto):
	informacion_red = netmiko_connection(mi_ip, "show ip route " + siguiente_salto);
	get_neighbour_information = show_ip_row(informacion_red);

	comando = "network " + get_neighbour_information["id_red"];

	comandos = ["router rip",
		"version 2",
		#"redistribute ospf 1 metric 1",
		"no auto-summary",
		comando,
		"exit",
		"exit",
		#"configure terminal",
		"show ip route",
		"show ip protocols"]

	ejecucion = netmiko_connection(mi_ip, comandos,True);
	print(ejecucion)
	return ejecucion

def netmiko_connection(ip_vecino_inmediato,comando, isForConfig=False):
	cisco1 = {
		"device_type": "cisco_ios",
		"ip": ip_vecino_inmediato,
		"username": user_name,
		"password": password,
		"secret": secret
	}
	net_connect = ConnectHandler(**cisco1)
	net_connect.enable()
	if(isForConfig):
		salidaComando = net_connect.send_config_set(comando);
	else:
		salidaComando = net_connect.send_command(comando);

	net_connect.disconnect()
	return salidaComando;


      
def enruter(router, protocolo):
#de awuiwi debe estar configurado ssh
	print("Empezando Deteccion de direcciones ips, y enrutamiento STATICO, RIP Y OSPF en router \n")
	informacion_interfaz_enlace = os.popen('ip route').read() 
    #informacion_interfaz_enlace = ipw
	#print (informacion_interfaz_enlace)
	informacion_array=informacion_interfaz_enlace.strip().replace("\n","").split(" ");
	#print(informacion_array)
	interfaz={
		"VMGateway":informacion_array[2],
		"prefix":informacion_array[9].split("/")[1],
		"ip":informacion_array[9].split("/")[0]
	}
	print(interfaz)
	comando_neighbours = netmiko_connection(interfaz["VMGateway"],"show cdp neighbors detail | i Device ID|IP address|Interface:")
	lista_neighbours = comando_neighbors(comando_neighbours);

	contador=0;    

	#Los enrutamientos son entre el router conectado y el router adyacente de nombre por parametro
    #Enrutamiento rip
	for neighbour in lista_neighbours:

		if (neighbour["hostname"] == router and protocolo=="rip"):
			enrutamiento_rip(interfaz["VMGateway"], neighbour["ip_vecino_inmediato"]);
			print("FINALIZACION ENRUTAMIENTO RIP ENTRE ROUTER ADYASENTE Y:",neighbour["hostname"])            
		else:#Enrutamiento ospf
			if (neighbour["hostname"] == router and protocolo=="ospf"):
				enrutamiento_ospf(interfaz["VMGateway"], neighbour["ip_vecino_inmediato"],contador)
				print("FINALIZACION ENRUTAMIENTO OSPF ENTRE ROUTER ADYASENTE Y:", neighbour["hostname"])			
				contador=contador+1 



				#desabilitar el secret en los routers y cambiar la contraseña por 1234