import os
from django.test import LiveServerTestCase
from django.test import tag
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSelenium(LiveServerTestCase):

    @tag('selenium')
    def setUp(self):
        self.selenium = webdriver.Firefox()

    @tag('selenium')
    def test_registration(self):
        ''' tests registration with selenium'''
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/signup/')
        username = selenium.find_element_by_id('id_username')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        submit = selenium.find_element_by_name('submit')
        username.send_keys('friha')
        password1.send_keys('Somepassword')
        password2.send_keys('Somepassword')
        submit.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "logout"))
        )
        self.assertTrue(self.selenium.find_element_by_id("logout"))

    @tag('selenium')
    def test_login(self):
        ''' tests login with selenium'''
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

    @tag('selenium')
    def test_selenium_save(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000')
        query = selenium.find_element_by_name("query")
        query.send_keys('coca')
        query.send_keys(Keys.RETURN)
        save = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "save"))
        )
        save.send_keys(Keys.RETURN)

    @tag('selenium')
    def test_selenium_remove(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/preferences')
        element = WebDriverWait(selenium, 20).until(
            EC.presence_of_element_located((By.ID, "remove"))
        )
        element.send_keys(Keys.RETURN)
