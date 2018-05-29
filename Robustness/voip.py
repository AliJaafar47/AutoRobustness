import time
from ssh_decorate import ssh_connect      
#from .models import Test_Result


class TestVoip():   

    # test_time : the approximative time for test , delay time : the waiting time before start the test
    def __init__(self,test_time,class_name,IDTable):
        self.class_name = class_name
        self.test_time = test_time
        #self.table = Test_Result.objects.filter(test_id=IDTable)
        
    def startTest(self):
        #self.table.update(state="starting test")
        timeout = time.time() + self.test_time
 
        #while time.time() < timeout :

        a = Call("name",2)
        #self.table.update(state="testing 1")
            #percentage = str((time.time() / timeout))[9:11]
            #self.table.update(progress=str(percentage))
            #time.sleep(3)
            #self.table.update(state="testing 2")
            #percentage = str((time.time() / timeout))[9:11]
            #self.table.update(progress=str(percentage))
        
    def endTest(self):
        print("End")
        #self.table.update(state="Ending test")
        #self.table.update(progress=str(100))
        
class Call():
    def __init__(self,name,test_time):
        ssh=ssh_connect('pi','raspberry','192.168.1.23')
        self.name = name
        self.test_time = test_time
        
        @ssh
        def makecall():
            import os
            import time
            os.popen("sudo /home/pi/sipp/sipp -sf /home/pi/sipp/register_ameny.xml 172.16.31.10:5060 -i 192.168.1.23 -p 5060 -aa -inf /home/pi/sipp/reg_ameny.csv  -m 1")       
            time.sleep(1)
            os.popen("sudo /home/pi/sipp/sipp -sf /home/pi/sipp/invite_c5_g711_mgc2.xml  -i 192.168.1.23 172.16.31.10:5060 -inf /home/pi/sipp/invite_c5_g711_ameny.csv -p 5060 -m 1 ")
            
        makecall()
        print("Done")

        
#a = TestVoip(60,"FT",1)
#a.startTest()
#a.endTest()