from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
import pytest
import json
from datetime import datetime

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "capabilities: browser capabilities for BrowserStack"
    )

class BrowserStackTest:
    @pytest.fixture(scope='function')
    def driver(self, request):
        # Obtener capacidades del marcador pytest
        capabilities = request.node.get_closest_marker("capabilities").kwargs
        
        # Configuración de BrowserStack
        bstack_options = {
            "userName": os.environ.get("BROWSERSTACK_USERNAME"),
            "accessKey": os.environ.get("BROWSERSTACK_ACCESS_KEY"),
            "debug": "true",
            "consoleLogs": "verbose"
        }
        
        # Configurar opciones según el navegador
        if capabilities.get("browserName", "").lower() == "chrome":
            options = ChromeOptions()
        elif capabilities.get("browserName", "").lower() == "firefox":
            options = FirefoxOptions()
        else:
            options = ChromeOptions()  # Default
            
        # Fusionar capacidades
        capabilities["bstack:options"] = bstack_options
        for key, value in capabilities.items():
            options.set_capability(key, value)
        
        # Inicializar driver
        driver = webdriver.Remote(
            command_executor="https://hub-cloud.browserstack.com/wd/hub",
            options=options
        )
        
        yield driver
        
        # Reportar estado a BrowserStack
        status = "passed" if request.node.rep_call.passed else "failed"
        reason = "Test completed" if status == "passed" else "Test failed"
        driver.execute_script(
            f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"{status}", "reason": "{reason}"}}}}'
        )
        driver.quit()

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        rep = outcome.get_result()
        setattr(item, "rep_" + rep.when, rep)

    def take_screenshot(self, driver, name=None):
        """Toma un screenshot y lo guarda en el directorio correcto"""
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        if not name:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = os.path.join(screenshot_dir, f"{name}.png")
        driver.save_screenshot(filepath)
        return filepath
