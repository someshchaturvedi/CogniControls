from .base import FunctionalTest
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Congizance-Controls', self.browser.title)
