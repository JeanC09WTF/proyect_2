from .base_test import BrowserStackTest
from selenium.webdriver.common.by import By

class TestWebApp(BrowserStackTest):
    @pytest.mark.capabilities(
        browserName="Chrome",
        browserVersion="latest",
        platformName="Windows"
    )
    def test_example(self, driver):
        driver.get("https://www.google.com")
        assert "Google" in driver.title
