import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "capabilities: browser capabilities for BrowserStack"
    )

@pytest.fixture(scope='function')
def driver(request):
    capabilities = request.node.get_closest_marker("capabilities").kwargs
    
    bstack_options = {
        "userName": os.environ.get("BROWSERSTACK_USERNAME"),
        "accessKey": os.environ.get("BROWSERSTACK_ACCESS_KEY"),
        "debug": "true",
        "consoleLogs": "verbose"
    }
    
    browser_name = capabilities.get("browserName", "").lower()
    if browser_name == "chrome":
        options = ChromeOptions()
    elif browser_name == "firefox":
        options = FirefoxOptions()
    else:
        options = ChromeOptions()
    
    capabilities["bstack:options"] = bstack_options
    
    for key, value in capabilities.items():
        options.set_capability(key, value)
    
    driver = webdriver.Remote(
        command_executor="https://hub-cloud.browserstack.com/wd/hub",
        options=options
    )
    
    yield driver
    
    status = "failed"
    try:
        if hasattr(request.node, "rep_call") and not request.node.rep_call.failed:
            status = "passed"
    except:
        pass
    
    driver.execute_script(
        f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"{status}", "reason": "Test completed"}}}}'
    )
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
