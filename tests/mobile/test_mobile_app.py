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
        """Prueba de navegación en dispositivo móvil"""
        try:
            # Navegar a Wikipedia móvil
            driver.get("https://m.wikipedia.org")
            self.take_screenshot(driver, "mobile_home")
            
            # Esperar y hacer clic en el botón de menú (selector actualizado)
            menu_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".main-menu-button, .menu-button, .mw-ui-icon"))
            )
            menu_button.click()
            
            # Verificar que el menú se despliega correctamente
            content_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Contenido"))
            )
            assert content_link.is_displayed()
            
        except Exception as e:
            self.take_screenshot(driver, "error_state")
            raise e
