from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains



class TestWebUi():   

    def __init__(self,test_time):
        
        self.test_time = test_time
        self.driver = webdriver.Chrome() 
        self.driver.maximize_window()

   
    def startTest(self):
        timeout = time.time() + self.test_time
        while time.time()< timeout :
            try:
                self.driver.get('http://192.168.3.1')
                time.sleep(2)
                element = self.driver.find_element_by_id('linkLanguages')
                hover = ActionChains(self.driver).move_to_element(element)
                hover.perform()
                time.sleep(2)
                lang = self.driver.find_element_by_xpath("/html/body/header/div/nav/ul/li[3]/div/ul/li[1]/a")
                lang.click()
                time.sleep(2)
                password = self.driver.find_element_by_css_selector('[class="userPw"]')
                password.clear()
                password.send_keys('test1234')
        
                loginButton = self.driver.find_element_by_css_selector('[class="log-button"]')
                loginButton.click()
                time.sleep(3)
            except : 
                print('invalid url or credentials')
            pass
            
            try:
                network = self.driver.find_element_by_id('viewNetwork')  
                network.click()
                time.sleep(3)
                
                networkConfig = self.driver.find_element_by_id('hmenu-advconfig')  
                networkConfig.click()
                time.sleep(2)
                
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
               
                addStaticIP = self.driver.find_element_by_id('bt_save') 
                addStaticIP.click()
                time.sleep(8)
                
                firewallTab = self.driver.find_element_by_id('left-firewall-link')
                firewallTab.click()
                time.sleep(3)
                
                userRomote = self.driver.find_element_by_id('left-remote-link')
                userRomote.click()
                time.sleep(3)
                
                internetCnx = self.driver.find_element_by_id('left-access-link')
                internetCnx.click()
                time.sleep(3)
                
                admin = self.driver.find_element_by_id('left-admin-link')
                admin.click()
                time.sleep(3)
                
                menuWifi = self.driver.find_element_by_id('hmenu-wifi')
                menuWifi.click()
                time.sleep(3)
                
                orangewifi = self.driver.find_element_by_id('orange-wifi-link')
                orangewifi.click()
                time.sleep(3)
                
                bandsteering= self.driver.find_element_by_id('band-steering')
                bandsteering.click()
                time.sleep(3)
                
                advwifi = self.driver.find_element_by_id('left-advwifi-link')
                advwifi.click()
                time.sleep(3)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                
                hmenusupport = self.driver.find_element_by_id('hmenu-support')
                hmenusupport.click()
                time.sleep(3)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                
                systemInformation = self.driver.find_element_by_id('left-information-link-pl')
                systemInformation.click()
                time.sleep(3)
                
                backup = self.driver.find_element_by_id('left-backup-link')
                backup.click()
                time.sleep(3)
                
                restore = self.driver.find_element_by_id('left-restore-link')
                restore.click()
                time.sleep(3)
                
                restart = self.driver.find_element_by_id('left-restart-link')
                restart.click()
                time.sleep(3)
                
                reset = self.driver.find_element_by_id('left-reset-link')
                reset.click()
                time.sleep(3)
                
                updatef = self.driver.find_element_by_id('left-upgrade-link')
                updatef.click()
                time.sleep(3)
                
                hostLine = self.driver.find_element_by_id('left-hotline-link')
                hostLine.click()
                time.sleep(3)
                
                try :
                    self.driver.execute_script("$(window.open('http://www.google.com'))")
                    time.sleep(5) 
                    self.driver.current_window_handle
                    self.driver.switch_to_window(self.driver.window_handles[-1])
                    time.sleep(3) 

                    search_box = self.driver.find_element_by_name('q')
                    search_box.send_keys('funbox orange 3.0')
                    assert "No results found." not in self.driver.page_source
                    search_box.submit() 
                    time.sleep(5)
                except:
                    print("no internet connection")
                    pass
                try:
                    self.driver.switch_to_window(self.driver.window_handles[0])
                    time.sleep(5)
                    self.driver.execute_script("$(window.open('https://www.youtube.com/watch?v=ksvk1mMwU84'))")
                    time.sleep(2)
                    self.driver.current_window_handle
                    self.driver.switch_to_window(self.driver.window_handles[-1])
                    time.sleep(15)
                    self.driver.switch_to_window(self.driver.window_handles[0])
                    time.sleep(5)
                except:
                    print("no internet connection")
                    pass
                
            except:
                print("invalid URL")    
                
            
            
        self.driver.close()
            
            
        
a = TestWebUi(2000)
a.startTest()