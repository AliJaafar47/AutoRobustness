import telnetlib
# function for CPU usage 

def get_CPU_usage():
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
    print("CPU usage :",cpu_usage[:4]+"%")
    return (cpu_usage[:4]+"%")


def get_RAM_usage():
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
    except :    
        memory_usage = "0"
    print('Memory usage :',memory_usage)
    return(memory_usage)




