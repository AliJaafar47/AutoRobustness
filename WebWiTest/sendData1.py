import sys
import time
import select
import paramiko
import os
import threading

class MyThread_Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        file = open("log.txt","w")
        file.write("")
        file.close()     
    def run(self):
        host = '192.168.1.105'
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
            if i == 2:
                print ("Could not connect to %s. Giving up") % host
                sys.exit(1)

    # Send the command (non-blocking)
        stdin, stdout, stderr = ssh.exec_command("echo $$ ; exec iperf -s -i 1")
        pid = stdout.readline()
        print(pid)
        test_time = time.time()+ 12

        while not stdout.channel.exit_status_ready() and time.time() < test_time :

    # Only print data if there is data to read in the channel
    
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)

                if len(rl) > 0:
            # Print data from stdout
                    file = open("log.txt","a")
                    ch = str(stdout.channel.recv(1024))+"\n"
                    file.write(ch)
                    file.close()     
                    print (stdout.channel.recv(1024))
# Disconnect from the host
#
        print ("Command done, closing SSH connection")
        stdin, stdout, stderr = ssh.exec_command(" sudo kill -9 "+pid )

        ssh.close()
        
      

class MyThread_Local(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        os.system("iperf -c 192.168.1.105 -i 1 ")
        

class TestSendData():
    def __init__(self,ip_dest,login,password):
        self.ip_dest= ip_dest
        self.login = login
        self.password = password
        







a = MyThread_Server()
a.start()
time.sleep(5)
b = MyThread_Local()
b.start()
a.join()
b.join()    

try:
    cfg_dict = {}
    lst = []
    cfg_file = open('log.txt','r')
    for line in cfg_file:
        if '-' and not '=' in  line:
            line = line.split()
            line.append('None')
            lst.append( line)
        else:
            line = ''.join(line.strip().split('=')).split()
            lst.append(line)
   
    for item in lst :
    
        
        print(item[7])
        
    cfg_file.close()
   
except IOError :
    print("can't open the file or file didn't exist")     

    
