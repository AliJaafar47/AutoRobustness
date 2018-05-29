import sys
import time
import paramiko
import threading
import pwd
from .models import Project, Step, Test_Result, Step_Result, Project_result
from builtins import str

#Class For 1 IPTV stream    

class MyThread_mccat1(threading.Thread):
    
    def __init__(self,username,pwd,ip):
        threading.Thread.__init__(self)
        self.username = username
        self.pwd = pwd
        self.ip = ip
    def run(self):
        host = self.ip
        i = 1
        while True:
            print ('Trying to connect to %s (%i/2)' % (host, i))

            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port=22, username=self.username, password=self.pwd)
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
    
        stdin, stdout, stderr = ssh.exec_command("mccat 238.1.250.1 5004 -s 1 -q 2> mccat_stdout.log")
        
        
class MyThread_KillMccat1(threading.Thread):
    
    def __init__(self,username,pwd,ip):
        threading.Thread.__init__(self)
        self.username = username
        self.pwd = pwd
        self.ip = ip
    
    def run(self):
        host = self.ip
        i = 1
        while True:
            print ('Trying to connect to %s (%i/2)' % (host, i))

            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port=22, username=self.username, password=self.pwd)
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
    
        stdin, stdout, stderr = ssh.exec_command("killall mccat")
        
class MyThread_GetResult1(threading.Thread):
    
    def __init__(self,username,pwd,ip,IDTable):
        threading.Thread.__init__(self)
        file = open("logTV.txt","w")
        file.write("")
        file.close()  
        
        #table to add result in database 
        self.table = Test_Result.objects.get(test_id=IDTable)
        
        self.username = username
        self.pwd = pwd
        self.ip = ip
        
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False 
      
      
    def run(self):
        host = self.ip
        i = 1
        while True:
            print ('Trying to connect to %s (%i/2)' % (host, i))

            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port=22, username=self.username, password=self.pwd)
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
    
        stdin, stdout, stderr = ssh.exec_command("cat mccat_stdout.log")  
        stdin.close()
        for line in stdout.read().splitlines():
            print(line.decode("ascii"))
            out= line.decode("ascii")+"\n"
            file = open("logTV.txt","a")
            file.write(out)
            file.close() 
            
        a = open("logTV.txt","r")
        average_packet_loss = 0
        average_bw = 0
        j = 0
        
        for i in a.readlines():
            #print(i.split(" "))
            try :
                
                if self.is_number(i.split(" ")[4]):
                    j = j+1
                    print(i.split(" ")[4])
                    average_packet_loss = int(i.split(" ")[4]) + average_packet_loss
                    
                if self.is_number(i.split(" ")[-1]) :
                    print(i.split(" ")[-1])
                    average_bw = float(i.split(" ")[-1]) + average_bw
                    
            except :
                pass 
            
            
        if j==0 :
           packet_loss = str(0)
           throughput == str(0)
            
        else :    
            throughput = str(round(average_bw/(j*1000)))
            packet_loss  = str(round(average_packet_loss/(j*1000)))
        
        metrics = self.table.metrics.all()
        
        
        for j in metrics :
            if j.name == "THROUGHPUT" :
                j.update_values(throughput+"Mbit/s")
                j.add_new_value(throughput)
            if j.name == "PACKET_LOSS":
                j.update_values(packet_loss)
                j.add_new_value(packet_loss)
                
        #print('AVG P',round(average_packet_loss/j),' AVG BW',round(average_bw/j))  
    
            
            
class TestIPTV1():       
    def __init__(self,time_test,class_name,IDTable):
        ip="192.168.1.10"
        username = "pi"
        pwd = "raspberry"
        
        
        self.test_time = time_test
        self.class_name = class_name
        self.IDTable = IDTable
        self.iptv_time = 10
        timeout= time.time()+self.test_time
        
        #table to update progress
        self.table_one = Test_Result.objects.filter(test_id=IDTable)
        
        
        while time.time() < timeout :
            #update ressult 1
            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            self.table_one.update(state="Begin IPTV test")
            
            a = MyThread_mccat1(username,pwd,ip)
            a.start()
            time.sleep(self.iptv_time)
            
            #update ressult 2
            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            self.table_one.update(state="Begin IPTV Stream")
            
            
            b = MyThread_KillMccat1(username,pwd,ip)
            b.start()
            time.sleep(2)
            #update ressult 3
            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            self.table_one.update(state="End IPTV Stream")
            
            time.sleep(2)
            c= MyThread_GetResult1(username,pwd,ip,self.IDTable)
            c.start()
            
            #update ressult 4
            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            self.table_one.update(state="Getting results")
            
            
            time.sleep(2)
        
        
        self.table_one.update(state="Finished")
        self.table_one.update(progress=str(100))
     
#Class For 2 IPTV stream      
        
        
class MyThread_mccat2(threading.Thread):
    
    def __init__(self,username,pwd,ip):
        threading.Thread.__init__(self)
        self.username = username
        self.pwd = pwd
        self.ip = ip
    def run(self):
        host = self.ip
        i = 1
        while True:
            print ('Trying to connect to %s (%i/2)' % (host, i))

            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port=22, username=self.username, password=self.pwd)
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
    
        stdin, stdout, stderr = ssh.exec_command("mccat 238.1.250.1 5004 -s 1 -q 2> mccat_stdout1.log")
        stdin, stdout, stderr = ssh.exec_command("mccat 238.1.250.2 5004 -s 1 -q 2> mccat_stdout2.log")
        
