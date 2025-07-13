from selenium import webdriver
from selenium.webdriver.common.by import By
import os
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

    def take_screenshot(self, driver, name):
        driver.save_screenshot(f"screenshots/{name}.png")

    def report_session_status(self, driver, status, reason):
        driver.execute_script(
            f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"{status}", "reason": "{reason}"}}}}'
        )
