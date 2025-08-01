# locator_finder.py

from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
import argparse
import time

def connect_to_app(platform, device_name, app_package=None, app_activity=None, bundle_id=None):
    if platform.lower() == "android":
        desired_caps = {
            "platformName": "Android",
            "deviceName": device_name,
            "appPackage": app_package,
            "appActivity": app_activity,
            "automationName": "UiAutomator2",
            "noReset": True
        }
    elif platform.lower() == "ios":
        desired_caps = {
            "platformName": "iOS",
            "deviceName": device_name,
            "bundleId": bundle_id,
            "automationName": "XCUITest",
            "noReset": True
        }
    else:
        raise ValueError("Unsupported platform")

    print("[INFO] Connecting to Appium server...")
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    time.sleep(3)
    print("[INFO] Connected!")
    return driver

def find_element(driver, locator_type, locator_value):
    try:
        element = None
        if locator_type == "id":
            element = driver.find_element("id", locator_value)
        elif locator_type == "accessibility_id":
            element = driver.find_element("accessibility id", locator_value)
        elif locator_type == "xpath":
            element = driver.find_element("xpath", locator_value)
        else:
            print("[ERROR] Unsupported locator type")
            return

        print(f"[SUCCESS] Element found: {element.text if element.text else 'No text'}")
    except NoSuchElementException:
        print("[ERROR] Element not found.")

def main():
    parser = argparse.ArgumentParser(description="Find mobile app elements using Appium")
    parser.add_argument("--platform", choices=["android", "ios"], required=True)
    parser.add_argument("--device", default="Android Emulator")
    parser.add_argument("--locator_type", choices=["id", "accessibility_id", "xpath"], required=True)
    parser.add_argument("--locator_value", required=True)

    # Android only
    parser.add_argument("--package", help="Android app package name")
    parser.add_argument("--activity", help="Android app activity")

    # iOS only
    parser.add_argument("--bundle", help="iOS app bundle ID")

    args = parser.parse_args()

    driver = connect_to_app(
        args.platform,
        args.device,
        app_package=args.package,
        app_activity=args.activity,
        bundle_id=args.bundle
    )

    find_element(driver, args.locator_type, args.locator_value)
    driver.quit()

if __name__ == "__main__":
    main()
