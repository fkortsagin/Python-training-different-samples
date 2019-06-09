#Imports the needed libraries and a webdriver for a specific browser
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#Opens browser in full window
driver = webdriver.Edge()
driver.get('http://www.python.org')
driver.maximize_window()
#Goes to the https://erply.com/? around 10 times
driver.get('https://erply.com/?')
for page_no in range(10):
    	driver.get('https://erply.com/?=%s' % str(page_no))
driver.quit()
driver = webdriver.Firefox()
driver.get('http://www.python.org')
driver.maximize_window()    
for page_no in range(10):
    	driver.get('https://erply.com/?=%s' % str(page_no))
driver.quit()
driver = webdriver.Chrome()
driver.get('http://www.python.org')
driver.maximize_window()
for page_no in range(10):
    	driver.get('https://erply.com/?=%s' % str(page_no))
driver.quit()
