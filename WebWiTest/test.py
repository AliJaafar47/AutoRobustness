from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
browser = webdriver.Chrome(chrome_options=options)
browser.get('https://www.google.com')