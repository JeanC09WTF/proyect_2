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
            # 1. Navegar a Wikipedia móvil
            driver.get("https://en.m.wikipedia.org")  # Usar versión en inglés
            self.take_screenshot(driver, "mobile_home")
            
            # 2. Selectores actualizados para Wikipedia en inglés
            menu_selectors = [
                (By.CSS_SELECTOR, "#mw-mf-main-menu-button"),  # Selector actual
                (By.CSS_SELECTOR, ".main-menu-button"),
                (By.XPATH, "//button[contains(@class, 'menu')]")
            ]
            
            # 3. Intentar abrir menú
            menu_found = False
            for by, selector in menu_selectors:
                try:
                    menu_button = WebDriverWait(driver, 8).until(
                        EC.element_to_be_clickable((by, selector)))
                    menu_button.click()
                    menu_found = True
                    break
                except:
                    continue
            
            if not menu_found:
                raise Exception("No se encontró el botón de menú")
            
            # 4. Verificar menú abierto
            menu_items = [
                (By.LINK_TEXT, "Contents"),
                (By.PARTIAL_LINK_TEXT, "Cont"),
                (By.CSS_SELECTOR, "#toc")
            ]
            
            for by, selector in menu_items:
                try:
                    WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((by, selector)))
                    self.take_screenshot(driver, "menu_opened")
                    return
                except:
                    continue
            
            raise Exception("Menú no mostró contenido esperado")
            
        except Exception as e:
            self.take_screenshot(driver, "mobile_error")
            raise e
