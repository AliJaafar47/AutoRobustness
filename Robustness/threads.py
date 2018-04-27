import threading

from  .webui import TestWebUi


class WebUiThread(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, test_time,delay_time,class_name,IDTable):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.test_time = test_time
        self.delay_time = delay_time
        self.class_name = class_name
        self.IDTable = IDTable
        

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs in backgroud """
        a = TestWebUi(self.test_time,self.delay_time,self.class_name,self.IDTable)
        a.startTest()
        a.endTest()

