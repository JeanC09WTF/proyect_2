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
        # ... código existente ...

    @pytest.mark.capabilities(
        browserName="Firefox",
        browserVersion="latest",
        platformName="Windows"
    )
    def test_search_feature(self, driver):
        """Prueba de función de búsqueda"""
        try:
            driver.get("https://www.google.com")
            
            # Intentar aceptar cookies
            try:
                accept_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceptar todo')]"))
                )
                accept_button.click()
            except:
                pass

            search_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "q"))
            )
            search_box.send_keys("BrowserStack" + Keys.RETURN)
            
            WebDriverWait(driver, 15).until(
                lambda d: "BrowserStack" in d.title or "browserstack" in d.page_source
            )
            self.take_screenshot(driver, "search_results")  # Ahora sí funciona
            
        except Exception as e:
            self.take_screenshot(driver, "search_error")
            raise e
