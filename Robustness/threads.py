import threading

from  .torrent import TestTorrent
from  .voip import TestVoip
from  .webui import TestWebUi
from .sendData import TestSendData,TestSendDataFromWan
from .iptv import TestIPTV1 , TestIPTV2

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
        try :
            a.startTest()
        except : 
            print("Error in WebUI test")
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
        
        
class SendDataLanThread(threading.Thread):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, test_time,class_name,IDTable,ip_client,ip_server):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.test_time = test_time
        self.class_name = class_name
        self.IDTable = IDTable       
        self.ip_server=ip_server
        self.ip_client = ip_client
        threading.Thread.__init__(self)
        
    def run(self):
        """ Method that runs in backgroud """
        a = TestSendData(self.test_time,self.class_name,self.IDTable,self.ip_client,self.ip_server)

class SendDataWanThread(threading.Thread):
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
        a = TestSendDataFromWan(self.test_time,self.class_name,self.IDTable)




class IPTVThreadWLAN1(threading.Thread):
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
        a = TestIPTV1(self.test_time,self.class_name,self.IDTable)
        
        
class IPTVThreadWLAN2(threading.Thread):
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
        a = TestIPTV2(self.test_time,self.class_name,self.IDTable,"wlan")
        
        
class IPTVThreadLAN2(threading.Thread):
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
        a = TestIPTV2(self.test_time,self.class_name,self.IDTable,"lan")


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
                print(j)
                tableId = i.test_result.all().filter(name=j)[0].test_id
                if j == "WEBUI":
                    oneThread = WebUiThread(self.test_time,self.class_name,tableId)
                    jobs.append(oneThread)
                    
                if j == "VoIP":
                    oneThread = VoipThread(self.test_time,self.class_name,tableId)
                    jobs.append(oneThread)
                    
                if j == "P2P_WLAN_5_Ghz":
                    print("Begin Thread Torrent")
                    oneThread = TorrentThread(self.test_time,self.class_name,tableId)
                    jobs.append(oneThread)
                    
                if j == "DATA_LAN_LAN":
                    oneThread = SendDataLanThread(self.test_time,self.class_name,tableId,"192.168.1.104","192.168.1.106")
                    jobs.append(oneThread)
                    
                if j == "DATA_LAN_WLAN_2_4_Ghz":
                    oneThread = SendDataLanThread(self.test_time,self.class_name,tableId,"192.168.1.103","192.168.1.110")
                    jobs.append(oneThread)
                    
                                    
                if j == "DATA_LAN_WLAN_5_Ghz":
                    oneThread = SendDataLanThread(self.test_time,self.class_name,tableId,"192.168.1.140","192.168.1.107")
                    jobs.append(oneThread)
                    
                    
                if j == "2xIPTV_WLAN_5_Ghz":
                    oneThread = IPTVThreadWLAN2(self.test_time,self.class_name,tableId)
                    jobs.append(oneThread)
                
                if j == "1xIPTV_WLAN_5_Ghz":
                    oneThread = IPTVThreadWLAN1(self.test_time,self.class_name,tableId)
                    jobs.append(oneThread)
                
                if j == "2xIPTV_LAN":
                    oneThread = IPTVThreadLAN2(self.test_time,self.class_name,tableId)
                    jobs.append(oneThread)
                
                if j == "DATA_WAN_WLAN_5_Ghz":
                    oneThread = SendDataWanThread(self.test_time,self.class_name,tableId)
                    jobs.append(oneThread)
                    
                    
                    
            [job.start() for job in jobs ]    
            [job.join() for job in jobs]
                 

        
        
        
        
        