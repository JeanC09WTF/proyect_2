import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.base_test import BrowserStackTest

class TestWebApp(BrowserStackTest):
    @pytest.mark.capabilities(
        browserName="Chrome",
        browserVersion="latest",
        platformName="Windows"
    )
    def test_login_flow(self, driver):
        """Prueba de flujo de login"""
        try:
            driver.get("https://www.google.com")
            self.take_screenshot(driver, "google_home")
            assert "Google" in driver.title
        except Exception as e:
            self.take_screenshot(driver, "login_error")
            raise e

    @pytest.mark.capabilities(
        browserName="Firefox",
        browserVersion="latest",
        platformName="Windows"
    )
    def test_search_feature(self, driver):
        """Prueba de función de búsqueda"""
        try:
            driver.get("https://www.google.com")
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            search_box.send_keys("BrowserStack")
            search_box.send_keys(Keys.RETURN)
            
            WebDriverWait(driver, 10).until(
                lambda d: "BrowserStack" in d.title.lower() or 
                         "browserstack" in d.page_source.lower())
            
            self.take_screenshot(driver, "search_results")
            assert any([
                "BrowserStack" in driver.title,
                "browserstack" in driver.title.lower(),
                "BrowserStack" in driver.page_source
            ])
        except Exception as e:
            self.take_screenshot(driver, "search_error")
            raise e
