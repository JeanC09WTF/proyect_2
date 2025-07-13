import os
from datetime import datetime

class BrowserStackTest:
    def take_screenshot(self, driver, name=None):
        screenshot_dir = os.environ.get("SCREENSHOT_DIR", "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        
        if not name:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = os.path.join(screenshot_dir, f"{name}.png")
        driver.save_screenshot(filepath)
        return filepath
