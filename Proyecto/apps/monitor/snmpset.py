from pysnmp.hlapi import * 

def snmp_set(host,community,attr,value):
    iterator = setCmd(SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity('SNMPv2-MIB',attr,0),value))
    
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        return False
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))
        return True