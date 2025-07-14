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
        platformName="WINDOWS"
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
        platformName="WINDOWS"
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

    # NUEVOS TESTS PARA DETECTAR DIFERENCIAS VISUALES
    @pytest.mark.capabilities(
        browserName="Safari",
        browserVersion="15",
        platformName="MAC",
        name="Test UI Differences - Safari"
    )
    def test_ui_compatibility_safari(self, driver):
        """Detecta diferencias visuales en Safari"""
        try:
            driver.get("https://www.google.com")
            self.take_screenshot(driver, "safari_ui")
            
            # Ejemplo: Verificar estilos específicos
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            font_size = search_box.value_of_css_property("font-size")
            assert font_size == "16px", f"Tamaño de fuente incorrecto en Safari: {font_size}"
            
        except Exception as e:
            self.take_screenshot(driver, "safari_ui_error")
            raise e

    @pytest.mark.capabilities(
        browserName="Chrome",
        browserVersion="latest",
        platformName="MAC",
        name="Test UI Baseline - Chrome"
    )
    def test_ui_baseline_chrome(self, driver):
        """Establece línea base visual en Chrome"""
        try:
            driver.get("https://www.google.com")
            self.take_screenshot(driver, "chrome_ui_baseline")
            
            # Mismas verificaciones que en Safari para comparar
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            font_size = search_box.value_of_css_property("font-size")
            assert font_size == "16px", f"Tamaño de fuente incorrecto en Chrome: {font_size}"
            
        except Exception as e:
            self.take_screenshot(driver, "chrome_ui_error")
            raise e
