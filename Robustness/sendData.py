import sys
import time
import select
import paramiko
import os
import threading
from ssh_decorate import ssh_connect   
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
        test_time = time.time()+ self.test_time

        while not stdout.channel.exit_status_ready() and time.time() < test_time :

    # Only print data if there is data to read in the channel
    
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)

                if len(rl) > 0:
            # Print data from stdout
                    file = open("log.txt","a")
                    ch = str(stdout.channel.recv(1024),"utf-8")+"\n"
                    file.write(ch)
                    file.close()     
                    print (stdout.channel.recv(1024))
# Disconnect from the host
#
        print ("Command done, closing SSH connection")
        stdin, stdout, stderr = ssh.exec_command(" sudo kill -9 "+pid )

        ssh.close()
        
      

class Client(threading.Thread):
    def __init__(self,test_time,client_username,client_pwd,ip_client,ip_server):
        threading.Thread.__init__(self)
        self.test_time=test_time
        ssh=ssh_connect(client_username,client_pwd,ip_client)
        ip_server = ip_server
        @ssh
        def iperf_command(test_time,ip_server):
            import os
            
            os.system("iperf -c "+str(ip_server)+" -i 1 -t "+str(test_time))
            
        iperf_command(test_time,ip_server)
        
    def run(self):
        print("")
        
        

class TestSendData():
    def __init__(self,test_time,class_name,IDTable):
        
        #setting tables 
        self.table = Test_Result.objects.get(test_id=IDTable)
        self.table_one = Test_Result.objects.filter(test_id=IDTable)
        
        self.test_time= test_time
        self.class_name = class_name
        self.IDTable = IDTable
        self.iperf_time = 20
        timeout = time.time() + self.test_time
            
        while time.time() < timeout :
            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            
            a = Server(self.iperf_time,"pi","raspberry","192.168.1.21")
            a.start()
            self.table_one.update(state="Connected to Distant Host")
            time.sleep(2)
            self.table_one.update(state="Sending Data")
            b = Client(self.iperf_time,"pi","raspberry","192.168.1.21","192.168.1.28")
            
            time.sleep(2)
            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            
            b.start()
            a.join()
            b.join() 
            
            #writing results  in data base 
            metrics = self.table.metrics.all()
            
            for j in metrics :
                if j.name == "THROUGHPUT" :
                    j.update_values(str(self.get_result())+" Mbit/s")
                    j.add_new_value(str(self.get_result()))

            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            
        
        
        self.table_one.update(state="Finished")
        self.table_one.update(progress=str(100))
        
    def get_result(self):
        try:
            lst = []
            cfg_file = open('log.txt','r')
            
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
        
    
        
#a = TestSendData(20,"FT",1)       








  

   

    
