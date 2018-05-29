from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select



class TestWebUi():   

    def __init__(self,test_time):
        
        self.test_time = test_time
        self.driver = webdriver.Chrome() 
        #self.driver.maximize_window()

   
    def startTest(self):
        timeout = time.time() + self.test_time
        while time.time()< timeout :
            try:
                self.driver.get('http://192.168.1.1')
                time.sleep(4)
                password = self.driver.find_element_by_id('login_password')
                password.send_keys('admin')
        
                loginButton = self.driver.find_element_by_id('login_save')
                loginButton.click()
                time.sleep(2)
            except : 
                print('invalid url or credentials')
            pass
        ################################# Administration - Mes Favoris ##################################################
        
            favorisWi= self.driver.find_element_by_id('favoritesTitle_Fav')
            favorisWi.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            
            
            
        ########################################  Réseau local########################################################## 
        
            slideWidget= self.driver.find_element_by_css_selector('[class="navarrow right"]')
            #self.driver.execute_script("arguments[0].click();",slideWidget)
            slideWidget.click()
            time.sleep(2)
            
            
            devicesListTitleWi= self.driver.find_element_by_id('devicesListTitle')
            devicesListTitleWi.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            
            internetStateTitle= self.driver.find_element_by_id('internetStateTitle')
            internetStateTitle.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            
            televisionStateStatus= self.driver.find_element_by_id('televisionStateStatus')
            televisionStateStatus.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            
            voiceAdvanced= self.driver.find_element_by_id('voiceAdvanced')
            voiceAdvanced.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            
            wifiAdvancedTitle= self.driver.find_element_by_id('wifiAdvanced')
            wifiAdvancedTitle.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            
            wifiGuest= self.driver.find_element_by_id('wifiGuest')
            wifiGuest.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            
            wifiScheduling= self.driver.find_element_by_id('wifiScheduling')
            wifiScheduling.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            
            devicesHistory= self.driver.find_element_by_id('devicesHistory')
            devicesHistory.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
        ######################################## Stockage Livebox et Cloud d'Orange ########################################################## 
            slideWidget= self.driver.find_element_by_css_selector('[class="navarrow right"]')
            slideWidget.click()
            time.sleep(2)
            
            hubState= self.driver.find_element_by_id('hubState')
            hubState.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            
            hubApps= self.driver.find_element_by_id('hubApps')
            hubApps.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            
            hubSupport= self.driver.find_element_by_id('hubSupport')
            hubSupport.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            
        ######################################## Paramètres avancés ##########################################################    
            slideWidget= self.driver.find_element_by_css_selector('[class="navarrow right"]')
            slideWidget.click()
            time.sleep(2)
            
            internetConnection= self.driver.find_element_by_id('internetConnection')
            internetConnection.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            
            internetRemote= self.driver.find_element_by_id('internetRemote')
            internetRemote.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            
            localSettings= self.driver.find_element_by_id('localSettings')
            localSettings.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            
            reseauWi= self.driver.find_element_by_id('networkAdvancedTitle')
            reseauWi.click()
            time.sleep(3)
            iframe = self.driver.find_element_by_xpath("//iframe[@id='iframeapp']")
            self.driver.switch_to.frame(iframe)
            time.sleep(3)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            try :
                selectOp = Select(self.driver.find_element_by_id('tools'))
                selectOp.select_by_index('1')
                time.sleep(3)
                addOp = self.driver.find_element_by_id('add')
                addOp.click()
                time.sleep(3)
            except:
                print("no device found")
                pass
            self.driver.back()
            time.sleep(3)
            
            networkFirewall= self.driver.find_element_by_id('networkFirewall')
            networkFirewall.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            
            systemBackup= self.driver.find_element_by_id('systemBackup')
            systemBackup.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            
            userPassword= self.driver.find_element_by_id('userPassword')
            userPassword.click()
            time.sleep(3)
            self.driver.back()
            time.sleep(3)
            try :
                self.driver.execute_script("$(window.open('http://www.google.com'))")
                time.sleep(5) 
                self.driver.current_window_handle
                self.driver.switch_to_window(self.driver.window_handles[-1])
                time.sleep(3) 

                search_box = self.driver.find_element_by_name('q')
                search_box.send_keys('livebox orange')
                assert "No results found." not in self.driver.page_source
                search_box.submit() 
                time.sleep(5)
            except:
                print("no internet connection")
                pass
            try:
                self.driver.switch_to_window(self.driver.window_handles[0])
                time.sleep(5)
                self.driver.execute_script("$(window.open('https://www.youtube.com/watch?v=H-KbosQTlKA'))")
                time.sleep(2)
                self.driver.current_window_handle
                self.driver.switch_to_window(self.driver.window_handles[-1])
                time.sleep(8)
                self.driver.switch_to_window(self.driver.window_handles[0])
                time.sleep(5)
            except:
                print("no internet connection")
                pass
                
            
            
        self.driver.close()
            
            
        
a = TestWebUi(2000)
a.startTest()