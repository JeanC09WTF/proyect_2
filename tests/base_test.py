from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from datetime import datetime
import pytest

class BrowserStackTest:
    @pytest.fixture(scope='function')
    def driver(self, request):
        capabilities = request.node.get_closest_marker("capabilities").kwargs
        options = webdriver.ChromeOptions() if "chrome" in capabilities["browserName"].lower() else None
        
        # Configuración específica para BrowserStack
        bstack_options = {
            "userName": os.environ.get("BROWSERSTACK_USERNAME"),
            "accessKey": os.environ.get("BROWSERSTACK_ACCESS_KEY"),
            "debug": "true",
            "consoleLogs": "verbose"
        }
        
        capabilities.update({"bstack:options": bstack_options})
        
        if options:
            for cap_name, cap_value in capabilities.items():
                options.set_capability(cap_name, cap_value)
        
        driver = webdriver.Remote(
            command_executor="https://hub-cloud.browserstack.com/wd/hub",
            options=options
        )
        
        yield driver
        driver.quit()

    def take_screenshot(self, driver, name=None):
        """Toma un screenshot y lo guarda en el directorio correcto"""
        screenshot_dir = os.environ.get("SCREENSHOT_DIR", "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        
        if not name:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = os.path.join(screenshot_dir, f"{name}.png")
        driver.save_screenshot(filepath)
        return filepathe}.png")

    def report_session_status(self, driver, status, reason):
        driver.execute_script(
            f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"{status}", "reason": "{reason}"}}}}'
        )


