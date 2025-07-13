import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.base_test import BrowserStackTest

class TestWebApp(BrowserStackTest):
    @pytest.mark.capabilities(
        browserName="Chrome",
        browserVersion="latest",
        platformName="Windows"
    )
    def test_login_flow(self, driver):
        try:
            driver.get("https://www.google.com")
            WebDriverWait(driver, 10).until(
                lambda d: "Google" in d.title
            )
            self.take_screenshot(driver, "google_home")
        except Exception as e:
            self.take_screenshot(driver, "login_error")
            raise e

    @pytest.mark.capabilities(
        browserName="Firefox",
        browserVersion="latest",
        platformName="Windows"
    )
    def test_search_feature(self, driver):
        """Prueba de función de búsqueda"""
        try:
            # 1. Navegar a Google y aceptar cookies si existe
            driver.get("https://www.google.com")
            
            # Intentar aceptar cookies (si aparece)
            try:
                accept_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceptar todo') or contains(., 'Aceptar') or contains(., 'Acepto')]"))
                )
                accept_button.click()
            except:
                pass  # Si no aparece el modal, continuar
            
            # 2. Esperar y realizar búsqueda
            search_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "q"))
            )
            search_box.clear()
            search_box.send_keys("BrowserStack")
            search_box.send_keys(Keys.RETURN)
            
            # 3. Verificar resultados con múltiples condiciones
            WebDriverWait(driver, 15).until(
                lambda d: any([
                    "BrowserStack" in d.title,
                    "browserstack" in d.title.lower(),
                    "BrowserStack" in d.page_source,
                    len(d.find_elements(By.PARTIAL_LINK_TEXT, "BrowserStack")) > 0
                ])
            )
            self.take_screenshot(driver, "search_results")
            
        except Exception as e:
            self.take_screenshot(driver, "search_error")
            raise e
