from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.translation import activate


class TestGoogleLogin(StaticLiveServerTestCase):

    fixtures = ['allauth_fixture']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.wait = WebDriverWait(self.browser, 10)

    def tearDown(self):
        self.browser.quit()

    def get_element_by_id(self, element_id):
        return self.browser.wait.until(EC.presence_of_element_located(
            (By.ID, element_id)))

    def get_button_by_id(self, element_id):
        return self.browser.wait.until(EC.element_to_be_clickable(
            (By.ID, element_id)))

    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)

    def user_login(self):
        import json
        with open("docker_django/fixtures/google_user.json") as f:
            credentials = json.loads(f.read())
        for key, value in credentials.items():
            self.get_element_by_id(key).send_keys(value)
        for btn in ["Email", "signIn"]:
            self.get_button_by_id(btn).click()
        return

    def test_google_login(self):
        self.browser.get(self.get_full_url("home"))
        google_login = self.get_element_by_id("google_login")
        # logout not present
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("logout")
        self.assertEqual(
            google_login.get_attribute("href"),
            self.live_server_url + "/accounts/google/login")
        google_login.click()
        self.user_login()
        # login not present
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("google_login")
        google_logout = self.get_element_by_id("logout")
        google_logout.click()
        google_login = self.get_element_by_id("google_login")
