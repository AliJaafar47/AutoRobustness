import paramiko
import select
import time
import sys
class CheckVoIP():
    def __init__(self):
        self.host = '192.168.1.10'
        self.username = 'pi'
        self.pwd = 'raspberry'
        #self.name = name
        #self.test_time = test_time
        print("Start Checking")   
        i = 1
        while True:
            print ('Trying to connect to %s (%i/2)' % (self.host, i))
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.host, port=22, username=self.username, password=self.pwd)
                print ("Connected to %s" % self.host)
                break
            except paramiko.AuthenticationException:
                print ("Authentication failed when connecting to %s" % self.host)
                sys.exit(1)
            except:
                print ("Could not SSH to %s, waiting for it to start" % self.host)
                i += 1
                time.sleep(2)

        # If we could not connect within time limit
            if i == 5:
                print ("Could not connect to %s. Giving up" % self.host)
                sys.exit(1)
        print("End checking")
        self.session_ssh = ssh
    def check(self):
        stdin, stdout, stderr = self.session_ssh.exec_command("sudo python /home/pi/check.py")
        while not stdout.channel.exit_status_ready():
            #if stdout.channel.recv_ready():
                #rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
            i=0
        ch = str(stdout.read(),"utf-8")
        if 'False' in ch :
            return(False)
        else :
            return (True)
    def reboot(self):
        self.session_ssh.exec_command("sudo reboot")
        print('rebooting')
        time.sleep(50)
        print('end reboot')
        self.session_ssh.close()
        
        
a = CheckVoIP()
b= a.check()
print(type(b))

if b == False :
    print("False check")



