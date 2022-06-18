from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from datetime import datetime as dt
from apps.monitor.models import IfData
from apps.protocols.models import Entry
from apps.auth.models import Settings
from database import database
from utils import mailing

cmdGen = None
snmpEngine = None
hostAddress = None
routerAddress = None
communityName = None
hostPort = 0
errorLimit = 0
interfaces = []

def init_app(host = "192.168.0.10", router = "192.168.0.1", community = "public", port = 2400, error = 500):
    global cmdGen, snmpEngine, hostAddress, routerAddress, communityName, hostPort, interfaces
    hostAddress = host
    routerAddress = router
    communityName = community
    hostPort = port 
    errorLimit = error
    interfaces = []
    snmpEngine = engine.SnmpEngine()
    cmdGen = cmdgen.CommandGenerator()
    config.addTransport(
        snmpEngine,
        udp.domainName + (1,),
        udp.UdpTransport().openServerMode((hostAddress, port))
    )
    #Configuracion de comunidad V1 y V2c
    config.addV1System(snmpEngine, communityName, communityName)
    print('PySNMP Traps configurado correctamente...')


def print_results(snmpEngine, stateReference, contextEngineId, contextName,varBinds, cbCtx):
    print('Nueva trap entrando...')
    time = dt.now().strftime("%H:%M:%S")
    description = "La interface "
    for name, val in varBinds:
        if "1.3.6.1.2.1.2.2.1.2" in name.prettyPrint():
            description = description + val.prettyPrint() + " ha cambiado su estado a "
        if "1.3.6.1.4.1.9.2.2.1.1.20" in name.prettyPrint():
            description = description + val.prettyPrint()
    if description != "La interface ":
        new_entry = Entry('SNMPAgent',time,description)
        mailing.send_email(description,'Cambio de estado en interfaz')
        database.insert(new_entry)

def start_listen():
    global snmpEngine
    #Se recibes alguna notificacion del router, manda a llamar a print_results
    ntfrcv.NotificationReceiver(snmpEngine, print_results)
    snmpEngine.transportDispatcher.jobStarted(1)  
    try:
        snmpEngine.transportDispatcher.runDispatcher()
        print('Escuchando traps...')
    except:
        snmpEngine.transportDispatcher.closeDispatcher()
        raise

def stop_listen():
    global snmpEngine
    snmpEngine.transportDispatcher.jobFinished(1)    
    snmpEngine.transportDispatcher.closeDispatcher()
    return