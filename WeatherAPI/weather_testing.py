import unittest

from selenium import webdriver

from selenium.webdriver.common.keys import Keys


class WeatherAppTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='/Users/matthewserna/Desktop/chromedriver')

    def test_chromedriver(self):
        driver = self
        driver.get('http://www/python.org')
        self.assertIn('Python', driver.title)
        elem = driver.find_element_by_name('q')
        elem.send_keys('pycon')
        elem.send_keys(Keys.RETURN)
        assert 'No results found' not in driver.page_source
        driver.quit()