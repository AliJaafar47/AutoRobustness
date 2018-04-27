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

        while time.time() < timeout :
            def random_generator(size=6, chars=string.ascii_uppercase):
                return ''.join(random.choice(chars) for x in range(size))
            print(random_generator())
            
            percentage = str((time.time() / timeout))[9:11]
            self.table.update(progress=str(percentage))
            
            """
            try:
                cfg_dict = {}
                lst = []
                cfg_file = open('ConfigFile','r')
                for line in cfg_file:
                    if '-' and not '=' in  line:
                        line = line.split()
                        line.append('None')
                        lst.append( line)
                    else:
                        line = ''.join(line.strip().split('=')).split()
                        lst.append(line)
                cfg_file.close()
                for item in lst:
                    cfg_dict[item[0]] = item[1]
                print(cfg_dict['url'])
                print(cfg_dict['pass'])
                v1 = cfg_dict['url']
                v2 = cfg_dict['pass']
    
   
            except IOError :
                print("can't open the file or file didn't exist")  
            """   
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
         
            '''
            speedTest = self.driver.find_element_by_css_selector('[class="speed-check text"]')
            speedTest.click()
            time.sleep(3)
        
            lunchSpeedTest = self.driver.find_element_by_css_selector('[class="button primary big no-highlighting"]')
            lunchSpeedTest.click()
            time.sleep(100)
        
            self.driver.back()
            time.sleep(3)
            '''
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
                op3 = self.driver.find_element_by_css_selector('body > div.swc-dropdown-overlay.dhcplease-device-selection.no-highlighting > ul > li:nth-child(2)')
                op3.click()
                time.sleep(5)
        ##self.driver.execute_script("document.getElementByName('DHCPLeaseIPAddress')[1].style.top = 0;")
        ##time.sleep(3)
        
                validButton = self.driver.find_element_by_xpath('//*[@id="current-page"]/div/ul/div/div/div[2]/div[1]/a[2]/span')
                validButton.click()
                time.sleep(3)
                myWindowHandle = self.driver.current_window_handle
                self.driver.switch_to.window(myWindowHandle)
                time.sleep(3)
                popup=self.driver.find_element_by_xpath('/html/body/div[5]/div/div[3]/a/span')
                popup.click()
                time.sleep(3)
            ##self.driver.back()
            ##time.sleep(3)"""
        
        
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
                
    def endTest(self):
        self.table.update(state="Ending test")
        self.table.update(progress=str(100))
        self.driver.close()
        






    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    