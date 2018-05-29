#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import string
import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .models import Test_Result


# importing the model of django app 
class TestWebUi():   

    # test_time : the approximative time for test , delay time : the waiting time before start the test
    def __init__(self,test_time,class_name,IDTable):
        self.class_name = class_name
        self.test_time = test_time
        self.table = Test_Result.objects.filter(test_id=IDTable)
        chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome() 

   
    def startTest(self):
        self.table.update(state="starting test")
        timeout = time.time() + self.test_time
        #SwissCom Class WebUI tests
        if self.class_name == "Swiss":

            while time.time() < timeout :
                def random_generator(size=6, chars=string.ascii_uppercase):
                    return ''.join(random.choice(chars) for x in range(size))
                print(random_generator())
                
                percentage = str((time.time() / timeout))[9:11]
                self.table.update(progress=str(percentage))
                
                
                self.table.update(state="Browsing Web ui test")
                try:
                    self.driver.get("http://192.168.3.1")
                    time.sleep(2)
           
                    password = self.driver.find_element_by_name('login-password')
                    password.send_keys('1234')
            
                    loginButton = self.driver.find_element_by_name('login-button')
                    loginButton.click()
                    time.sleep(5)
                except : 
                    print('invalid url or credentials')
                
                percentage = str((time.time() / timeout))[9:11]
                self.table.update(progress=str(percentage))
             
                
                speedTest = self.driver.find_element_by_css_selector('[class="speed-check text"]')
                speedTest.click()
                time.sleep(3)
            
                lunchSpeedTest = self.driver.find_element_by_css_selector('[class="button primary big no-highlighting"]')
                lunchSpeedTest.click()
                time.sleep(100)
            
                self.driver.back()
                time.sleep(3)
                
                try :
                    reseauWi = self.driver.find_element_by_css_selector('[class="navigation-item menu-network"]')
                    reseauWi.click()
                    time.sleep(3)
            
                    expertmode = self.driver.find_element_by_css_selector('[data-value="expert"]')
                    expertmode.click()
                    time.sleep(3)
        
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        
                    selectOp = self.driver.find_element_by_css_selector('[data-name="DHCPLeaseNewDevice"]')
                    selectOp.click()
                    time.sleep(3)
                    try :
                        op3 = self.driver.find_element_by_css_selector('body > div.swc-dropdown-overlay.dhcplease-device-selection.no-highlighting > ul > li:nth-child(2)')
                        op3.click()
                        time.sleep(5)
                    except:
                        print("empty device select option")
                        pass
            
                    try:
                        validButton = self.driver.find_element_by_xpath('//*[@id="current-page"]/div/ul/div/div/div[2]/div[1]/a[2]/span')
                        validButton.click()
                        time.sleep(3)
                        myWindowHandle = self.driver.current_window_handle
                        self.driver.switch_to.window(myWindowHandle)
                        time.sleep(3)
                        popup=self.driver.find_element_by_xpath('/html/body/div[5]/div/div[3]/a/span')
                        popup.click()
                        time.sleep(3)
                    except:
                        print("button hide no such configuration")
                        pass
                        
                ##urlGoogle = self.driver.get('http://www.google.com')
                    self.table.update(state="Googling")
                    self.driver.execute_script("$(window.open('http://www.google.com'))")
                    time.sleep(5) 
                    self.driver.current_window_handle
                    self.driver.switch_to_window(self.driver.window_handles[-1])
                    time.sleep(3) 
                    
                    
                    percentage = str((time.time() / timeout))[9:11]
                    self.table.update(progress=str(percentage))
                    
                    
                    search_box = self.driver.find_element_by_name('q')
                    search_box.send_keys('swisscom')
                    assert "No results found." not in self.driver.page_source
                    search_box.submit() 
                    time.sleep(5)
            
                    self.driver.switch_to_window(self.driver.window_handles[0])
                    time.sleep(5)
                    self.table.update(state="Youtube")
                    self.driver.execute_script("$(window.open('https://www.youtube.com/watch?v=nDjpGV-5rHk'))")
                    time.sleep(2)
                    self.driver.current_window_handle
                    self.driver.switch_to_window(self.driver.window_handles[-1])
                    time.sleep(8)
                    self.driver.switch_to_window(self.driver.window_handles[0])
                    time.sleep(5)
                    print (self.driver.title)
                    tabPort = self.driver.find_element_by_xpath('//*[@id="current-page"]/div/ul/li[2]/a/span')
                    tabPort.click()
                    
                    percentage = str((time.time() / timeout))[9:11]
                    self.table.update(progress=str(percentage))
        
            
            
            ##self.driver.execute_script("arguments[0].scrollIntoView();", tabPort);
                    time.sleep(3)
                    ajoutRegle = self.driver.find_element_by_xpath('//*[@id="current-page"]/div/ul/div/div/div[2]/a/span')
                    ajoutRegle.click()
                    time.sleep(3)
                    nomRegle = self.driver.find_element_by_name('serviceName')    
                    nomRegle.send_keys(random_generator())
                    time.sleep(3)
                    plagePort1 = self.driver.find_element_by_name('entryPort')    
                    plagePort1.send_keys('5001')
                    time.sleep(3)
                    
                    
                    percentage = str((time.time() / timeout))[9:11]
                    self.table.update(progress=str(percentage))
                ##plagePort2 = self.driver.find_element_by_name('destinationPort')    
                ##plagePort2.send_keys('5010')
                ##time.sleep(3)
                    selectOp1 = self.driver.find_element_by_css_selector('[data-name="deviceIP"]')
                    selectOp1.click()
                    time.sleep(5)
                except :
                    print("element not found or connexion down")
        
        #Generic Class WebUI tests
        if self.class_name == "Generic" :
            
            while time.time()< timeout :
                percentage = str((time.time() / timeout))[9:11]
                self.table.update(progress=str(percentage))
                
                
                self.table.update(state="Browsing Web ui test")
                try:
                    self.driver.get('http://192.168.1.1')
                    time.sleep(2)
                    password = self.driver.find_element_by_id('login_password')
                    password.send_keys('admin')
            
                    loginButton = self.driver.find_element_by_id('login_save')
                    loginButton.click()
                    time.sleep(2)
                except : 
                    print('invalid url or credentials')
                pass
            ################################# Administration - Mes Favoris ##################################################
            
                favorisWi= self.driver.find_element_by_id('favorites_Fav')
                favorisWi.click()
                time.sleep(3)
                self.driver.back()
                time.sleep(3) 
                
                
            ########################################  Réseau ########################################################## 
            
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
                percentage = str((time.time() / timeout))[9:11]
                self.table.update(progress=str(percentage))
                
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
                
                mysmarthome= self.driver.find_element_by_id('mysmarthome')
                mysmarthome.click()
                time.sleep(5)
                self.driver.back()
                time.sleep(3)
                percentage = str((time.time() / timeout))[9:11]
                self.table.update(progress=str(percentage))
                
                myhomemap= self.driver.find_element_by_id('myhomemap')
                myhomemap.click()
                time.sleep(3)
                iframe = self.driver.find_element_by_xpath("//iframe[@id='iframeapp']")
                self.driver.switch_to.frame(iframe)
                time.sleep(2)
                self.driver.find_element_by_css_selector('[class="logo-retour"]').click()
                time.sleep(3)
                
                speedTest= self.driver.find_element_by_id('speedTest')
                speedTest.click()
                time.sleep(3)
                iframe = self.driver.find_element_by_xpath("//iframe[@id='iframeapp']")
                self.driver.switch_to.frame(iframe)
                time.sleep(2)
                startSpeedTest=self.driver.find_element_by_id('start')
                startSpeedTest.click()
                time.sleep(5)
                self.driver.back()
                time.sleep(3)
                
                wifiSpectrum= self.driver.find_element_by_id('wifiSpectrum')
                wifiSpectrum.click()
                time.sleep(3)
                iframe = self.driver.find_element_by_xpath("//iframe[@id='iframeapp']")
                self.driver.switch_to.frame(iframe)
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                self.driver.back()
                time.sleep(3)
                
                networkTools= self.driver.find_element_by_id('networkTools')
                networkTools.click()
                time.sleep(3)
                startSpeedTest=self.driver.find_element_by_css_selector('[value="Ping"]')
                startSpeedTest.click()
                time.sleep(5)
                self.driver.find_element_by_id('app_close').click()
                percentage = str((time.time() / timeout))[9:11]
                self.table.update(progress=str(percentage))
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
                percentage = str((time.time() / timeout))[9:11]
                self.table.update(progress=str(percentage))
                
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
        
        
        
        #OPL Class WebUI tests
        if self.class_name == "OPL" :
            while time.time()< timeout :
                try:
                    self.driver.get('http://192.168.1.1')
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
                    
    
    #FT Class WebUI tests
        if self.class_name == "FT" :   
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
                    
                    
                        
                        
                
    def endTest(self):
        self.table.update(state="Finished")
        self.table.update(progress=str(100))
        self.driver.close()
        






    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    