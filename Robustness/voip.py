import time
import paramiko
import select
import os
import sys
import pyshark as p
from .models import Test_Result


class TestVoip():   

    # test_time : the approximative time for test , delay time : the waiting time before start the test
    def __init__(self,test_time,class_name,IDTable):
        self.class_name = class_name
        self.test_time = test_time
        self.table = Test_Result.objects.filter(test_id=IDTable)
        
        #object for setting metrics
        self.table_one = Test_Result.objects.get(test_id=IDTable)
        
        
    def startTest(self):
        
        timeout = time.time() + self.test_time
        
        while time.time()< timeout:
            self.table.update(state="Starting Test")
            
            #progress
            percentage = str((time.time() / timeout))[9:11]
            self.table.update(progress=str(percentage))
            
            #status of test
            self.table.update(state="Making Call")
            
            a = ReceiveCall("name",2)
            pesq_down_value =self.get_pesq()
            one_way_delay_down_value=self.get_one_way_delay_down()
            print("***************************************")
            print("PESQ DOWN:",pesq_down_value)
            print("ONE WAY DELAY DOWN: ",one_way_delay_down_value)
            print("***************************************")
            
            #progress 
            percentage = str((time.time() / timeout))[9:11]
            self.table.update(progress=str(percentage))
            
            time.sleep(10)
            
            #progress 
            percentage = str((time.time() / timeout))[9:11]
            self.table.update(progress=str(percentage))        
            
            
            b = MakeCall("name",2)
            pesq_up_value =self.get_pesq()
            one_way_delay_up_value=self.get_one_way_delay_up()
            print("***************************************")
            print("PESQ UP: ",pesq_up_value)
            print("ONE WAY DELAY UP: ",one_way_delay_up_value)
            print("***************************************")
            
            #status of test
            self.table.update(state="Ending Call")
            
            #writing results  in data base 
            metrics = self.table_one.metrics.all()
            
            for j in metrics :
                if j.name == "PESQ_UPSTREAM" :
                    j.update_values(str(pesq_up_value))
                    j.add_new_value(str(pesq_up_value))
                if j.name == "PESQ_DOWNSTREAM" :
                    j.update_values(str(pesq_down_value))
                    j.add_new_value(str(pesq_down_value))
                if j.name == "ONE_WAY_DELAY_UPSTREAM" :
                    j.update_values(str(one_way_delay_up_value)+" ms")
                    j.add_new_value(str(one_way_delay_up_value))
                if j.name == "ONE_WAY_DELAY_DOWNSTREAM" :
                    j.update_values(str(one_way_delay_down_value)+" ms")
                    j.add_new_value(str(one_way_delay_down_value))
            
            time.sleep(10)
            
            #progress 
            percentage = str((time.time() / timeout))[9:11]
            self.table.update(progress=str(percentage))   
            
            #status of test
            self.table.update(state="Making New Call")
    
    
    def get_pesq(self):
        filename="pesq_results.txt"
        pesq_file = open(filename,"r")
        lines = pesq_file.readlines()
        pesq_value = lines[-1].split()[3]
        return (pesq_value)
    
    def get_one_way_delay_down(self):
        filename="one_way_delay.txt"
        one_way_delay = open(filename,"r")
        lines = one_way_delay.readlines()
        a = lines[2:-1]
        one_way_delay_value = a[-1].split()[-1]
        return one_way_delay_value
    
    def get_one_way_delay_up(self):
        filename="one_way_delay.txt"
        one_way_delay = open(filename,"r")
        lines = one_way_delay.readlines()
        a = lines[2:-1]
        one_way_delay_value = a[0].split()[-1]
        return one_way_delay_value


    def endTest(self):
        self.table.update(state="Finished")
        self.table.update(progress=str(100))
        #self.table.update(state="Ending test")
        #self.table.update(progress=str(100))
        
