import sys
import time
import paramiko
import threading
import select

def isDigit(x):
    try:
        float(x)
        return True
    except ValueError:
        return False
    
    
class MyThread_RecieveData(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        host = '192.168.1.104'
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
        
        
class MyThread_SendData(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
       
    def run(self):
        host = '192.168.1.106'
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
    
        stdin, stdout, stderr = ssh.exec_command("iperf -c 192.168.1.104 -i 1 q 1> data_stdout.log")
        ssh.close()
        
class MyThread_GetResult(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
       
        
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False 
      
      
    def run(self):
        host = '192.168.1.106'
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
            
        
        
           
    
            
            
class testIPTV():       
    def __init__(self):
        a = MyThread_RecieveData()
        a.start()
        b = MyThread_SendData()
        b.start()
        a.join()
        b.join()
        
        c= MyThread_GetResult()
        c.start()
        
        
        
        
#a = testIPTV()

      
         
        
                    
                    
                    
                    

    
            

             

 
