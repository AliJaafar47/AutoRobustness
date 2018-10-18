import telnetlib
import os
# function for CPU usage 


class DUT_metrics :
    
    def get_CPU_usage(self):
        HOST = "192.168.1.1"
        user = "root"
        password = "sah"
        tn = telnetlib.Telnet(HOST)
        tn.read_until(b"login: ")
        tn.write(user.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")
        tn.write(b"mpstat \r\n")
        result = tn.read_until(b"/cfg/system/root #exit", 2).decode('ascii')
        try :
            cpu_idle = result.split("\n")[-2].split("  ")[-1]
        except :    
            cpu_idle = "100"
        tn.write(b"exit\n")
        cpu_usage = str(100 - float(cpu_idle))
        print("CPU usage :",cpu_usage[:4])
        return (cpu_usage[:4])
    
    def get_Memory_usage(self):
        HOST = "192.168.1.1"  
        
        user = "root"
        password = "sah"
        tn = telnetlib.Telnet(HOST)
        tn.read_until(b"login: ")
        tn.write(user.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")
        tn.write(b"free \r\n")
        result = tn.read_until(b"/cfg/system/root #exit", 2).decode('ascii')
        try :
            memory_usage = result.split("\n")[-2].split()[-2]
            memory_usage = memory_usage[:3]
        except :    
            memory_usage = "0"
        print('Memory usage :',memory_usage)
        return(memory_usage)
    def get_wan_ip(self):
        HOST = "192.168.1.1"  
        user = "root"
        password = "sah"
        tn = telnetlib.Telnet(HOST)
        tn.read_until(b"login: ")
        tn.write(user.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")
        
        tn.write(b"ifconfig | grep 'addr:172.16.' | sed -e 's/P-/%/' -e 's/:/x/'| cut -d'x' -f2 | cut -d'%' -f1 | cut -d ' ' -f 1 \r\n")
        result = tn.read_until(b"/cfg/system/root #exit", 2).decode('ascii')
        lines = result.split("\n")[-2]
        print(lines)
        return (lines)
    def get_class(self):
        HOST = "192.168.1.1"  
        user = "root"
        password = "sah"
        tn = telnetlib.Telnet(HOST)
        tn.read_until(b"login: ")
        tn.write(user.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")
        
        tn.write(b"head /web/version.txt | grep BUILD_PROJECT\n")

        result = tn.read_until(b"/cfg/system/root #exit", 2).decode('ascii')
        lines = result.split("\n")[-2]
        if not lines :
            return (None)
        else :
            return (lines.split("=")[1])

class Build() : 
    def __init__(self,name):
        self.name = name

class Builds_list() : 
    def get_builds_names (self):
        lis = os.listdir("/var/www")
        print(lis)
        list_of_builds =[]
        for i in lis : 
           list_of_builds.append(Build(i)) 
        return list_of_builds
#a=Builds_list()
#a.get_builds_names()

