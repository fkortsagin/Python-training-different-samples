#libraries
import unittest
from selenium import webdriver
class SimpleTestCase(unittest.TestCase):
#Open and close dp.ee page on multiple browsers simultanuasly
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.addCleanup(self.browser.quit)
        self.browser = webdriver.Edge()
        self.addCleanup(self.browser.quit)
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)
#Checking if the page title is correctly displayed in every browser
    def testPageTitle(self):
        self.browser.get('http://www.dp.ee/test.html')
        self.assertIn('Ð¿Ñ€Ð¾Ð³Ñ€Ð°Ð¼Ð¼Ð°', self.browser.title)
       
if __name__ == '__main__':
    unittest.main(verbosity=2)
