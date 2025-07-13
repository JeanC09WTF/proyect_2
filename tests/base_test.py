from selenium import webdriver
import os
import pytest

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
