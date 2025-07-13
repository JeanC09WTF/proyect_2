import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tests.base_test import BrowserStackTest

class TestWebApp(BrowserStackTest):
    @pytest.mark.capabilities(
        browserName="Chrome",
        browserVersion="latest",
        platformName="Windows"
    )
    def test_login_flow(self, driver):
        """Prueba de flujo de login"""
        driver.get("https://www.google.com")
        self.take_screenshot(driver, "google_home")
        assert "Google" in driver.title

    @pytest.mark.capabilities(
        browserName="Firefox",
        browserVersion="latest",
        platformName="Windows"
    )
    def test_search_feature(self, driver):
        """Prueba de función de búsqueda"""
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("BrowserStack")
        search_box.send_keys(Keys.RETURN)
        self.take_screenshot(driver, "search_results")
        assert "BrowserStack" in driver.title
