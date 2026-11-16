from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# На bs://sample.app (iOS) нет статей Wikipedia — это демо-приложение
# "Sample iOS" с табами UI Elements / Web View / Local Testing.
# Имитируем "открытие статьи" через переход на вкладку с WebView-контентом.
WEB_VIEW_TAB = (AppiumBy.ACCESSIBILITY_ID, "Web View")
ARTICLE_WEBVIEW = (AppiumBy.CLASS_NAME, "XCUIElementTypeWebView")


def test_open_article(driver):
    wait = WebDriverWait(driver, 30)

    page_before_click = driver.page_source

    web_view_tab = wait.until(EC.element_to_be_clickable(WEB_VIEW_TAB))
    web_view_tab.click()

    wait.until(EC.presence_of_element_located(ARTICLE_WEBVIEW))

    assert driver.page_source != page_before_click