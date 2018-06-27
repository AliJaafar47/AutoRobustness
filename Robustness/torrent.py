import os
import random
import sys
import threading
import time
import libtorrent as lt
from ssh_decorate import ssh_connect      
import threading
import time
import paramiko 
import select
from .models import Project, Step, Test_Result, Step_Result, Project_result

class P2pTest():
    def __init__(self,name,test_time):
        
        self.name = name
        self.test_time = test_time
        self.ip = '192.168.1.105'
        self.username = 'pi'
        self.password='raspberry'
        
        def download(name,test_time):
            i=1
            while True:
                print ('Trying to connect to %s (%i/2)' % (self.ip , i))
        
                try:
                    ssh2 = paramiko.SSHClient()
                    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh2.connect(self.ip , port=22, username=self.username, password=self.password)
                    print ("Connected to %s" % self.ip)
                    break
                except paramiko.AuthenticationException:
                    print ("Authentication failed when connecting to %s") % self.ip
                    sys.exit(1)
                except:
                    print ("Could not SSH to %s, waiting for it to start" % self.ip)
                    i += 1
                    time.sleep(2)
        
            # If we could not connect within time limit
                if i == 5:
                    print ("Could not connect to %s. Giving up") % self.ip
                    sys.exit(1)    
            

            stdin2, stdout2, stderr2 = ssh2.exec_command("python /home/pi/download.py "+name)
            print("Exec command 1")
            
            #block untill command is over 
            while not stdout2.channel.exit_status_ready():
        # Only print data if there is data to read in the channel
                    if stdout2.channel.recv_ready():
                        rl, wl, xl = select.select([stdout2.channel], [], [], 0.0)



        
        self.download_thread  = threading.Thread(target = download,args = (self.name,self.test_time))
        self.download_thread.start()
        

class GetResult():
    def __init__(self):
        self.dssh = paramiko.SSHClient()
        self.dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.dssh.connect('192.168.1.105', username='pi', password='raspberry')
        
    def getResult(self,name):
        stdin, stdout, stderr = self.dssh.exec_command('cat ./torrentfiles/'+name+"_report")
        ch = str(stdout.read(),"utf-8")
        return ch
    
    



class TestTorrent():
    
    def __init__(self,test_time,class_name,IDTable):
        self.number_of_files = 2
        self.class_name = class_name
        self.test_time = test_time
        self.table = IDTable
        self.table = Test_Result.objects.get(test_id=IDTable)
        self.table_one = Test_Result.objects.filter(test_id=IDTable)
        
        timeout = time.time()+ self.test_time    
        while time.time() < timeout :
            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            thread_list=[]
            
            #begin downloading
            self.table_one.update(state="Downloading")
            
            
            for i in range(1,self.number_of_files):
                percentage = str((time.time() / timeout))[9:11]
                self.table_one.update(progress=str(percentage))
                a = P2pTest("Thread"+str(i),self.test_time)
                thread_list.append(a.download_thread)
                
            [j.join() for j in thread_list]
            print("all threads are done",flush=True)
            print("Writing results")
            #Ending downloading
            self.table_one.update(state="Finish downloading")
            
            peers = 0
            result = 0
            
            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            
            throughtput_list = []
            time.sleep(10)
            for i in range (1,self.number_of_files):
                b = GetResult()
                ch = b.getResult("Thread"+str(i)) 
                if ch != "":
                    peers = peers +1 
                    result = round(float(ch)) + result
                    throughtput_list.append(str(float(ch)/1000)[0:4])
                    
            #Ending downloading       
            self.table_one.update(state="Getting results")
            try :
                result = result / peers 
            except :
                result = 0 
            result_peers = str(peers)
            
            result_throughput = str(result/1000)+" Mbit/s"
            
            metrics = self.table.metrics.all()
            
            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            
            
            for j in metrics :
                if j.name == "THROUGHPUT" :
                    j.update_values(result_throughput)
                    j.add_all_values(",".join(throughtput_list))
                if j.name == "NUMBER_OF_CONNECTION":
                    j.update_values(result_peers)
                    
                    
        self.table_one.update(state="Finished")
        self.table_one.update(progress=str(100))
                    




