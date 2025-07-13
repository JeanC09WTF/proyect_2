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
            driver.get("https://en.m.wikipedia.org")
            self.take_screenshot(driver, "mobile_home")
            
            # 2. Solución para el click interceptado
            menu_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "mw-mf-main-menu-button"))
            )
            
            # Intentar hacer scroll y click con JavaScript como alternativa
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", menu_button)
                driver.execute_script("arguments[0].click();", menu_button)
            except:
                # Si falla JavaScript, intentar click normal
                menu_button.click()
            
            # 3. Verificar menú abierto con múltiples opciones
            menu_indicators = [
                (By.LINK_TEXT, "Contents"),
                (By.CSS_SELECTOR, ".menu__container--open"),
                (By.ID, "mw-mf-page-left")
            ]
            
            for by, selector in menu_indicators:
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((by, selector))
                    )
                    self.take_screenshot(driver, "menu_opened")
                    return  # Éxito
                except:
                    continue
            
            raise Exception("No se pudo verificar la apertura del menú")
            
        except Exception as e:
            self.take_screenshot(driver, "mobile_error")
            raise e
