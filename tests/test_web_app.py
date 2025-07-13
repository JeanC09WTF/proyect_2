from .base_test import BrowserStackTest
from selenium.webdriver.common.keys import Keys
import pytest

class TestWebApp(BrowserStackTest):
    @pytest.mark.capabilities(
        browserName="Chrome",
        browserVersion="latest",
        platformName="Windows"
    )
    def test_login_flow(self, driver):
        driver.get("https://www.google.com")
        self.take_screenshot(driver, "google_home")
        assert "Google" in driver.title

    @pytest.mark.capabilities(
        browserName="Firefox",
        browserVersion="latest",
        platformName="Windows"
    )
    def test_search_feature(self, driver):
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("BrowserStack")
        search_box.send_keys(Keys.RETURN)
        self.take_screenshot(driver, "search_results")
        assert "BrowserStack" in driver.title
