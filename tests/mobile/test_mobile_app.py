from ..base_test import BrowserStackTest
import pytest

class TestMobileApp(BrowserStackTest):
    @pytest.mark.capabilities(
        browserName="chrome",
        platformName="android",
        deviceName="Samsung Galaxy S22"
    )
    def test_mobile(self, driver):
        driver.get("https://mobile.twitter.com")
        assert "Twitter" in driver.title
