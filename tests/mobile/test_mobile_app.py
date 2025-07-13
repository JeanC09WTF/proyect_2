import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.base_test import BrowserStackTest

class TestMobileApp(BrowserStackTest):
    @pytest.mark.capabilities(
        browserName="chrome",
        platformName="android",
        deviceName="Samsung Galaxy S22",
        osVersion="13.0",
        realMobile="true"
    )
    def test_mobile_navigation(self, driver):
        try:
            driver.get("https://en.m.wikipedia.org")
            self.take_screenshot(driver, "mobile_home")
            
            menu_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "mw-mf-main-menu-button"))
            )
            menu_button.click()
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Contents"))
            )
            self.take_screenshot(driver, "menu_opened")
        except Exception as e:
            self.take_screenshot(driver, "mobile_error")
            raise e