class ReceiveCall():
    def __init__(self,name,test_time):

        self.name = name
        self.test_time = test_time
        print("Start")   
        host = '192.168.1.21'
        self.username = 'pi'
        self.pwd = 'raspberry'
        
        serverip = '172.16.31.10'
        server_username = "root"
        server_pwd = "sah"
        
        self.ip_DUT_wan = "172.16.30.226"
        
        
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
            if i == 5:
                print ("Could not connect to %s. Giving up") % host
                sys.exit(1)

    # Send the command (non-blocking)

        
        stdin, stdout, stderr = ssh.exec_command("sudo /home/pi/sipp/sipp -sf /home/pi/sipp/register_ameny.xml 172.16.31.10:5060 -i "+host+" -p 5060 -aa -inf /home/pi/sipp/reg_ameny.csv  -m 1")
        print("Exec command 1")
        time.sleep(1)
        stdin, stdout, stderr = ssh.exec_command("sudo /home/pi/sipp/sipp -sf /home/pi/sipp/invite_c5_g711_mgc2.xml  -i "+host+" 172.16.31.10:5060 -inf /home/pi/sipp/invite_c5_g711_ameny.csv -p 5060 -m 1 ")
        print("Exec command 2")
        while True:
            print ('Trying to connect to %s (%i/2)' % (serverip, i))
    
            try:
                ssh2 = paramiko.SSHClient()
                ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh2.connect(serverip, port=22, username=server_username, password=server_pwd)
                print ("Connected to %s" % serverip)
                break
            except paramiko.AuthenticationException:
                print ("Authentication failed when connecting to %s") % serverip
                sys.exit(1)
            except:
                print ("Could not SSH to %s, waiting for it to start" % serverip)
                i += 1
                time.sleep(2)
    
        # If we could not connect within time limit
            if i == 5:
                print ("Could not connect to %s. Giving up") % serverip
                sys.exit(1)    
        
        stdin, stdout, stderr = ssh2.exec_command("tshark -i any -f 'host "+self.ip_DUT_wan+"' -w capture_rtp.pcap -a duration:20")
        
        time.sleep(3)
        stdin2, stdout2, stderr2 = ssh.exec_command("sudo python /home/pi/test.py 12")
        print("Exec command 3")
        
        #block untill command is over 
        while not stdout2.channel.exit_status_ready():
    # Only print data if there is data to read in the channel
                if stdout.channel.recv_ready():
                    rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                    
        print("getting pcap file")
        sftp = ssh2.open_sftp()
        remotePath="/root/capture_rtp.pcap"
        localPath="/home/sah/Robustness_ReceiveCalls/capture_rtp.pcap"
        sftp.get(remotePath,localPath) 
         
        stdin, stdout, stderr = ssh.exec_command("sox -e a-law -r 8000 -b 8 --norm=-1 /home/pi/out.raw -e signed-integer -b 16 -r 8000 /home/pi/test132_16_2.raw")
        time.sleep(1)
        print("getting raw file")
        sftp = ssh.open_sftp()
        remotePath="/home/pi/test132_16_2.raw"
        localPath="/home/sah/Robustness_ReceiveCalls/out.raw"
        sftp.get(remotePath,localPath)        
        time.sleep(1)

            #stdin, stdout, stderr = ssh.exec_command("PESQ +8000  /home/pi/RTP_G711a_16.raw  /home/pi/test132_16_2.raw ")
        original = open("/home/sah/Robustness_ReceiveCalls/RTP_G711a_16.raw","rb")
        original.read(35000)
    
        original_final = open("/home/sah/Robustness_ReceiveCalls/original_final.raw","wb")
        while True :
            k = original.read()
            
            if not k :
                break
        
            original_final.write(k)
    
    
        a = open("/home/sah/Robustness_ReceiveCalls/out.raw","rb")
        b = open("/home/sah/Robustness_ReceiveCalls/final_out.raw","wb")
    
        a.read(1000)
        print("converting")
        while True :
            k = a.read()
            
            if not k :
                break
        
            b.write(k)
        print("PESQ")
    
        os.system("PESQ +8000  /home/sah/Robustness_ReceiveCalls/original_final.raw  /home/sah/Robustness_ReceiveCalls/final_out.raw ")
            #block untill command is over 
            #while not stdout.channel.exit_status_ready():
        # Only print data if there is data to read in the channel
                #if stdout.channel.recv_ready():
                    #rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                    
                        
        os.system("tshark -r /home/sah/Robustness_ReceiveCalls/capture_rtp.pcap -q -z rtp,streams > one_way_delay.txt")
        print("Done")
    
    def get_pesq_value(self,filename):
        pesq_file=open(filename,"r")
        lines = pesq_file.readlines()
        print(lines)





















