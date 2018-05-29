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
from .models import Project, Step, Test_Result, Step_Result, Project_result

class P2pTest():
    def __init__(self,name,test_time):
        ssh=ssh_connect('pi','raspberry','192.168.1.105')
        self.name = name
        self.test_time = test_time
        @ssh
        def download(name,test_time):
            import libtorrent as lt
            import time
            import sys
            import random
            import os
            ses = lt.session()
            port1 = random.randint(6000, 65535 )
            port2 = random.randint(5000, 65535 ) 
            ses.listen_on(port1, port2)
            #ses.listen_on(sport, dport)
            info = lt.torrent_info("./torrentfiles/"+name+".torrent")
            #h = ses.add_torrent({'ti': info, 'save_path': threadName})
            h = ses.add_torrent({'ti': lt.torrent_info("./torrentfiles/"+name+".torrent"), 'save_path': './torrentfiles/', 'seed_mode': False}) 
            print ('starting', h.name())
            s = h.status()
            down_rate =[]
            i = 0
      
            timeout = time.time() + test_time
      
            while s.progress * 100  < 100 : 
                s = h.status()
                state_str = ['queued', 'checking', 'downloading metadata', \
                     'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']

                if time.time() > timeout :
                    break
                
                
                if ( s.download_rate / 1000 ) > 0 :
                # TODO : append in  data base and add one peer             
                    down_rate.append(int(s.download_rate / 1000))
            
            
            
            os.system("rm ./torrentfiles/"+name)
            try :
                print(h.name(), 'complete *** average download_rate : ',sum(down_rate) / float(len(down_rate)))
                report_file = open("./torrentfiles/"+name+"_report","w")   
                report_file.write(str(sum(down_rate) / float(len(down_rate))))
                report_file.close()
                
            except Exception as e :
                report_file = open("./torrentfiles/"+name+"error","w") 
                report_file.write(str(e))
                report_file.close()
                return 0

        
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
        self.number_of_files = 3
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
                    




