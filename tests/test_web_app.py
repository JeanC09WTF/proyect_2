from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuración de BrowserStack
BROWSERSTACK_USERNAME = "TU_USUARIO"
BROWSERSTACK_ACCESS_KEY = "TU_ACCESS_KEY"

capabilities = {
    'bstack:options': {
        "os": "Windows",
        "osVersion": "11",
        "buildName": "Prueba Larga BrowserStack",
        "sessionName": "Navegación Infosgroup",
    },
    "browserName": "Chrome",
    "browserVersion": "latest",
}

# Conexión con BrowserStack
driver = webdriver.Remote(
    command_executor=f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub",
    options=webdriver.ChromeOptions().set_capability('bstack:options', capabilities['bstack:options'])
)

try:
    # 1. Abrir Google
    driver.get("https://www.google.com")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys("Infosgroup")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    # 2. Clic en el primer resultado que lleve a infosgroup.com
    try:
        infosgroup_link = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'infosgroup.com')]"))
        )
        infosgroup_link.click()
    except:
        # Si no encuentra el href, clic en el primer resultado <h3>
        first_result = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "h3"))
        )
        first_result.click()

    time.sleep(5)

    # 3. Interacción dentro de la web de Infosgroup
    # Ejemplo: navegar por el menú
    try:
        menu_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "nav a"))
        )
        menu_button.click()
        time.sleep(3)
    except:
        print("No se encontró un menú inicial, continuando...")

    # Ejemplo: hacer scroll en la página
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)

    print("✅ Prueba finalizada correctamente")

finally:
    driver.quit()
