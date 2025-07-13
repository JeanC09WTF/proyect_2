import pytest
from .base_test import BrowserStackTest
from selenium.webdriver.common.keys import Keys

class TestWebApp(BrowserStackTest):
    @pytest.mark.capabilities(
        browserName="Chrome",
        browserVersion="latest",
        platformName="Windows",
        platformVersion="10"
    )
    def test_login_flow(self, driver):
        driver.get("https://your-internal-app.com/login")
        
        # Flujo de login
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "password").send_keys("securepass123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        assert "Dashboard" in driver.title
        self.report_session_status(driver, "passed", "Login exitoso")

    @pytest.mark.capabilities(
        browserName="Safari",
        browserVersion="15",
        platformName="macOS",
        platformVersion="Monterey"
    )
    def test_search_feature(self, driver):
        driver.get("https://your-internal-app.com/dashboard")
        
        search_box = driver.find_element(By.NAME, "search")
        search_box.send_keys("reporte financiero")
        search_box.send_keys(Keys.RETURN)
        
        assert "reporte financiero" in driver.page_source
        self.take_screenshot(driver, "search_results")
        self.report_session_status(driver, "passed", "Búsqueda exitosa")
