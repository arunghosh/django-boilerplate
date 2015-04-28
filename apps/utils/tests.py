from urlparse import urljoin

from django.test import TestCase
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Create your tests here.


class SeleniumTestCase(TestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        super(SeleniumTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(SeleniumTestCase, self).tearDown()

    def get_absolute_url(self, path=''):
        return urljoin(settings.BASE_URL, path)

    def login(self, email='', password=''):
        login_page = self.selenium.get(self.get_absolute_url('/login/'))
        self.selenium.find_element_by_id("id_email").send_keys(email)
        self.selenium.find_element_by_id("id_password").send_keys(password)
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

    def by_id(self, text):
        return self.selenium.find_element_by_id(text)

    def by_xpath(self, xpath, many=False):
        if many:
            return self.selenium.find_elements_by_xpath(xpath)
        return self.selenium.find_element_by_xpath(xpath)

    def by_link_text(self, link_text, many=False):
        if many:
            return self.selenium.find_elements_by_link_text(link_text)
        return self.selenium.find_element_by_link_text(link_text)

    def by_class_name(self, class_name, many=False):
        if many:
            return self.selenium.find_elements_by_class_name(class_name)
        return self.selenium.find_element_by_class_name(class_name)

    def by_tag_name(self, tag_name, many=False):
        if many:
            return self.selenium.find_elements_by_tag_name(tag_name)
        return self.selenium.find_element_by_tag_name(tag_name)
