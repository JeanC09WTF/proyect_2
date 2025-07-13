from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import pytest
from datetime import datetime

class BrowserStackTest:
    @pytest.fixture(scope='function')
    def driver(self, request):
        capabilities = request.node.get_closest_marker("capabilities").kwargs
        capabilities.update({
            "bstack:options": {
                "userName": os.environ.get("BROWSERSTACK_USERNAME"),
                "accessKey": os.environ.get("BROWSERSTACK_ACCESS_KEY"),
                "debug": "true"
            }
        })
        
        driver = webdriver.Remote(
            command_executor="https://hub-cloud.browserstack.com/wd/hub",
            desired_capabilities=capabilities
        )
        yield driver
        driver.quit()

    def take_screenshot(self, driver, name=None):
        """Toma un screenshot y lo guarda en el directorio correcto"""
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        if not name:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = os.path.join(screenshot_dir, f"{name}.png")
        driver.save_screenshot(filepath)
        return filepath
