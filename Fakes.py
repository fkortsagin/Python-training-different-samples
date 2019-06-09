#Imports the needed libraries and a webdriver for a specific browser
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from faker import Faker
#dummy data
fake = Faker()
#Results output file
f = open('TestResults.txt','w+')
#Open Edge browser in full window
driver = webdriver.Edge()
driver.get('http://www.python.org')
driver.maximize_window()
#Goes to the http://www.dp.ee/test.html page
driver.get('http://www.dp.ee/test.html')
#Fills the form with the details required
field = driver.find_element_by_id('name')
field.send_keys(fake.name())
field = driver.find_element_by_id('email')
field.send_keys(fake.email())
field = driver.find_element_by_id ('date-of-birth')
field.send_keys(fake.date())
driver.find_element_by_id('button').click()
elems = driver.find_elements_by_id('name')
if len(elems) > 0 and elems[0].is_displayed():
    print ('Passed',file =f)
else: 
    print ('Failed',file=f)
# close the browser window after making it wait for 5 secs
time.sleep(5)

f.close()