class MyThread_KillMccat2(threading.Thread):
    
    def __init__(self,username,pwd,ip):
        threading.Thread.__init__(self)
        self.username = username
        self.pwd = pwd
        self.ip = ip
    
    def run(self):
        host = self.ip
        i = 1
        while True:
            print ('Trying to connect to %s (%i/2)' % (host, i))

            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port=22, username=self.username, password=self.pwd)
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
    
        stdin, stdout, stderr = ssh.exec_command("killall mccat")
        
class MyThread_GetResult2(threading.Thread):
    
    def __init__(self,username,pwd,ip,IDTable):
        threading.Thread.__init__(self)
        file = open("logTV.txt","w")
        file.write("")
        file.close()  
        
        #table to add result in database 
        self.table = Test_Result.objects.get(test_id=IDTable)
                
        
        
        self.username = username
        self.pwd = pwd
        self.ip = ip
        
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False 
      
      
    def run(self):
        host = self.ip
        i = 1
        while True:
            print ('Trying to connect to %s (%i/2)' % (host, i))

            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port=22, username=self.username, password=self.pwd)
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
    
        stdin2, stdout2, stderr2 = ssh.exec_command("cat mccat_stdout2.log")  
        
        stdin1, stdout1, stderr1 = ssh.exec_command("cat mccat_stdout1.log")
        
        for line in stdout1.read().splitlines():
            print(line.decode("ascii"))
            out= line.decode("ascii")+"\n"
            file = open("logTV1.txt","w")
            file.write(out)
            file.close() 
        
        for line in stdout2.read().splitlines():
            print(line.decode("ascii"))
            out= line.decode("ascii")+"\n"
            file = open("logTV2.txt","w")
            file.write(out)
            file.close()
        
        
            
        a1 = open("logTV1.txt","r")
        a2 = open("logTV2.txt","r")
        
        average_packet_loss = 0
        average_bw = 0
        j = 0
        
        
        for i in a1.readlines():
            #print(i.split(" "))
            try :
                
                if self.is_number(i.split(" ")[4]):
                    j = j+1
                    print(i.split(" ")[4])
                    average_packet_loss = int(i.split(" ")[4]) + average_packet_loss
                    
                if self.is_number(i.split(" ")[-1]) :
                    print(i.split(" ")[-1])
                    average_bw = float(i.split(" ")[-1]) + average_bw
                    
            except :
                pass 
        if j==0 :
            return None
        
        
        for i in a2.readlines():
            #print(i.split(" "))
            try :
                
                if self.is_number(i.split(" ")[4]):
                    j = j+1
                    print(i.split(" ")[4])
                    average_packet_loss = int(i.split(" ")[4]) + average_packet_loss
                    
                if self.is_number(i.split(" ")[-1]) :
                    print(i.split(" ")[-1])
                    average_bw = float(i.split(" ")[-1]) + average_bw
                    
            except :
                pass 
        if j==0 :
           packet_loss = str(0)
           throughput == str(0)
            
        else :    
            throughput = str(round(average_bw/(j*1000)))
            packet_loss  = str(round(average_packet_loss/(j*1000)))
        
        metrics = self.table.metrics.all()
        
        for j in metrics :
            if j.name == "THROUGHPUT" :
                j.update_values(throughput+"Mbit/s")
                j.add_new_value(throughput)
            if j.name == "PACKET_LOSS":
                j.update_values(packet_loss)
                j.add_new_value(packet_loss)
        
        
        #print('AVG P',round(average_packet_loss/j),' AVG BW',round(average_bw/j))  
    
            
            
class TestIPTV2():       
    def __init__(self,time_test,class_name,IDTable,test_type):
        ip="192.168.1.10"
        username = "pi"
        pwd = "raspberry"
        
        self.test_type = test_type
        self.test_time = time_test
        self.class_name = class_name
        self.IDTable = IDTable
        self.iptv_time = 10
        timeout= time.time()+self.test_time
        
        #table to update progress
        self.table_one = Test_Result.objects.filter(test_id=IDTable)
        
        
        while time.time() < timeout :
            #update ressult 1
            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            self.table_one.update(state="Begin IPTV test")
            
            a = MyThread_mccat2(username,pwd,ip)
            a.start()
            time.sleep(self.iptv_time)
            
            #update ressult 2
            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            self.table_one.update(state="Begin IPTV Stream")
            
            
            b = MyThread_KillMccat2(username,pwd,ip)
            b.start()
            time.sleep(2)
            #update ressult 3
            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            self.table_one.update(state="End IPTV Stream")
            
            time.sleep(2)
            c= MyThread_GetResult2(username,pwd,ip,self.IDTable)
            c.start()
            
            #update ressult 4
            percentage = str((time.time() / timeout))[9:11]
            self.table_one.update(progress=str(percentage))
            self.table_one.update(state="Getting results")
            
            
            time.sleep(2)
        
        
        self.table_one.update(state="Finished")
        self.table_one.update(progress=str(100))
            
        
        

#a = TestIPTV2(10,"FT",1)


#a = TestIPTV1(30,"FT",1)
         
        
                    
                    
                    
                    

    
            

             

 
