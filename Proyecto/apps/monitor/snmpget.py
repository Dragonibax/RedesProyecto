from ctypes.wintypes import PWIN32_FIND_DATAA
from dis import pretty_flags
from pysnmp.hlapi import *
from datetime import datetime as dt
from apps.alerts.models import Record
from apps.monitor.models import IfData, Interface
from apps.protocols.models import Entry
from apps.auth.models import Settings
from database import database
from utils import mailing

hostAddress = None
routerAddress = None
communityName = None
hostPort = 0
errorLimit = 0

def init_app(host = "192.168.0.10", router = "192.168.0.1", community = "public", port = 2400, error = 500):
    global hostAddress, routerAddress, communityName, hostPort, interfaces, errorLimit
    hostAddress = host
    routerAddress = router
    communityName = community
    hostPort = port 
    errorLimit = error
    print("PySNMP Interfaces configurado correctamente...")
    

def init_interfaces():
    time = dt.now().strftime("%H:%M:%S")
    print("Inicializando interfaces...",end='') 
    for _, _, _, varBinds in nextCmd(
        SnmpEngine(),
        CommunityData(communityName, mpModel=1),
        UdpTransportTarget((routerAddress, 161)),
        ContextData(),
        ObjectType(ObjectIdentity('IF-MIB', 'ifDescr')),
        lexicographicMode=False):
        ifName = varBinds  # unpack the list of resolved objectTypes
        ifName = ifName[0][1].prettyPrint()
        if "Null" not in ifName:
            new_interface_data = IfData(ifName,0,0,0,0,time)
            database.insert(new_interface_data)
            new_interface_name = Interface(ifName)
            database.insert(new_interface_name)
    print("[OK]")

def get_interfaces_data():
    global communityName, routerAddress
    print("Leyendo informacion de snmp_query...")
    time = dt.now().strftime("%H:%M:%S") 
    try:
        for _, _, _, varBinds in nextCmd(
            SnmpEngine(),
            CommunityData(communityName, mpModel=1),
            UdpTransportTarget((routerAddress, 161)),
            ContextData(),
            ObjectType(ObjectIdentity('IF-MIB', 'ifDescr')),
            ObjectType(ObjectIdentity('IF-MIB', 'ifOutUcastPkts')),
            ObjectType(ObjectIdentity('IF-MIB', 'ifInUcastPkts')),
            ObjectType(ObjectIdentity('IF-MIB', 'ifInErrors')),
            ObjectType(ObjectIdentity('IF-MIB', 'ifOperStatus')),
            lexicographicMode=False):
            ifName, outPackets, inPackets, inErrors, ifStatus = varBinds  # unpack the list of resolved objectTypes
            ifName = ifName[1].prettyPrint()
            outPackets = outPackets[1].prettyPrint()
            inPackets = inPackets[1].prettyPrint()
            inErrors = inErrors[1].prettyPrint()
            ifStatus = '0' if ifStatus[1].prettyPrint() != 'up' else '1'
            if "Null" not in ifName:
                print("Obtengo la interfaz...",ifName)
                packet_diff = int(inPackets) - IfData.get_last_record(ifName).inerrors
                data = IfData(ifName, inPackets, inErrors, outPackets, ifStatus, time)
                database.insert(data)
                if  packet_diff > errorLimit:
                    message = Settings.get_settings().alert_interface_packets
                    message = message.replace('*name*',ifName)
                    message = message.replace('*value*',str(errorLimit))
                    new_record = Record('SNMPget',dt.now().strftime("%Y-%m-%d-%H:%M:%S"), message)
                    database.insert(new_record)
                    mailing.send_email(message,'Limite de paquetes superado')
    except Exception as ex:
        print("Fallo en get_interfaces_data")
        print(ex)

def delete_interfaces():
    IfData.delete_all()

def reset_interfaces():
    Interface.reset_interfaces()