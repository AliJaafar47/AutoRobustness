import sys
import time
import paramiko
import threading
import pwd


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
            return None
        
        
        
        
        print('AVG P',round(average_packet_loss/j),' AVG BW',round(average_bw/j))  
    
            
            
class TestIPTV2():       
    def __init__(self,time_test,class_name,IDTable):
        ip="192.168.1.10"
        username = "pi"
        pwd = "raspberry"
        
        self.test_time = time_test
        self.class_name = class_name
        self.IDTable = IDTable
        
        a = MyThread_mccat2(username,pwd,ip)
        a.start()
        time.sleep(self.test_time)
        b = MyThread_KillMccat2(username,pwd,ip)
        b.start()
        time.sleep(3)
        c= MyThread_GetResult2(username,pwd,ip,self.IDTable)
        c.start()
        
        

      
         
        
                    
                    
                    
                    

    
            

             

 
