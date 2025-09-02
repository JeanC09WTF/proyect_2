import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.base_test import BrowserStackTest

class TestMobileApp(BrowserStackTest):

    @pytest.mark.capabilities(
        browserName="Chrome",
        platformName="Android",
        deviceName="Samsung Galaxy S23",
        platformVersion="13.0",
        realMobile=True,
        name="Test Navegación Infosgroup en Android"
    )
    def test_infosgroup_mobile_navigation(self, driver):
        """Prueba extendida en Android: Buscar Infosgroup y navegar por botones"""
        try:
            # 1. Entrar a Google
            driver.get("https://www.google.com")

            # Aceptar cookies si aparece
            try:
                accept_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(., 'Aceptar') or contains(., 'Acepto')]")
                    )
                )
                accept_button.click()
            except:
                pass

            # 2. Buscar Infosgroup Panamá
            search_box = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.NAME, "q"))
            )
            search_box.send_keys("Infosgroup Panamá")
            search_box.send_keys(Keys.RETURN)

            # 3. Clic en el primer resultado de Infosgroup
            infosgroup_link = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Infosgroup"))
            )
            infosgroup_link.click()

            # 4. Esperar a que cargue la página de Infosgroup
            WebDriverWait(driver, 20).until(
                lambda d: "Infosgroup" in d.title or "InfosGroup" in d.page_source
            )
            self.take_screenshot(driver, "infosgroup_mobile_home")

            # 5. Navegar por el menú principal (versión móvil)
            menu_items = [
                "//a[contains(text(), 'Nosotros')]",
                "//a[contains(text(), 'Servicios')]",
                "//a[contains(text(), 'Clientes')]",
                "//a[contains(text(), 'Contacto')]"
            ]

            for i, item in enumerate(menu_items, start=1):
                try:
                    btn = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, item))
                    )
                    btn.click()
                    self.take_screenshot(driver, f"infosgroup_mobile_menu_{i}")
                except Exception as e:
                    print(f"No se pudo acceder al botón {item}: {e}")

        except Exception as e:
            self.take_screenshot(driver, "infosgroup_mobile_error")
            raise e
