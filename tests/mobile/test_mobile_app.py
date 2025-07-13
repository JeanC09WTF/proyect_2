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
            
            # Selectores alternativos para el botón de menú
            possible_selectors = [
                (By.CSS_SELECTOR, "button.menu-toggle"),
                (By.CSS_SELECTOR, ".mw-ui-icon.mw-ui-icon-element"),
                (By.CSS_SELECTOR, ".main-menu-button"),
                (By.CSS_SELECTOR, ".menu-button")
            ]
            
            # Intentar con cada selector hasta encontrar uno que funcione
            for selector in possible_selectors:
                try:
                    menu_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(selector))
                    menu_button.click()
                    break
                except:
                    continue
            
            # Verificar contenido del menú
            content_indicators = [
                (By.LINK_TEXT, "Contenido"),
                (By.PARTIAL_LINK_TEXT, "Conten"),
                (By.CSS_SELECTOR, "#toc")
            ]
            
            for indicator in content_indicators:
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(indicator))
                    self.take_screenshot(driver, "menu_opened")
                    return  # Éxito
                except:
                    continue
            
            raise Exception("No se pudo verificar la apertura del menú")
            
        except Exception as e:
            self.take_screenshot(driver, "mobile_error")
            raise e
