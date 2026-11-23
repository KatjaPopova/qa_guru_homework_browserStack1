import time

import allure
import pytest
import requests
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
    session_id = drv.session_id

    dashboard_link = f"https://app-automate.browserstack.com/dashboard/v2/sessions/{session_id}"
    allure.dynamic.link(dashboard_link, name="BrowserStack session (видео, логи)")

    yield drv
    drv.quit()

    _attach_browserstack_video(session_id)


def _attach_browserstack_video(session_id: str, max_wait_seconds: int = 180, poll_interval: int = 10):
    api_url = f"https://api.browserstack.com/app-automate/sessions/{session_id}.json"
    auth = (settings.browserstack_username, settings.browserstack_access_key)

    response = requests.get(api_url, auth=auth)
    if not response.ok:
        return

    video_url = response.json().get("automation_session", {}).get("video_url")
    if not video_url:
        return

    waited = 0
    while waited < max_wait_seconds:
        video_response = requests.get(video_url)
        content = video_response.content

        if video_response.ok and len(content) > 10_000:
            allure.attach(
                content,
                name="BrowserStack session video",
                attachment_type=allure.attachment_type.MP4,
            )
            return

        time.sleep(poll_interval)
        waited += poll_interval