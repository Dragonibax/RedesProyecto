from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

def send_config_commands(device,commands):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ssh.send_config_set(commands)
        return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
    
""" Esta funcion esta diseñada unicamente para enviar comandos tipo show y regresar la respuesta de los comandos dentro de un json"""
def send_commands(device,commands):
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
    return result

def enable_ssh_service(ip,name,username,password,secret):
    device = {
        "device_type" : "cisco_ios_telnet",
        "host": ip,
        "username": username,
        "password": password,
        "secret": secret
    }

    commands = ['service password-encryption',
                'ip domain-name caliente.com.mx',
                'ip ssh v 2',
                'ip ssh time-out 30',
                'ip ssh authentication-retries 3',
                'ip ssh rsa keypair-name sshkey',
                'crypto key generate rsa usage-keys label sshkey modulus 1024',
                'username root privilege 15 password root',
                'line vty 0 15',
                'login local',
                'transport input ssh',
                'end'
            ]

    result = send_config_commands(device,commands)
    #print(result)
    prompt = name+"#"

    if prompt in result: #Si nos devolvio la prompt Rx# entonces todo bien
        return True
    else:
        return False

def create_ssh_user(ip,name,username,password,secret,user_username,user_password):
    
    """El usuario del cual tenemos garantizada su existencia es root"""
    device = {
        "device_type" : "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
        "secret": secret
    }

    command = "username <myuser> privilege 15 password <mypass>"
    command = command.replace("<myuser>",user_username)
    command = command.replace("<mypass>",user_password)

    result = send_config_commands(device,[command,'end'])
    # print(result) para ver que regresa
    prompt = name+"#"
    if prompt in result:
        return True
    else:
        return False

def delete_ssh_user(ip,name,username,password,secret,user_username):
    
    device = {
        "device_type" : "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
        "secret": secret
    }

    command = "No username <myuser>"
    command = command.replace("<myuser>",user_username)

    result = send_config_commands(device,[command,'end'])
    # print(result) para ver que regresa
    prompt = name+"#"

    if prompt in result:
        return True
    else:
        return False

def enable_protocol(name, ip, username, password, secret, protocol):    
    print(ip+" "+username+" "+password+" "+ secret+" "+protocol)
    device = {
        "device_type" : "cisco_ios",
        "host": ip,
        "username": username, #usuario ssh 
        "password": password, #contraseña del usuario ssh
        "secret": secret
    }

    commands = []
    
    if protocol == 'OSPF':
        commands.append('router ospf 1')
        commands.append('network 192.168.0.0 0.0.0.255 area 0')
        commands.append('end') #importante enviar al final

    if protocol == 'RIP':
        commands.append('router rip')
        commands.append('version 2')
        commands.append('no auto-summary')
        commands.append('network 192.168.0.0')
        commands.append('end')
    
    result = send_config_commands(device,commands)
    prompt = name + '#'

    if prompt in result: 
        return True
    else:
        return False

def change_protocol(name, ip, username, password, secret, old_protocol, new_protocol):
    print(ip+" "+username+" "+password+" "+ secret+" "+old_protocol+" "+new_protocol)
    device = {
        "device_type" : "cisco_ios",
        "host": ip,
        "username": username, #usuario ssh 
        "password": password, #contraseña del usuario ssh
        "secret": secret
    }

    commands = []

    if old_protocol == "OSPF":
        commands.append('no router ospf')

    if old_protocol == "RIP":
        commands.append('no router rip')

    if new_protocol == 'OSPF':
        commands.append('router ospf 1')
        commands.append('network 192.168.0.0 0.0.0.255 area 0')
        commands.append('end') #importante enviar al final

    if new_protocol == 'RIP':
        commands.append('router rip')
        commands.append('version 2')
        commands.append('no auto-summary')
        commands.append('network 192.168.0.0')
        commands.append('end')
    
    result = send_config_commands(device,commands)
    prompt = name + '#'

    if prompt in result: 
        return True
    else:
        return False
