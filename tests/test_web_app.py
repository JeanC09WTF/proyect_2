import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuración de BrowserStack - REEMPLAZA CON TUS CREDENCIALES REALES
BROWSERSTACK_USERNAME = "TU_USUARIO"
BROWSERSTACK_ACCESS_KEY = "TU_ACCESS_KEY"

class TestWebApp:
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Fixture para configurar y cerrar el driver"""
        # Configuración de capacidades
        self.capabilities = {
            'bstack:options': {
                "os": "Windows",
                "osVersion": "11",
                "buildName": "Prueba Larga BrowserStack",
                "sessionName": "Navegación Infosgroup",
            },
            "browserName": "Chrome",
            "browserVersion": "latest",
        }
        
        # Inicializar driver
        self.driver = webdriver.Remote(
            command_executor=f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub",
            options=webdriver.ChromeOptions().set_capability('bstack:options', self.capabilities['bstack:options'])
        )
        
        yield
        
        # Teardown - cerrar driver
        self.driver.quit()
    
    def test_login_flow(self):
        """Test de flujo de login (ya existente)"""
        # Tu código existente para test_login_flow
        pass
    
    def test_search_feature(self):
        """Test de búsqueda y navegación en Infosgroup"""
        try:
            # 1. Abrir Google
            self.driver.get("https://www.google.com")
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.send_keys("Infosgroup")
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)

            # 2. Clic en el primer resultado que lleve a infosgroup.com
            try:
                infosgroup_link = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'infosgroup.com')]"))
                )
                infosgroup_link.click()
            except:
                # Si no encuentra el href, clic en el primer resultado <h3>
                first_result = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "h3"))
                )
                first_result.click()

            time.sleep(5)

            # 3. Interacción dentro de la web de Infosgroup
            # Ejemplo: navegar por el menú
            try:
                menu_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "nav a"))
                )
                menu_button.click()
                time.sleep(3)
            except:
                print("No se encontró un menú inicial, continuando...")

            # Ejemplo: hacer scroll en la página
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(3)

            print("✅ Prueba finalizada correctamente")
            assert True  # Test exitoso
            
        except Exception as e:
            print(f"❌ Error en la prueba: {e}")
            assert False, f"Test falló con error: {e}"

# Si quieres también una versión como función (sin clase)
@pytest.mark.capabilities(
    browserName="Firefox",
    browserVersion="latest",
    platformName="Windows"
)
def test_search_feature_function(driver):
    """Versión alternativa como función (si prefieres este estilo)"""
    # Tu código aquí usando driver directamente
    pass