class MakeCall():
    def __init__(self,name,test_time):
    #test parameters 
        host = '192.168.1.21'
        self.username = 'pi'
        self.pwd = 'raspberry'
    
        serverip = '172.16.31.10'
        server_username = "root"
        server_pwd = "sah"

        
        self.ip_DUT_wan ="172.16.30.226"


        self.name = name
        self.test_time = test_time
        print("Start")   
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
                print ("Authentication failed when connecting to %s" % host)
                sys.exit(1)
            except:
                print ("Could not SSH to %s, waiting for it to start" % host)
                i += 1
                time.sleep(2)

        # If we could not connect within time limit
            if i == 5:
                print ("Could not connect to %s. Giving up" % host)
                sys.exit(1)

        stdin, stdout, stderr = ssh.exec_command("sudo killall sipp")
        stdin, stdout, stderr = ssh.exec_command("sudo /home/pi/sipp/sipp -sf /home/pi/sipp/register_ameny_receiver.xml "+serverip+":5060 -i "+host+" -p 5060 -aa -inf /home/pi/sipp/reg_ameny_receiver.csv  -m 1")
        print("Exec command 1")
        time.sleep(1)
    
        stdin, stdout, stderr = ssh.exec_command("sudo /home/pi/sipp/sipp -sf /home/pi/sipp/receive_invite_ameny.xml  -i "+host+" -p 5060")
    
        print("Exec command 2")
        time.sleep(2)
        stdin2, stdout2, stderr2 = ssh.exec_command("sudo python /home/pi/sipp/makecall.py")
    
        print("Exec command 3")
        print("Start Capturing traffic")
    
        i=0
        while True:
            print ('Trying to connect to %s (%i/2)' % (serverip, i))
    
            try:
                ssh2 = paramiko.SSHClient()
                ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh2.connect(serverip, port=22, username=server_username, password=server_pwd)
                print ("Connected to %s" % serverip)
                break
            except paramiko.AuthenticationException:
                print ("Authentication failed when connecting to %s") % serverip
                sys.exit(1)
            except:
                print ("Could not SSH to %s, waiting for it to start" % serverip)
                i += 1
                time.sleep(2)
    
        # If we could not connect within time limit
            if i == 5:
                print ("Could not connect to %s. Giving up") % serverip
                sys.exit(1)    
        
        stdin, stdout, stderr = ssh2.exec_command("tshark -i any -f 'host "+self.ip_DUT_wan+"'  -w capture_rtp.pcap -a duration:50")
            #blockTestVoip untill command is over 
        while not stdout.channel.exit_status_ready():
            # Only print data if there is data to read in the channel
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
        print("getting file")
        sftp = ssh2.open_sftp()
        remotePath="/root/capture_rtp.pcap"
        localPath="/home/sah/Robustness_files/capture_rtp.pcap"
        sftp.get(remotePath,localPath)        
        time.sleep(1)
        stdin, stdout, stderr = ssh.exec_command("sudo killall sipp")
    
    
        os.system('python /home/sah/Robustness_files/rtp2wav2.py '+localPath+' '+self.ip_DUT_wan)
        #self.convertToraw(localPath)
        os.system("sox -e a-law -r 8000 -b 8 --norm=-1 /home/sah/Robustness_files/out.raw -e signed-integer -b 16 -r 8000 /home/sah/Robustness_files/out_16bits.raw")
    
        original = open("/home/sah/Robustness_files/out_16bits.raw","rb")
        original.read(135000)
        original_final = open("/home/sah/Robustness_files/original_final_16bit.raw","wb")
        while True :
            k = original.read()
            
            if not k :
                break
        
            original_final.write(k)
    
        print("PESQ")
        os.system("PESQ +8000  /home/sah/Robustness_files/source1_raw16.raw /home/sah/Robustness_files/original_final_16bit.raw")
        os.system("tshark -r /home/sah/Robustness_files/capture_rtp.pcap -q -z rtp,streams")
        print('test is over')

    def convertToraw(self,localPath):
        rtp_list = []
        cap = p.FileCapture(localPath,display_filter='rtp')
        raw_audio = open('/home/sah/Robustness_files/out.raw','wb')
        wav_commande = 'echo something went wrong'
        for i in cap:

            try:
                #print(i[3])
                rtp = i[3]
                if rtp.payload:
                   rtp_list.append(rtp.payload.split(":"))
            except:
                print('there is a probleme in '+str(i[3]))
                pass

            print("converting..")
            
            for rtp_packet in rtp_list:
                
                packet = " ".join(rtp_packet)
       #print(packet)
                audio = bytearray.fromhex(packet)
       #print audio
                raw_audio.write(audio)
    



        
        
#a = TestVoip(300,"FT",1)
#a.startTest()
#a.endTest()




