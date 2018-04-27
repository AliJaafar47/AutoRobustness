import time

from .models import Test_Result


class TestVoip():   

    # test_time : the approximative time for test , delay time : the waiting time before start the test
    def __init__(self,test_time,class_name,IDTable):
        self.class_name = class_name
        self.test_time = test_time
        self.table = Test_Result.objects.filter(test_id=IDTable)
        
    def startTest(self):
        self.table.update(state="starting test")
        timeout = time.time() + self.test_time
 
        while time.time() < timeout :
            time.sleep(3)
            self.table.update(state="testing 1")
            percentage = str((time.time() / timeout))[9:11]
            self.table.update(progress=str(percentage))
            time.sleep(3)
            self.table.update(state="testing 2")
            percentage = str((time.time() / timeout))[9:11]
            self.table.update(progress=str(percentage))
        
    def endTest(self):
        self.table.update(state="Ending test")
        self.table.update(progress=str(100))