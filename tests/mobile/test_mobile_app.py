import pytest
from ..base_test import BrowserStackTest

class TestMobileApp(BrowserStackTest):
    @pytest.mark.capabilities(
        browserName="chrome",
        platformName="android",
        deviceName="Samsung Galaxy S22",
        osVersion="13.0",
        realMobile="true"
    )
    def test_mobile_navigation(self, driver):
        driver.get("https://the-internet.herokuapp.com/login")
        
        menu_button = driver.find_element(By.CSS_SELECTOR, ".mobile-menu")
        menu_button.click()
        
        assert driver.find_element(By.LINK_TEXT, "Configuración").is_displayed()
        self.report_session_status(driver, "passed", "Navegación móvil exitosa")
