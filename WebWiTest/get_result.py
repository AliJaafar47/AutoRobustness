import telnetlib
HOST = "192.168.1.1"
user = "root"
password = "sah"
sport="5001"
tn = telnetlib.Telnet(HOST)
tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")

if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

dport=sport
ip="192.168.1.103"
id="IPerf_Send_Traffic_Port_"+sport
command = "Firewall.setPortForwarding(id:"+id+", origin:webui, sourceInterface:data, externalPort:"+sport+", internalPort:"+dport+", destinationIPAddress:"+ip+", protocol:6, enable:true, persistent:true, description:download)"
ch = command.encode()

print("pcb_cli")
tn.write(b"pcb_cli '"+ch+b"'\n")
print("before exit")
tn.write(b"exit\n")
print("after exit")       
print(tn.read_all().decode('ascii'))
print("end")