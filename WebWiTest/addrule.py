import telnetlib

HOST = "192.168.1.1"
user = "root"
password = "sah"

tn = telnetlib.Telnet(HOST)
tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")

if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")


sport="5004"
dport="5004"
ip="192.168.1.10"
id="IPerf_Send_Traffic_Port_"+sport
command = "Firewall.setPortForwarding(id:"+id+", origin:webui, sourceInterface:data, externalPort:"+sport+", internalPort:"+dport+", destinationIPAddress:"+ip+", protocol:6, enable:true, persistent:true, description:download)"
ch = command.encode()

print("pcb_cli")
tn.write(b"pcb_cli '"+ch+b"'\n")
#tn.write(b"pcb_cli\n")

#tn.read_until(b" >")
print("before exit")
tn.write(b"exit\n")
print("after exit")

print(tn.read_all().decode('ascii'))
print("end")
