import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

from config import settings


def pytest_addoption(parser):
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        choices=["android", "ios"],
        help="На какой платформе гонять тесты: android или ios",
    )


@pytest.fixture
def driver(request):
    platform = request.config.getoption("--platform")

    if platform == "android":
        options = UiAutomator2Options()
        options.set_capability("app", settings.android_app)
        options.set_capability("platformName", "android")
        options.set_capability("deviceName", "Samsung Galaxy S22 Ultra")
        options.set_capability("platformVersion", "12.0")
    else:
        options = XCUITestOptions()
        options.set_capability("app", settings.ios_app)
        options.set_capability("platformName", "iOS")
        options.set_capability("deviceName", "iPhone 14 Pro Max")
        options.set_capability("platformVersion", "16.0")

    options.set_capability("browserstack.user", settings.browserstack_username)
    options.set_capability("browserstack.key", settings.browserstack_access_key)
    options.set_capability("project", settings.project_name)
    options.set_capability("build", settings.build_name)
    options.set_capability("name", request.node.name)

    remote_url = (
        f"https://{settings.browserstack_username}:"
        f"{settings.browserstack_access_key}@{settings.browserstack_url}/wd/hub"
    )

    drv = webdriver.Remote(remote_url, options=options)
    yield drv
    drv.quit()