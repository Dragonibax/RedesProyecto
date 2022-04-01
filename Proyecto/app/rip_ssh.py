from netmiko import ConnectHandler
import netifaces as ni
import time;
# from detecta import *

user = 'cisco'
password = 'cisco'
secret = '1234'

cisco = {
	"device_type": "cisco_ios",
	'ip': '',
    "username": user,
    "password": password,
    "secret": secret
}

known_routers = []


def arr_to_ip(ip):
    return f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}"


def get_id_net(ip, net):
    idnet = []
    for i in range(4):
        idnet.append((ip[i] & net[i]))
    return idnet


def configure_router(router, hostname, con):
	output = con.send_command(f'show cdp entry {router}')
	resp = output.split();
	comando_ssh = 'ssh -l '+user+' '+resp[8];
	print("COMANDO:", comando_ssh);
	con.send_command(comando_ssh, expect_string=r'Password:')
	string_final = router.split(".")[0];
	print("string_final:", string_final);
	con.write_channel(password+'\n')
	# con.send_command(password, expect_string=r''+string_final+'#')

	rip(con)

	neighbors(router, con)
	print("HOSTNAME CONFIGURE:", hostname)
	con.send_command('exit', expect_string=hostname.split(".")[0]+'#')
	return 1;


def neighbors(hostname, con):
	output = con.send_command('show cdp neighbors')
	routers = output.split();
	# print("ROUTERS:",routers);
	routers.pop();
	# print("ROUTERS 2:",routers[35])
	# exit(1);

	i = 35
	while i < len(routers):
		if routers[i] not in known_routers:
			print(routers[i]+":")
			known_routers.append(routers[i])
			configure_router(routers[i], hostname, con)
		i = i + 8
	return 1;


def findNetworkID(ip, con):
	output = con.send_command('show ip interface brief | i '+ip)
	net = output.split()
	output = con.send_command('show running-config | i '+net[1])
	mask = output.split()

	addr = list(map(int, net[1].split(".")))
	netmask = list(map(int, mask[3].split(".")))

	idnet = get_id_net(addr, netmask)

	return arr_to_ip(idnet)


def rip(con):
	output = con.send_command('show ip interface brief | i up')
	ip = output.split()
	# print("SH IP INT BR:",ip);
	ip_id = []
	i = 1
	while i < len(ip):
		ip_id.append(findNetworkID(ip[i], con))
		i = i + 6

	print("ip_ids:", ip_id);
	con.write_channel('configure terminal\n')
	time.sleep(1)
	con.write_channel('no ip routing\n')
	time.sleep(5)
	con.write_channel('ip routing\n')
	time.sleep(2)
	con.write_channel('router rip\n')
	time.sleep(1)
	con.write_channel('version 2\n')
	time.sleep(1)

	for i in ip_id:
		print('RIP Network '+i)
		con.write_channel('network '+i+'\n')
		time.sleep(1)

	con.write_channel('exit\n')
	time.sleep(2)
	con.write_channel('exit\n')
	time.sleep(2)
	return 1;


cisco = {
	"device_type":"cisco_ios",
	'ip': '',
    "username":user,
    "password":password,
    "secret":secret
}

def init_rip_ssh(ip,userName,userPassword,secret="1234"):
	codigo=0;
	try:
		cisco['ip'] = ip
		cisco['username'] = userName
		cisco['password'] = userPassword
		cisco['secret'] = secret
		con = ConnectHandler(**cisco)
		output = con.send_command("show running-config | i hostname")
		hostname = output.split()
		print("HOSTNAME",hostname)
		known_routers.append(hostname[1])
		print(hostname[1]+":")
		rip(con)
		neighbors(hostname[1],con)
		con.disconnect()
	except Exception as e:
		print("ERRORRR:",str(e))
		codigo=-1
	return {
            "codigoResultado":codigo
        }
