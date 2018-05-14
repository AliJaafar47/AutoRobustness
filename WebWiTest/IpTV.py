import sys
import time
import paramiko
import threading


class MyThread_mccat(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        host = '192.168.3.132'
        i = 1
        while True:
            print ('Trying to connect to %s (%i/2)' % (host, i))

            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port=22, username='pi', password='raspberry')
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
        
        
class MyThread_KillMccat(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
       
    def run(self):
        host = '192.168.3.132'
        i = 1
        while True:
            print ('Trying to connect to %s (%i/2)' % (host, i))

            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port=22, username='pi', password='raspberry')
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
        
class MyThread_GetResult(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        file = open("logTV.txt","w")
        file.write("")
        file.close()  
        
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False 
      
      
    def run(self):
        host = '192.168.3.132'
        i = 1
        while True:
            print ('Trying to connect to %s (%i/2)' % (host, i))

            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port=22, username='pi', password='raspberry')
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
            return None
        print('AVG P',round(average_packet_loss/j),' AVG BW',round(average_bw/j))  
    
            
            
class testIPTV():       
    def __init__(self,time_test):
        a = MyThread_mccat()
        a.start()
        time.sleep(time_test)
        b = MyThread_KillMccat()
        b.start()
        time.sleep(3)
        c= MyThread_GetResult()
        c.start()
        
        
a = testIPTV(10)

      
         
        
                    
                    
                    
                    

    
            

             

 
