import threading

from  .torrent import TestTorrent
from  .voip import TestVoip
from  .webui import TestWebUi


class WebUiThread(threading.Thread):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, test_time,class_name,IDTable):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.test_time = test_time
        self.class_name = class_name
        self.IDTable = IDTable        
        threading.Thread.__init__(self)
        
    def run(self):
        """ Method that runs in backgroud """
        a = TestWebUi(self.test_time,self.class_name,self.IDTable)
        a.startTest()
        a.endTest()
        
        
class VoipThread(threading.Thread):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, test_time,class_name,IDTable):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.test_time = test_time
        self.class_name = class_name
        self.IDTable = IDTable        
        threading.Thread.__init__(self)
        
    def run(self):
        """ Method that runs in backgroud """
        a = TestVoip(self.test_time,self.class_name,self.IDTable)
        a.startTest()
        a.endTest()
        
class TorrentThread(threading.Thread):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, test_time,class_name,IDTable):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.test_time = test_time
        self.class_name = class_name
        self.IDTable = IDTable        
        threading.Thread.__init__(self)
        
    def run(self):
        """ Method that runs in backgroud """
        a = TestTorrent(self.test_time,self.class_name,self.IDTable)



class Synchronize_Steps(object):
    
    def __init__(self, steps,test_time,class_name):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.test_time= test_time
        self.steps = steps  
        self.class_name= class_name    
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()  
        
    def run(self):
        """ Method that runs in backgroud """
        for i in  self.steps :
            tests = i.description.split(',')
            jobs = []
            for j in tests :
                tableId = i.test_result.all().filter(name=j)[0].test_id
                if j == "WEBUI":
                    oneThread = WebUiThread(self.test_time,self.class_name,tableId)
                    jobs.append(oneThread)
                if j == "VOIP_TEST":
                    oneThread = VoipThread(self.test_time,self.class_name,tableId)
                    jobs.append(oneThread)

                    
                    
                    
            [job.start() for job in jobs ]    
            [job.join() for job in jobs]
                 

        
        
        
        
        