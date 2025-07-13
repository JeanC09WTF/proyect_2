import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.base_test import BrowserStackTest
import time

class TestWebApp(BrowserStackTest):
    @pytest.mark.capabilities(
        browserName="Chrome",
        browserVersion="latest",
        platformName="Windows"
    )
    def test_login_flow(self, driver):
        """Prueba de flujo de login"""
        driver.get("https://www.google.com")
        self.take_screenshot(driver, "google_home")
        assert "Google" in driver.title

    @pytest.mark.capabilities(
        browserName="Firefox",
        browserVersion="latest",
        platformName="Windows"
    )
    def test_search_feature(self, driver):
        """Prueba de función de búsqueda"""
        try:
            # 1. Navegar a Google
            driver.get("https://www.google.com")
            
            # 2. Realizar búsqueda
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            search_box.send_keys("BrowserStack")
            search_box.send_keys(Keys.RETURN)
            
            # 3. Esperar resultados y verificar
            WebDriverWait(driver, 10).until(
                lambda d: "BrowserStack" in d.title.lower() or "browserstack" in d.page_source.lower())
            
            self.take_screenshot(driver, "search_results")
            
            # Verificación más robusta
            assert any([
                "BrowserStack" in driver.title,
                "browserstack" in driver.title.lower(),
                "BrowserStack" in driver.page_source
            ]), "No se encontró 'BrowserStack' en la página de resultados"
            
        except Exception as e:
            self.take_screenshot(driver, "search_error")
            raise e
