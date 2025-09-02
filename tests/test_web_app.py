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
        platformName="WINDOWS",
        name="Test Navegación Infosgroup"
    )
    def test_infosgroup_navigation(self, driver):
        """Prueba extendida: Buscar Infosgroup y navegar por botones"""
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

            # 2. Buscar Infosgroup
            search_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "q"))
            )
            search_box.send_keys("Infosgroup Panamá")
            search_box.send_keys(Keys.RETURN)

            # 3. Clic en el primer resultado de Infosgroup
            infosgroup_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.PARTIAL_LINK_TEXT, "Infosgroup")
                )
            )
            infosgroup_link.click()

            # 4. Esperar a que cargue la página de Infosgroup
            WebDriverWait(driver, 15).until(
                lambda d: "Infosgroup" in d.title or "InfosGroup" in d.page_source
            )
            self.take_screenshot(driver, "infosgroup_home")

            # 5. Navegar por algunos botones del menú principal
            menu_items = [
                "//a[contains(text(), 'Nosotros')]",
                "//a[contains(text(), 'Servicios')]",
                "//a[contains(text(), 'Clientes')]",
                "//a[contains(text(), 'Contacto')]"
            ]

            for i, item in enumerate(menu_items, start=1):
                try:
                    btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, item))
                    )
                    btn.click()
                    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)
                    self.take_screenshot(driver, f"infosgroup_menu_{i}")
                except Exception as e:
                    print(f"No se pudo acceder al botón {item}: {e}")

        except Exception as e:
            self.take_screenshot(driver, "infosgroup_error")
            raise e

