import sys
import time
import select
import paramiko
import os
import threading
 
from .models import Project, Step, Test_Result, Step_Result, Project_result
import telnetlib

def isDigit(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

class Server(threading.Thread):
    def __init__(self,test_time,server_username,server_pwd,ip_server):
        threading.Thread.__init__(self)
        file = open("log.txt","w")
        file.write("")
        file.close()  
        self.test_time =test_time 
        self.ip_server = ip_server
        self.server_username =server_username
        self.server_pwd = server_pwd
        
    def run(self):
        #host = '192.168.1.105'
        i = 1
        while True:
            print ('Trying to connect to %s (%i/2)' % (self.ip_server, i))
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(str(self.ip_server), port=22, username=str(self.server_username), password=str(self.server_pwd))
                print ("Connected to %s" % self.ip_server)
                break
            except paramiko.AuthenticationException:
                print ("Authentication failed when connecting to %s" % self.ip_server)
                sys.exit(1)
            except:
                print ("Could not SSH to %s, waiting for it to start" % self.ip_server)
                i += 1
                time.sleep(2)

        # If we could not connect within time limit
            if i == 2:
                print ("Could not connect to %s. Giving up" % self.ip_server)
                sys.exit(1)

    # Send the command (non-blocking)

        stdin, stdout, stderr = ssh.exec_command("echo $$ ; exec iperf -s -i 1")
        pid = stdout.readline()
        print(pid)
        iperf_time = 20
        test_time = time.time()+ iperf_time
        
                
        while not stdout.channel.exit_status_ready() :
            # Only print data if there is data to read in the channel
            if test_time < time.time():
                break
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
        
# Disconnect from the host
#       time
        
        
        print ("Command done, closing SSH connection")
        stdin, stdout, stderr = ssh.exec_command(" sudo kill -9 "+pid )

        ssh.close()

class Client(threading.Thread):
    def __init__(self,test_time,client_username,client_pwd,ip_client,ip_server):
        threading.Thread.__init__(self)
        self.test_time=test_time
        
        ip_server = ip_server
        self.ip_client=ip_client
        self.ip_server=ip_server
        self.client_pwd=client_pwd
        self.client_username=client_username

        
    def run(self):
        host = self.ip_client
        i = 1
        while True:
            print ('Trying to connect to %s (%i/2)' % (host, i))

            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port=22, username=self.client_username, password=self.client_pwd)
                print ("Connected to %s" % host)
                break
            except paramiko.AuthenticationException:
                print ("Authentication failed when connecting to %s") % host
                sys.exit(1)
            except:
                print ("Could not SSH to %s, waiting for it to start" % host)
                i += 1
                time.sleep(2)

        # If we could not connect within time limit
            if i == 30:
                print ("Could not connect to %s. Giving up") % host
                sys.exit(1)

    # Send the command (non-blocking)
    
        stdin, stdout, stderr = ssh.exec_command("iperf -c "+str(self.ip_server)+" -i 1 > data_stdout.log")
        ssh.close()
        
class MyThread_GetResult(threading.Thread):
    
    def __init__(self,client_username,client_pwd,ip_client):
        threading.Thread.__init__(self)
        self.client_username=client_username
        self.client_pwd=client_pwd
        self.ip_client=ip_client
        
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False 
      
      
    def run(self):
        host = self.ip_client
        i = 1
        while True:
            print ('Trying to connect to %s (%i/2)' % (host, i))

            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port=22, username=self.client_username, password=self.client_pwd)
                print ("Connected to %s" % host)
                break
            except paramiko.AuthenticationException:
                print ("Authentication failed when connecting to %s") % host
                sys.exit(1)
            except:
                print ("Could not SSH to %s, waiting for it to start" % host)
                i += 1
                time.sleep(2)

        # If we could not connect within time limit
            if i == 30:
                print ("Could not connect to %s. Giving up") % host
                sys.exit(1)

    # Send the command (non-blocking)
    
        sftp = ssh.open_sftp()
        remotePath="/home/pi/data_stdout.log"
        localPath="/home/sah/data_stdout.log"
        sftp.get(remotePath,localPath) 
        time.sleep(4) 
        print(self.get_result())
        
    def get_result(self):
        try:
            lst = []
            cfg_file = open('/home/sah/data_stdout.log','r')
            
            lines = cfg_file.readlines()
            lines = lines[6:] 
            list_integer = []
    
            for line in lines: 
                print(line[-17:-10])
                if isDigit(line[-17:-10]):
                    list_integer.append(float(line[-17:-10])) 
                      
            if len(list_integer)==0:
                return 0
            
            return(round(sum(list_integer)/len(list_integer)))
        except IOError :
            print("can't open the file or file didn't exist")      

class TestSendData():
    def __init__(self,test_time,class_name,IDTable):
        
        #setting tables 
        self.table = Test_Result.objects.get(test_id=IDTable)
        self.table_one = Test_Result.objects.filter(test_id=IDTable)
        
        self.test_time= test_time
        self.class_name = class_name
        self.IDTable = IDTable
        self.iperf_time = 10
        timeout = time.time() + self.test_time
            
        while time.time() < timeout :
            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            jobs = []
            a = Server(self.iperf_time,"pi","raspberry","192.168.1.104")
            jobs.append(a)
            
            self.table_one.update(state="Connected to Distant Host")

            self.table_one.update(state="Sending Data")
            b = Client(self.iperf_time,"pi","raspberry","192.168.1.106","192.168.1.104")
            
            jobs.append(b)
            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            

            [k.start() for k in jobs ]
            [k.join() for k in jobs ]
            
            #writing results  in data base 
            c=MyThread_GetResult('pi','raspberry','192.168.1.106')
            c.start()
            
            metrics = self.table.metrics.all()
            
            for j in metrics :
                if j.name == "THROUGHPUT" :
                    if str(self.get_result())!="0":
                        j.update_values(str(self.get_result())+" Mbit/s")
                        j.add_new_value(str(self.get_result()))

            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            
        
        
        self.table_one.update(state="Finished")
        self.table_one.update(progress=str(100))
        
    def get_result(self):
        try:
            lst = []
            cfg_file = open('/home/sah/data_stdout.log','r')
            
            lines = cfg_file.readlines()
            lines = lines[6:] 
            list_integer = []
    
            for line in lines: 
                print(line[-17:-10])
                if isDigit(line[-17:-10]):
                    list_integer.append(float(line[-17:-10])) 
                      
            if len(list_integer)==0:
                return 0
            
            return(round(sum(list_integer)/len(list_integer)))
        except IOError :
            print("can't open the file or file didn't exist")  
            
            
            
            
    def add_nat_pat_rule (self,ip,sport):
        
        HOST = "192.168.1.1"
        user = "root"
        password = "sah"
        
        tn = telnetlib.Telnet(HOST)
        tn.read_until(b"login: ")
        tn.write(user.encode('ascii') + b"\n")
        
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")
        
        dport=sport
        ip="192.168.1.10"
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
        


#a = Client(20,'pi','raspberry','192.168.1.106','192.168.1.104')
#b = Server (20,'pi','raspberry','192.168.1.104')
#a.start()
#b.start()
#b.join()
#a.join()
#c=MyThread_GetResult('pi','raspberry','192.168.1.106')
#c.start()

        
#a = TestSendData(20,"FT",1)       








  

   

    
