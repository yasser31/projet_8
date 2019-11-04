import os
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSelenium(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()

    def test_registration(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/signup/')
        username = selenium.find_element_by_id('id_username')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        submit = selenium.find_element_by_name('submit')
        username.send_keys('Yasser')
        password1.send_keys('Somepassword')
        password2.send_keys('Somepassword')
        submit.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "logout"))
        )
        self.assertTrue(self.selenium.find_element_by_id("logout"))

    def test_login(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/accounts/login')
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_name('login')
        username.send_keys(os.environ['user'])
        password.send_keys(os.environ['password'])
        submit.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "logout"))
        )
        self.assertTrue(self.selenium.find_element_by_id("logout"))

    def test_save(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/search?query=pizzas')
        save = selenium.find_element_by_name('save')
        save.click()
    
    def test_delete(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        save = selenium.find_element_by_name('save')
        save.click()
