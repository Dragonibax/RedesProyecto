from sqlalchemy.exc import IntegrityError
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
import networkx as nx
import matplotlib.pyplot as plt
import pathlib
from apps.protocols.models import Router
from database import database
import re

topology = {}
topology_graph = None
routers = []
visitados = []

def parse_neighbors(text):
    devices = []
    device = []
    for line in text.split("\n"):
        if "Device ID" in line:
            device.append(line[11:])
        elif "IP address" in line:
            device.append(line[14:])
            devices.append(device)
            device = []
        else:
            continue
    return devices

def parse_networks(text):
    ips = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", text)
    return ','.join(ips)

def get_neighbors_of(connection,actual,anterior):
    global topology
    try:
        if topology.get(actual) != None:
            output = parse_neighbors(connection.send_command('show cdp neighbor detail'))
            topology[actual]['neighbors'] = output
            topology[actual]['networks'] = parse_networks(connection.send_command('show ip route connected | section include connected'))
            connection.send_command('exit',expect_string=anterior)
        else:
            topology[actual] = {}
            output = parse_neighbors(connection.send_command('show cdp neighbor detail'))
            topology[actual]['neighbors'] = output
            topology[actual]['networks'] = parse_networks(connection.send_command('show ip route connected | section include connected'))
            for device in output:
                if topology.get(device[0]) != None:
                    continue
                else:
                    connection.send_command(f'telnet {device[1]}',expect_string=r'\)\?|:|\$')
                    try:
                        connection.send_command('admin',expect_string=device[0]+'>',cmd_verify=False)
                    except Exception as e:
                        connection.send_command('admin',expect_string=device[0]+'#',cmd_verify=False)
                    get_neighbors_of(connection,device[0],actual)
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)    
        connection.disconnect()

""""La funcion para detectar la topologia siempre usara telnet, para garantizar su funcionamiento independientemente
de los usuarios ssh disponibles y los protocolos configurados dentro de los routers"""
def detect():
    global topology_graph, routers, topology
    device = {
        "device_type": "cisco_ios_telnet",
        "host": "192.168.0.1",
        "username": "admin",
        "password": "admin",
        "secret": "admin",
    }
    print("Detectando...")
    print("Routers anteriores...",routers)
    topology_graph = None
    topology = {}
    plt.clf()
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            get_neighbors_of(ssh,"R1",r'\)\?|:|\$')
            ssh.disconnect()
            #print(topology)
        #Una vez que se obtiene la topologia, se construye el grafo de networkx
        topology_graph = nx.Graph()
        topology_graph.add_nodes_from(topology)
        #Tambien resulta conveniente almacenar los routers en la base de datos
        print("Routers actuales...",topology.keys())
        for router in topology.keys():
            for neighbor in topology.get(router)['neighbors']:
                try:            
                    topology_graph.add_edge(router,neighbor[0])
                    if neighbor[0] not in routers:
                        new_router = Router(name=neighbor[0],ip=neighbor[1],protocol='no protocol',has_ssh='0',username='admin',password='admin',secret='admin',location='unknown',contact='ggnoteam@gmail.com',networks=topology.get(router)['networks'])
                        database.insert(new_router)
                    else:
                        routers.remove(neighbor[0])
                        continue
                except IntegrityError:
                    database.rollback()
                    continue
                    #Para este punto solo quedan en el arreglo de routers, aquellos que
        #ya no se encuentran en la topologia, por lo tanto, los borramos de la bd
        for router in routers:
            database.delete(Router.get_by_name(router))
        
        #Guardamos los nuevos routers anteriores para una futura consulta
        routers = []
        for router in topology.keys():
            routers.append(router)
        
        nx.draw(topology_graph,with_labels=True)
        #plt.show()
        plt.savefig(f"{pathlib.Path().resolve()}/static/assets/topology.png",format="PNG")
        return
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
        topology = {}
        topology_graph = None