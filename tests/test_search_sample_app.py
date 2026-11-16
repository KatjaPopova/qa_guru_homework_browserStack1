from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_successful_search(driver):
    wait = WebDriverWait(driver, 30)

    search_element = wait.until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
    )
    search_element.click()

    insert_text_element = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")
        )
    )
    insert_text_element.send_keys("Appium")

    results = wait.until(
        lambda d: d.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
    )
    assert len(results) > 0