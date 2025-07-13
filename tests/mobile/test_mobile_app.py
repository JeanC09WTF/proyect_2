import pytest
from tests.base_test import BrowserStackTest  # Cambiado a import absoluta
from selenium.webdriver.common.by import By

class TestMobileApp(BrowserStackTest):
    @pytest.mark.capabilities(
        browserName="chrome",
        platformName="android",
        deviceName="Samsung Galaxy S22",
        osVersion="13.0",
        realMobile="true"
    )
    def test_mobile_navigation(self, driver):
        """Prueba de navegación en dispositivo móvil"""
        driver.get("https://m.wikipedia.org")
        self.take_screenshot(driver, "mobile_home")
        
        menu_button = driver.find_element(By.CSS_SELECTOR, ".main-menu-button")
        menu_button.click()
        
        assert driver.find_element(By.LINK_TEXT, "Contenido").is_displayed()
